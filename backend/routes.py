from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from config import Config
from services.data_processor import DataProcessor
from services.database import Database

api = Blueprint('api', __name__)

# Initialize Database
try:
    db = Database(
        dbname="retail",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5000
    )
except Exception as e:
    db = None
    print(f"Failed to connect to the database: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@api.route('/analytics', methods=['GET'])
def get_analytics():
    try:
        if not db:
            return jsonify({'error': 'Database connection is not initialized'}), 500

        store_data = db.fetch_combined_store_data()

        return jsonify({
            'data': store_data['layout'],
            'analytics': store_data['analytics'],
            'loading': False
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'loading': False
        }), 500


@api.route('/process-data', methods=['POST'])
def process_data():
    try:
        if not db:
            return jsonify({'error': 'Database connection is not initialized'}), 500

        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Supported formats: XLSX, XLS, CSV, TXT'}), 400

        db.create_tables()
        db.clear_previous_data()

        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        file.save(filepath)

        # Log the upload in the history table
        db.add_file_history(filename)

        processor = DataProcessor(filepath, db)

        try:
            db.create_tables()
            db.clear_previous_data()

            processor.save_cleaned_data()

            # Extract data for customers, products, and sales
            customers_data = processor.get_customers_data()
            products_data = processor.get_products_data()
            sales_data = processor.get_sales_data()

            # # Save customers data
            # for customer in customers_data:
            #     db.add_customer(customer)
            #
            # # Save products data
            # for product in products_data:
            #     db.add_product(product)
            #
            # # Save sales data
            # for sale in sales_data:
            #     db.add_sale(sale)


            # Analyze data and generate layout recommendations
            analysis_results = processor.analyze_data()
            layout_recommendations = processor.generate_layout_recommendations()

            # Save analysis results and layout recommendations
            db.store_analysis_results(analysis_results)
            db.store_layout_recommendations(layout_recommendations)

            # Update the history status to Completed
            db.update_file_status(filename, status='Completed')

            return jsonify({
                'message': 'Data processed successfully',
                'category_analysis': analysis_results,
                'layout_recommendations': layout_recommendations
            })

        except Exception as e:
            # Update the history status to Failed
            db.update_file_status(filename, status='Failed', error_message=str(e))
            print(f"Error processing file: {e}")
            return jsonify({'error': str(e)}), 500

        finally:
            os.remove(filepath)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

