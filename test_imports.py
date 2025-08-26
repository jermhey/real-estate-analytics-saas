#!/usr/bin/env python3
"""
Quick import test to verify all modules can be loaded successfully
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        # Core backend
        from app.backend.app import create_app
        print("✅ Backend app import OK")
        
        # Database models
        from app.database.models import User, Property, db
        print("✅ Database models import OK")
        
        # Analytics modules
        from app.analytics.financial_calculator import FinancialCalculator
        print("✅ Financial calculator import OK")
        
        from app.analytics.monte_carlo import MonteCarloSimulator
        print("✅ Monte Carlo simulator import OK")
        
        # Frontend
        import streamlit as st
        print("✅ Streamlit import OK")
        
        # Critical dependencies
        import pandas as pd
        import numpy as np
        import plotly.graph_objects as go
        import requests
        from passlib.hash import pbkdf2_sha256
        print("✅ All dependencies import OK")
        
        # Test basic functionality
        app = create_app()
        print("✅ Flask app creation OK")
        
        # Test financial calculator with sample data
        sample_property = {
            "purchase_price": 300000,
            "down_payment": 60000,
            "loan_amount": 240000,
            "interest_rate": 6.5,
            "loan_term_years": 30,
            "monthly_rent": 2500,
            "monthly_expenses": {"property_tax": 300}
        }
        
        calc = FinancialCalculator(sample_property)
        payment = calc.calculate_monthly_payment()
        print(f"✅ Financial calculation test OK (Monthly payment: ${payment:.2f})")
        
        print("\n🎉 All imports and basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
