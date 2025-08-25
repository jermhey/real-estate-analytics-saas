"""
Database models for Real Estate Analytics SaaS
Production-grade SQLAlchemy models with proper relationships and constraints
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and account management"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    
    # Subscription management
    subscription_tier = db.Column(db.String(20), default='free', nullable=False)
    stripe_customer_id = db.Column(db.String(100), unique=True, nullable=True)
    subscription_status = db.Column(db.String(20), default='active', nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    properties = db.relationship('Property', backref='owner', lazy=True, cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'subscription_tier': self.subscription_tier,
            'created_at': self.created_at.isoformat(),
            'properties_count': len(self.properties)
        }

class Property(db.Model):
    """Property model for real estate investments"""
    
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Basic property information
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=False)
    property_type = db.Column(db.String(50), default='residential', nullable=False)
    
    # Financial details
    purchase_price = db.Column(db.Numeric(12, 2), nullable=False)
    down_payment = db.Column(db.Numeric(12, 2), nullable=False)
    loan_amount = db.Column(db.Numeric(12, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 3), nullable=False)  # Stored as decimal (6.5% = 6.500)
    loan_term_years = db.Column(db.Integer, nullable=False)
    
    # Income
    monthly_rent = db.Column(db.Numeric(10, 2), nullable=False)
    other_monthly_income = db.Column(db.Numeric(10, 2), default=0)
    
    # Expenses (stored as JSON for flexibility)
    monthly_expenses = db.Column(JSON, default=dict, nullable=False)
    
    # Property characteristics
    square_footage = db.Column(db.Integer, nullable=True)
    bedrooms = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Numeric(3, 1), nullable=True)
    year_built = db.Column(db.Integer, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    analyses = db.relationship('Analysis', backref='property', lazy=True, cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='property', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Property {self.name}>'
    
    @property
    def total_investment(self):
        """Calculate total initial investment"""
        return self.down_payment + self.monthly_expenses.get('closing_costs', 0)
    
    @property
    def loan_to_value_ratio(self):
        """Calculate loan-to-value ratio"""
        return float(self.loan_amount / self.purchase_price * 100)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'property_type': self.property_type,
            'purchase_price': float(self.purchase_price),
            'down_payment': float(self.down_payment),
            'loan_amount': float(self.loan_amount),
            'interest_rate': float(self.interest_rate),
            'loan_term_years': self.loan_term_years,
            'monthly_rent': float(self.monthly_rent),
            'monthly_expenses': self.monthly_expenses,
            'total_investment': float(self.total_investment),
            'loan_to_value_ratio': self.loan_to_value_ratio,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Analysis(db.Model):
    """Analysis results for property evaluations"""
    
    __tablename__ = 'analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    
    # Analysis type
    analysis_type = db.Column(db.String(50), nullable=False)  # 'basic', 'monte_carlo', 'scenario'
    
    # Analysis parameters
    parameters = db.Column(JSON, default=dict, nullable=False)
    
    # Results
    results = db.Column(JSON, default=dict, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Analysis {self.analysis_type} for Property {self.property_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'analysis_type': self.analysis_type,
            'parameters': self.parameters,
            'results': self.results,
            'created_at': self.created_at.isoformat()
        }

class Report(db.Model):
    """Generated reports for properties"""
    
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False, index=True)
    
    # Report details
    report_type = db.Column(db.String(50), nullable=False)  # 'investment_analysis', 'risk_assessment'
    title = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(500), nullable=True)  # Path to generated PDF
    
    # Report parameters and data
    parameters = db.Column(JSON, default=dict, nullable=False)
    
    # Status
    status = db.Column(db.String(20), default='pending', nullable=False)  # 'pending', 'completed', 'failed'
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Report {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'report_type': self.report_type,
            'title': self.title,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class UserSession(db.Model):
    """User session tracking for security and analytics"""
    
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Session details
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<UserSession {self.id} for User {self.user_id}>'
