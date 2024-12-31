import psycopg2
from psycopg2.extras import Json
from typing import Dict, List

class Database:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int = 5000):
        try:
            self.conn = psycopg2.connect(
                dbname="retail",
                user="postgres",
                password="postgres",
                host="localhost",
                port=5000
            )
            self.create_tables()
        except Exception as e:
            raise ValueError(f"Database initialization failed: {e}")

    def create_tables(self):
        with self.conn.cursor() as cur:
            # Customers Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id TEXT PRIMARY KEY,
                    customer_name TEXT NOT NULL,
                    segment TEXT NOT NULL,
                    country TEXT NOT NULL,
                    region TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state_province TEXT NOT NULL,
                    postal_code TEXT NOT NULL
                )
            """)

            # Products Table - Changed category to sub_category
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id TEXT PRIMARY KEY,
                    sub_category TEXT NOT NULL,  
                    product_name TEXT NOT NULL
                )
            """)

            # Sales Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    id SERIAL PRIMARY KEY,
                    order_id TEXT,
                    customer_id TEXT REFERENCES customers(customer_id),
                    product_id TEXT REFERENCES products(product_id),
                    sales NUMERIC NOT NULL,
                    quantity INTEGER NOT NULL,
                    discount NUMERIC NOT NULL,
                    profit NUMERIC NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Normalized Data Table - Changed category to sub_category
            cur.execute("""
                CREATE TABLE IF NOT EXISTS normalized_data (
                    id SERIAL PRIMARY KEY,
                    order_id TEXT NOT NULL,
                    customer_id TEXT REFERENCES customers(customer_id),
                    product_id TEXT REFERENCES products(product_id),
                    sub_category TEXT NOT NULL,  
                    sales NUMERIC NOT NULL,
                    quantity INTEGER NOT NULL,
                    profit NUMERIC NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Layout Recommendations Table - Changed category to sub_category
            cur.execute("""
                CREATE TABLE IF NOT EXISTS layout_recommendations (
                    id SERIAL PRIMARY KEY,
                    product_id TEXT REFERENCES products(product_id),
                    section INTEGER NOT NULL CHECK (section >= 0 AND section < 30),
                    priority TEXT CHECK (priority IN ('high', 'medium', 'low')),
                    sub_category TEXT NOT NULL,  -- Changed category to sub_category
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Add Products per Section View - Changed category to sub_category
            cur.execute("""
                CREATE OR REPLACE VIEW section_products AS
                SELECT 
                    lr.section,
                    lr.priority,
                    lr.sub_category,  
                    json_agg(json_build_object(
                        'id', p.product_id,
                        'name', p.product_name
                    )) as products
                FROM layout_recommendations as lr
                JOIN products as p ON p.product_id = lr.product_id
                GROUP BY lr.section, lr.priority, lr.sub_category
            """)

            # Analytics Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id SERIAL PRIMARY KEY,
                    metrics JSONB NOT NULL,
                    sub_category_analysis JSONB NOT NULL,  -- Changed category_analysis to sub_category_analysis
                    top_products JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # File Upload History Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS file_history (
                    id SERIAL PRIMARY KEY,
                    filename TEXT NOT NULL,
                    status TEXT NOT NULL,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.conn.commit()

    def add_customer(self, customer_data: Dict):
        """Add a customer record."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO customers (customer_id,customer_name, segment, country, region, city, state_province, postal_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
            """, (
                customer_data['customer_id'],
                customer_data['customer_name'],
                customer_data['segment'],
                customer_data['country'],
                customer_data['region'],
                customer_data['city'],
                customer_data['state_province'],
                customer_data['postal_code']
            ))
            self.conn.commit()

    def add_product(self, product_data: Dict):
        """Add a product record."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO products (product_id, sub_category, product_name)
                VALUES (%s, %s, %s)
            """, (
                product_data['product_id'],
                product_data['sub_category'],  # Changed category to sub_category
                product_data['product_name']
            ))
            self.conn.commit()

    def add_sale(self, sale_data: Dict):
        """Add a sale record."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO sales (order_id, customer_id, product_id, sales, quantity, discount, profit)
                VALUES (%s, %s, %s, %s, %s, %s,%s)
            """, (
                sale_data['order_id'],
                sale_data['customer_id'],
                sale_data['product_id'],
                sale_data['sales'],
                sale_data['quantity'],
                sale_data['discount'],
                sale_data['profit']
            ))
            self.conn.commit()

    def store_normalized_data(self, normalized_data: Dict):
        """Store normalized data."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO normalized_data (order_id, customer_id, product_id, sub_category, sales, quantity, profit)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                normalized_data['order_id'],
                normalized_data['customer_id'],
                normalized_data['product_id'],
                normalized_data['sub_category'],  # Changed category to sub_category
                normalized_data['sales'],
                normalized_data['quantity'],
                normalized_data['profit']
            ))
            self.conn.commit()

    def store_layout_recommendations(self, recommendations: Dict):
        """Store layout recommendations with product details."""
        with self.conn.cursor() as cur:
            # Validate section values
            for product_id, data in recommendations.items():
                if not (0 <= data['section'] <= 30):  # Check if section is within valid range
                    raise ValueError(f"Invalid section value: {data['section']}. Must be between 0 and 30.")

                # Insert new recommendations
                cur.execute("""
                    INSERT INTO layout_recommendations 
                    (product_id, section, priority, sub_category)
                    VALUES (%s, %s, %s, %s)
                """, (
                    product_id,
                    data['section'],
                    data['priority'],
                    data['sub_category']  # Changed category to sub_category
                ))
            self.conn.commit()

    def store_analysis_results(self, results: Dict):
        """Store analysis results."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO analysis_results (metrics, sub_category_analysis, top_products)
                VALUES (%s, %s, %s)
            """, (
                Json(results['metrics']),
                Json(results['sub_category_analysis']),  # Changed category_analysis to sub_category_analysis
                Json(results.get('top_products', {}))
            ))
            self.conn.commit()

    def fetch_normalized_data(self) -> List[Dict]:
        """Fetch all normalized data."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM normalized_data
            """)
            rows = cur.fetchall()
            return [{
                'id': row[0],
                'order_id': row[1],
                'customer_id': row[2],
                'product_id': row[3],
                'sub_category': row[4],  # Changed category to sub_category
                'sales': row[5],
                'quantity': row[6],
                'profit': row[7],
                'created_at': row[8]
            } for row in rows]

    def fetch_store_layout(self) -> Dict:
        """Fetch complete store layout data in the format needed by the frontend."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    lr.product_id AS layout_product_id,
                    lr.section,
                    lr.priority,
                    lr.sub_category, 
                    p.product_name
                FROM layout_recommendations lr
                JOIN products p ON p.product_id = lr.product_id
                ORDER BY lr.section, lr.priority
            """)
            rows = cur.fetchall()

            # Format data as needed by the frontend
            layout_data = {}
            for product_id, section, priority, sub_category, product_name in rows:
                layout_data[product_id] = {
                    'section': section,
                    'priority': priority,
                    'sub_category': sub_category,  # Changed category to sub_category
                    'products': [{
                        'name': product_name,
                        'id': product_id
                    }]
                }

            return layout_data

    def fetch_combined_store_data(self) -> Dict:
        """Fetch both layout and analytics data in a single query."""
        try:
            # Fetch layout data
            layout_data = self.fetch_store_layout()

            # Fetch analytics data
            analysis_results = self.fetch_analysis_results()

            # Combine the data
            return {
                'layout': layout_data,
                'analytics': {
                    'metrics': analysis_results.get('metrics', {}),
                    'sub_category_analysis': analysis_results.get('sub_category_analysis', {}),
                    'top_products': analysis_results.get('top_products', {})
                }
            }
        except Exception as e:
            # Rollback to ensure the transaction state is clean
            self.conn.rollback()
            raise Exception(f"Error fetching combined store data: {e}")

    def fetch_analysis_results(self) -> List[Dict]:
        """Fetch all analysis results."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT metrics, sub_category_analysis, top_products  
                FROM analysis_results
                ORDER BY created_at DESC LIMIT 1
            """)
            row = cur.fetchone()
            return {
                'metrics': row[0],
                'sub_category_analysis': row[1],
                'top_products': row[2]
            } if row else {}

    def add_file_history(self, filename: str):
        """Log the file upload in the file history table."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO file_history (filename, status)
                VALUES (%s, %s)
            """, (filename, 'Pending'))  # Set initial status as 'Pending'
            self.conn.commit()

    def update_file_status(self, filename: str, status: str, error_message: str = None):
        """Update the status of the uploaded file."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    UPDATE file_history
                    SET status = %s, error_message = %s
                    WHERE filename = %s
                """, (status, error_message, filename))
                self.conn.commit()
        except Exception as e:
            print(f"Error updating file status for {filename}: {e}")
            self.conn.rollback()  # Rollback in case of an error

    def clear_previous_data(self):
        """
        Clears all data from the relevant tables except the file history table.
        """
        try:
            # List of tables to clear (excluding 'file_history')
            tables_to_clear = ['analysis_results', 'layout_recommendations', 'normalized_data', 'sales', 'products',
                               'customers']

            for table in tables_to_clear:
                with self.conn.cursor() as cur:
                    # Corrected the query to properly include the table name
                    cur.execute(f"DELETE FROM {table};")
                    self.conn.commit()

            print("Data cleared successfully from the relevant tables.")

        except Exception as e:
            print(f"Error clearing previous data: {e}")
            self.conn.rollback()  # Rollback in case of an error
