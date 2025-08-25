#!/usr/bin/env python3
"""
Database setup script
Initialize the PostgreSQL database with all required tables
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.backend.app import create_app
from app.database.models import db, User, Property, Analysis, Report, UserSession
from dotenv import load_dotenv

def setup_database():
    """Initialize database with all tables"""
    
    # Load environment variables
    load_dotenv()
    
    print("🔧 Setting up Real Estate Analytics Database...")
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Drop all tables (for fresh start)
            print("📋 Dropping existing tables...")
            db.drop_all()
            
            # Create all tables
            print("🏗️  Creating database tables...")
            db.create_all()
            
            # Verify tables were created
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✅ Created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"   • {table}")
            
            # Create default admin user (optional)
            admin_email = os.getenv('ADMIN_EMAIL')
            if admin_email:
                print(f"\n👤 Creating admin user: {admin_email}")
                
                from passlib.hash import pbkdf2_sha256
                
                admin_user = User(
                    email=admin_email,
                    first_name="Admin",
                    last_name="User",
                    password_hash=pbkdf2_sha256.hash("admin123"),
                    subscription_tier="enterprise"
                )
                
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Admin user created successfully")
            
            print("\n🎉 Database setup completed successfully!")
            print("\n📝 Next steps:")
            print("   1. Update your .env file with correct database credentials")
            print("   2. Run: python scripts/run_dev.py")
            print("   3. Open http://localhost:8501 in your browser")
            
        except Exception as e:
            print(f"❌ Database setup failed: {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)
