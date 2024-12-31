from flask import Flask
from flask_cors import CORS
import os
from config import Config
from routes import api

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Ensure upload directory exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5500)
