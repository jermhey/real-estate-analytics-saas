"""
General API routes
Health checks, status endpoints, and utility functions
"""

from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.database.models import User, Property
from app.backend.app import db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/status', methods=['GET'])
def get_status():
    """API status and health check"""
    return jsonify({
        'status': 'operational',
        'version': '1.0.0',
        'service': 'Real Estate Analytics API',
        'features': [
            'User Authentication',
            'Property Management',
            'Financial Analysis',
            'Monte Carlo Simulation',
            'PDF Report Generation'
        ]
    }), 200

@bp.route('/dashboard', methods=['GET'])
@login_required
def get_dashboard_data():
    """Get dashboard summary data for the current user"""
    try:
        # Get user's properties
        properties = Property.query.filter_by(user_id=current_user.id).all()
        
        # Calculate summary statistics
        total_properties = len(properties)
        total_investment = sum(prop.purchase_price for prop in properties)
        total_monthly_rent = sum(prop.monthly_rent for prop in properties)
        
        # Recent activity (last 5 properties)
        recent_properties = Property.query.filter_by(user_id=current_user.id)\
                                        .order_by(Property.created_at.desc())\
                                        .limit(5).all()
        
        return jsonify({
            'summary': {
                'total_properties': total_properties,
                'total_investment': float(total_investment),
                'total_monthly_rent': float(total_monthly_rent),
                'average_rent_per_property': float(total_monthly_rent / total_properties) if total_properties > 0 else 0
            },
            'recent_properties': [{
                'id': prop.id,
                'name': prop.name,
                'address': prop.address,
                'purchase_price': float(prop.purchase_price),
                'monthly_rent': float(prop.monthly_rent),
                'created_at': prop.created_at.isoformat()
            } for prop in recent_properties],
            'user_info': {
                'subscription_tier': current_user.subscription_tier,
                'properties_limit': get_property_limit(current_user.subscription_tier)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to load dashboard data'}), 500

def get_property_limit(subscription_tier):
    """Get property limit based on subscription tier"""
    limits = {
        'free': 1,
        'pro': 10,
        'enterprise': 999999  # Unlimited
    }
    return limits.get(subscription_tier, 1)

@bp.route('/subscription/limits', methods=['GET'])
@login_required
def get_subscription_limits():
    """Get current user's subscription limits"""
    tier = current_user.subscription_tier
    properties_count = Property.query.filter_by(user_id=current_user.id).count()
    
    limits = {
        'free': {
            'properties': 1,
            'monte_carlo_simulations': 5,
            'pdf_reports': 2
        },
        'pro': {
            'properties': 10,
            'monte_carlo_simulations': 100,
            'pdf_reports': 50
        },
        'enterprise': {
            'properties': 999999,
            'monte_carlo_simulations': 999999,
            'pdf_reports': 999999
        }
    }
    
    current_limits = limits.get(tier, limits['free'])
    
    return jsonify({
        'subscription_tier': tier,
        'limits': current_limits,
        'usage': {
            'properties': properties_count
        },
        'can_add_property': properties_count < current_limits['properties']
    }), 200
