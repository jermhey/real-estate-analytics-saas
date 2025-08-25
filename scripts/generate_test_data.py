#!/usr/bin/env python3
"""
Test data generation script
Create sample properties and users for development and testing
"""

import os
import sys
from pathlib import Path
import random
from decimal import Decimal

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.backend.app import create_app, db
from app.database.models import User, Property
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv

# Sample data
SAMPLE_USERS = [
    {
        "email": "investor1@example.com",
        "first_name": "John",
        "last_name": "Smith",
        "subscription_tier": "pro"
    },
    {
        "email": "investor2@example.com", 
        "first_name": "Sarah",
        "last_name": "Johnson",
        "subscription_tier": "free"
    },
    {
        "email": "investor3@example.com",
        "first_name": "Michael",
        "last_name": "Brown",
        "subscription_tier": "enterprise"
    }
]

SAMPLE_PROPERTIES = [
    {
        "name": "Downtown Duplex",
        "address": "123 Main Street, Austin, TX 78701",
        "purchase_price": 450000,
        "down_payment": 90000,
        "loan_amount": 360000,
        "interest_rate": 6.5,
        "loan_term_years": 30,
        "monthly_rent": 3200,
        "monthly_expenses": {
            "property_tax": 450,
            "insurance": 200,
            "maintenance": 300,
            "vacancy_allowance": 160,
            "property_management": 224,
            "hoa_fees": 0,
            "other_expenses": 100
        }
    },
    {
        "name": "Suburban Family Home",
        "address": "456 Oak Avenue, Round Rock, TX 78664",
        "purchase_price": 320000,
        "down_payment": 64000,
        "loan_amount": 256000,
        "interest_rate": 6.25,
        "loan_term_years": 30,
        "monthly_rent": 2400,
        "monthly_expenses": {
            "property_tax": 350,
            "insurance": 150,
            "maintenance": 250,
            "vacancy_allowance": 120,
            "property_management": 168,
            "hoa_fees": 50,
            "other_expenses": 75
        }
    },
    {
        "name": "Condo Investment",
        "address": "789 High Rise Blvd #15C, Dallas, TX 75201",
        "purchase_price": 275000,
        "down_payment": 55000,
        "loan_amount": 220000,
        "interest_rate": 6.75,
        "loan_term_years": 30,
        "monthly_rent": 2100,
        "monthly_expenses": {
            "property_tax": 300,
            "insurance": 125,
            "maintenance": 150,
            "vacancy_allowance": 105,
            "property_management": 147,
            "hoa_fees": 250,
            "other_expenses": 50
        }
    },
    {
        "name": "Student Housing Quad",
        "address": "321 University Drive, College Station, TX 77840",
        "purchase_price": 380000,
        "down_payment": 76000,
        "loan_amount": 304000,
        "interest_rate": 6.8,
        "loan_term_years": 30,
        "monthly_rent": 2800,
        "monthly_expenses": {
            "property_tax": 400,
            "insurance": 180,
            "maintenance": 350,
            "vacancy_allowance": 140,
            "property_management": 196,
            "hoa_fees": 0,
            "other_expenses": 125
        }
    },
    {
        "name": "Historic Bungalow",
        "address": "567 Heritage Lane, San Antonio, TX 78212",
        "purchase_price": 225000,
        "down_payment": 45000,
        "loan_amount": 180000,
        "interest_rate": 6.0,
        "loan_term_years": 30,
        "monthly_rent": 1800,
        "monthly_expenses": {
            "property_tax": 250,
            "insurance": 120,
            "maintenance": 200,
            "vacancy_allowance": 90,
            "property_management": 126,
            "hoa_fees": 0,
            "other_expenses": 60
        }
    }
]

def create_sample_users():
    """Create sample users"""
    print("👥 Creating sample users...")
    
    created_users = []
    
    for user_data in SAMPLE_USERS:
        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if existing_user:
            print(f"   • User {user_data['email']} already exists, skipping...")
            created_users.append(existing_user)
            continue
        
        user = User()
        user.email = user_data["email"]
        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.password_hash = pbkdf2_sha256.hash("password123")
        user.subscription_tier = user_data["subscription_tier"]
        
        db.session.add(user)
        created_users.append(user)
        print(f"   ✅ Created user: {user_data['email']}")
    
    db.session.commit()
    return created_users

def create_sample_properties(users):
    """Create sample properties for users"""
    print("🏠 Creating sample properties...")
    
    created_properties = []
    
    for i, property_data in enumerate(SAMPLE_PROPERTIES):
        # Assign properties to users in round-robin fashion
        user = users[i % len(users)]
        
        # Check if property already exists for this user
        existing_property = Property.query.filter_by(
            user_id=user.id, 
            name=property_data["name"]
        ).first()
        
        if existing_property:
            print(f"   • Property '{property_data['name']}' already exists for {user.email}, skipping...")
            created_properties.append(existing_property)
            continue
        
        property_obj = Property()
        property_obj.user_id = user.id
        property_obj.name = property_data["name"]
        property_obj.address = property_data["address"]
        property_obj.purchase_price = Decimal(str(property_data["purchase_price"]))
        property_obj.down_payment = Decimal(str(property_data["down_payment"]))
        property_obj.loan_amount = Decimal(str(property_data["loan_amount"]))
        property_obj.interest_rate = Decimal(str(property_data["interest_rate"]))
        property_obj.loan_term_years = property_data["loan_term_years"]
        property_obj.monthly_rent = Decimal(str(property_data["monthly_rent"]))
        property_obj.monthly_expenses = property_data["monthly_expenses"]
        
        db.session.add(property_obj)
        created_properties.append(property_obj)
        print(f"   ✅ Created property: {property_data['name']} for {user.email}")
    
    db.session.commit()
    return created_properties

def generate_additional_properties(users, count=10):
    """Generate additional random properties for testing"""
    print(f"🎲 Generating {count} additional random properties...")
    
    # Property templates for random generation
    property_types = [
        "Single Family Home",
        "Duplex", 
        "Triplex",
        "Fourplex",
        "Condo",
        "Townhouse"
    ]
    
    cities = [
        ("Austin", "78701"),
        ("Dallas", "75201"),
        ("Houston", "77001"),
        ("San Antonio", "78201"),
        ("Fort Worth", "76101"),
        ("Plano", "75024"),
        ("Irving", "75038"),
        ("Garland", "75040")
    ]
    
    streets = [
        "Main Street", "Oak Avenue", "Pine Road", "Maple Drive",
        "Cedar Lane", "Elm Street", "Park Boulevard", "River Road",
        "Hill Street", "Valley Drive", "Sunset Avenue", "Sunrise Lane"
    ]
    
    for i in range(count):
        user = random.choice(users)
        property_type = random.choice(property_types)
        city, zip_code = random.choice(cities)
        street = random.choice(streets)
        
        # Generate realistic financial data
        purchase_price = random.randint(150, 600) * 1000  # $150k - $600k
        down_payment_percent = random.choice([0.20, 0.25, 0.30])  # 20%, 25%, or 30%
        down_payment = int(purchase_price * down_payment_percent)
        loan_amount = purchase_price - down_payment
        interest_rate = round(random.uniform(5.5, 7.5), 2)  # 5.5% - 7.5%
        
        # Calculate reasonable rent (typically 0.8% - 1.2% of purchase price per month)
        monthly_rent = int(purchase_price * random.uniform(0.008, 0.012))
        
        # Generate expenses
        expenses = {
            "property_tax": int(monthly_rent * random.uniform(0.15, 0.25)),
            "insurance": int(monthly_rent * random.uniform(0.08, 0.15)),
            "maintenance": int(monthly_rent * random.uniform(0.10, 0.20)),
            "vacancy_allowance": int(monthly_rent * random.uniform(0.05, 0.10)),
            "property_management": int(monthly_rent * random.uniform(0.08, 0.12)),
            "hoa_fees": random.choice([0, 0, 0, int(monthly_rent * random.uniform(0.05, 0.15))]),  # 75% chance of no HOA
            "other_expenses": int(monthly_rent * random.uniform(0.02, 0.08))
        }
        
        property_obj = Property()
        property_obj.user_id = user.id
        property_obj.name = f"{property_type} #{i+1}"
        property_obj.address = f"{random.randint(100, 9999)} {street}, {city}, TX {zip_code}"
        property_obj.purchase_price = Decimal(str(purchase_price))
        property_obj.down_payment = Decimal(str(down_payment))
        property_obj.loan_amount = Decimal(str(loan_amount))
        property_obj.interest_rate = Decimal(str(interest_rate))
        property_obj.loan_term_years = random.choice([15, 20, 30])
        property_obj.monthly_rent = Decimal(str(monthly_rent))
        property_obj.monthly_expenses = expenses
        
        db.session.add(property_obj)
        
        if (i + 1) % 5 == 0:
            print(f"   • Generated {i+1}/{count} properties...")
    
    db.session.commit()
    print(f"   ✅ Generated {count} additional properties")

def main():
    """Main function to generate test data"""
    load_dotenv()
    
    print("🏠 Real Estate Analytics SaaS - Test Data Generator")
    print("=" * 55)
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Create sample users
            users = create_sample_users()
            
            # Create sample properties
            properties = create_sample_properties(users)
            
            # Generate additional random properties
            generate_additional_properties(users, count=15)
            
            # Summary
            total_users = User.query.count()
            total_properties = Property.query.count()
            
            print(f"\n📊 Test data generation completed!")
            print(f"   • Total users: {total_users}")
            print(f"   • Total properties: {total_properties}")
            
            print(f"\n🔐 Sample login credentials:")
            for user_data in SAMPLE_USERS:
                print(f"   • {user_data['email']} / password123 ({user_data['subscription_tier']})")
            
            print(f"\n🚀 You can now run the development server:")
            print(f"   python scripts/run_dev.py")
            
        except Exception as e:
            print(f"❌ Error generating test data: {str(e)}")
            db.session.rollback()
            return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
