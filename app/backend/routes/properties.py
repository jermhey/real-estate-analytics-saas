"""
Property management routes
CRUD operations for real estate properties
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.database.models import Property
from app.backend.app import db
from app.analytics.financial_calculator import FinancialCalculator
from app.analytics.monte_carlo import MonteCarloSimulator
from datetime import datetime

bp = Blueprint('properties', __name__, url_prefix='/api/properties')

@bp.route('/', methods=['GET'])
@login_required
def get_properties():
    """Get all properties for the current user"""
    properties = Property.query.filter_by(user_id=current_user.id).all()
    
    return jsonify({
        'properties': [{
            'id': prop.id,
            'name': prop.name,
            'address': prop.address,
            'purchase_price': float(prop.purchase_price),
            'monthly_rent': float(prop.monthly_rent),
            'created_at': prop.created_at.isoformat(),
            'updated_at': prop.updated_at.isoformat()
        } for prop in properties]
    }), 200

@bp.route('/', methods=['POST'])
@login_required
def create_property():
    """
    Create a new property
    
    Expected JSON payload:
    {
        "name": "Property Name",
        "address": "123 Main St, City, State",
        "purchase_price": 250000,
        "down_payment": 50000,
        "loan_amount": 200000,
        "interest_rate": 6.5,
        "loan_term_years": 30,
        "monthly_rent": 2500,
        "monthly_expenses": {
            "property_tax": 300,
            "insurance": 150,
            "maintenance": 200,
            "vacancy_allowance": 125,
            "property_management": 175,
            "hoa_fees": 0,
            "other_expenses": 50
        }
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'address', 'purchase_price', 'down_payment', 
                          'loan_amount', 'interest_rate', 'loan_term_years', 'monthly_rent']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create property
        property = Property()
        property.user_id = current_user.id
        property.name = data['name']
        property.address = data['address']
        property.purchase_price = data['purchase_price']
        property.down_payment = data['down_payment']
        property.loan_amount = data['loan_amount']
        property.interest_rate = data['interest_rate']
        property.loan_term_years = data['loan_term_years']
        property.monthly_rent = data['monthly_rent']
        property.monthly_expenses = data.get('monthly_expenses', {})
        
        db.session.add(property)
        db.session.commit()
        
        return jsonify({
            'message': 'Property created successfully',
            'property_id': property.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create property'}), 500

@bp.route('/<int:property_id>', methods=['GET'])
@login_required
def get_property(property_id):
    """Get a specific property with detailed information"""
    property = Property.query.filter_by(id=property_id, user_id=current_user.id).first()
    
    if not property:
        return jsonify({'error': 'Property not found'}), 404
    
    return jsonify({
        'property': {
            'id': property.id,
            'name': property.name,
            'address': property.address,
            'purchase_price': float(property.purchase_price),
            'down_payment': float(property.down_payment),
            'loan_amount': float(property.loan_amount),
            'interest_rate': float(property.interest_rate),
            'loan_term_years': property.loan_term_years,
            'monthly_rent': float(property.monthly_rent),
            'monthly_expenses': property.monthly_expenses,
            'created_at': property.created_at.isoformat(),
            'updated_at': property.updated_at.isoformat()
        }
    }), 200

@bp.route('/<int:property_id>/analysis', methods=['GET'])
@login_required
def analyze_property(property_id):
    """Generate comprehensive financial analysis for a property"""
    property = Property.query.filter_by(id=property_id, user_id=current_user.id).first()
    
    if not property:
        return jsonify({'error': 'Property not found'}), 404
    
    try:
        # Initialize financial calculator
        calculator = FinancialCalculator(property)
        
        # Calculate basic metrics
        analysis = {
            'cash_flow': calculator.calculate_monthly_cash_flow(),
            'annual_cash_flow': calculator.calculate_annual_cash_flow(),
            'roi': calculator.calculate_roi(),
            'cap_rate': calculator.calculate_cap_rate(),
            'cash_on_cash_return': calculator.calculate_cash_on_cash_return(),
            'dscr': calculator.calculate_dscr(),
            'monthly_payment': calculator.calculate_monthly_payment(),
            'total_monthly_expenses': calculator.calculate_total_monthly_expenses(),
            'net_operating_income': calculator.calculate_noi()
        }
        
        return jsonify({
            'property_id': property_id,
            'analysis': analysis,
            'calculated_at': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Analysis calculation failed'}), 500

@bp.route('/<int:property_id>/monte-carlo', methods=['POST'])
@login_required
def run_monte_carlo(property_id):
    """
    Run Monte Carlo simulation for risk analysis
    
    Expected JSON payload:
    {
        "simulations": 10000,
        "years": 10,
        "rent_growth_range": [0.02, 0.05],
        "expense_volatility": 0.1,
        "vacancy_rate_range": [0.05, 0.15],
        "interest_rate_volatility": 0.02
    }
    """
    property = Property.query.filter_by(id=property_id, user_id=current_user.id).first()
    
    if not property:
        return jsonify({'error': 'Property not found'}), 404
    
    try:
        data = request.get_json()
        
        # Default simulation parameters
        params = {
            'simulations': data.get('simulations', 10000),
            'years': data.get('years', 10),
            'rent_growth_range': data.get('rent_growth_range', [0.02, 0.05]),
            'expense_volatility': data.get('expense_volatility', 0.1),
            'vacancy_rate_range': data.get('vacancy_rate_range', [0.05, 0.15]),
            'interest_rate_volatility': data.get('interest_rate_volatility', 0.02)
        }
        
        # Run Monte Carlo simulation
        simulator = MonteCarloSimulator(property, params)
        results = simulator.run_simulation()
        
        return jsonify({
            'property_id': property_id,
            'simulation_results': results,
            'parameters': params,
            'simulated_at': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Monte Carlo simulation failed'}), 500

@bp.route('/<int:property_id>', methods=['PUT'])
@login_required
def update_property(property_id):
    """Update an existing property"""
    property = Property.query.filter_by(id=property_id, user_id=current_user.id).first()
    
    if not property:
        return jsonify({'error': 'Property not found'}), 404
    
    try:
        data = request.get_json()
        
        # Update fields if provided
        updatable_fields = ['name', 'address', 'purchase_price', 'down_payment',
                           'loan_amount', 'interest_rate', 'loan_term_years',
                           'monthly_rent', 'monthly_expenses']
        
        for field in updatable_fields:
            if field in data:
                setattr(property, field, data[field])
        
        property.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Property updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update property'}), 500

@bp.route('/<int:property_id>', methods=['DELETE'])
@login_required
def delete_property(property_id):
    """Delete a property"""
    property = Property.query.filter_by(id=property_id, user_id=current_user.id).first()
    
    if not property:
        return jsonify({'error': 'Property not found'}), 404
    
    try:
        db.session.delete(property)
        db.session.commit()
        
        return jsonify({'message': 'Property deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete property'}), 500
