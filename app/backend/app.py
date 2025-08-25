"""
Flask Backend Application
Production-grade API server for Real Estate Analytics SaaS
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
import os
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
from app.database.models import db
login_manager = LoginManager()

def create_app(config_name='development'):
    """
    Application factory pattern for creating Flask app instances
    
    Args:
        config_name (str): Configuration environment name
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Use SQLite for development, PostgreSQL for production
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        # Default to SQLite for development
        import tempfile
        db_path = os.path.join(tempfile.gettempdir(), 'real_estate_dev.db')
        database_url = f'sqlite:///{db_path}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for API-only application
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app, origins=["http://localhost:8502", "http://127.0.0.1:8502"])  # Allow Streamlit frontend
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.database.models import User
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.backend.routes import auth, api, properties
    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(properties.bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'service': 'Real Estate Analytics API'
        })
    
    # Database initialization endpoint (development only)
    @app.route('/init-db', methods=['POST'])
    def init_database():
        try:
            db.create_all()
            return jsonify({'message': 'Database tables created successfully'}), 200
        except Exception as e:
            return jsonify({'error': f'Database initialization failed: {str(e)}'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
