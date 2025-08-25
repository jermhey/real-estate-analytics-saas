#!/usr/bin/env python3
"""
Real Estate Analytics SaaS - Live Demo Script
Demonstrates key features for potential customers/investors
"""

import sys
import os
import requests
import json
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def demo_api_functionality():
    """Demonstrate API functionality"""
    print("🔗 API Demo - Testing Live Endpoints")
    print("=" * 50)
    
    base_url = "http://localhost:5002"
    
    # Test health check
    print("1. 🏥 Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ API is healthy and operational")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ API not running: {e}")
        return False
    
    # Test status endpoint
    print("2. 📊 API Status...")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service: {data['service']}")
            print(f"   ✅ Version: {data['version']}")
            print(f"   ✅ Features: {len(data['features'])} available")
        else:
            print(f"   ❌ Status check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Status check error: {e}")
    
    return True

def demo_financial_calculations():
    """Demonstrate financial calculation engine"""
    print("\n🧮 Financial Calculator Demo")
    print("=" * 50)
    
    from app.analytics.financial_calculator import FinancialCalculator
    
    # Sample luxury property
    property_data = {
        'name': 'Luxury Downtown Condo',
        'purchase_price': 850000,
        'down_payment': 170000,
        'loan_amount': 680000,
        'interest_rate': 7.25,
        'loan_term_years': 30,
        'monthly_rent': 4200,
        'monthly_expenses': {
            'property_tax': 650,
            'insurance': 350,
            'maintenance': 400,
            'hoa_fees': 450,
            'property_management': 336,  # 8% of rent
            'vacancy_allowance': 350     # ~8% vacancy
        }
    }
    
    print(f"📍 Property: {property_data['name']}")
    print(f"💰 Purchase Price: ${property_data['purchase_price']:,}")
    print(f"🏦 Down Payment: ${property_data['down_payment']:,}")
    print(f"🏠 Monthly Rent: ${property_data['monthly_rent']:,}")
    print()
    
    try:
        calculator = FinancialCalculator(property_data)
        analysis = calculator.get_comprehensive_analysis()
        
        # Display key metrics
        cash_flow = analysis['cash_flow_analysis']
        profitability = analysis['profitability_ratios']
        risk = analysis['risk_metrics']
        
        print("📈 KEY INVESTMENT METRICS:")
        print(f"   • Monthly Cash Flow: ${cash_flow['monthly_cash_flow']:,.2f}")
        print(f"   • Annual Cash Flow: ${cash_flow['annual_cash_flow']:,.2f}")
        print(f"   • Cap Rate: {profitability['cap_rate']:.2f}%")
        print(f"   • Cash-on-Cash Return: {profitability['cash_on_cash_return']:.2f}%")
        print(f"   • Total ROI: {profitability['roi']:.2f}%")
        print(f"   • Debt Service Coverage: {risk['dscr']:.2f}x")
        print(f"   • Break-Even Ratio: {risk['break_even_ratio']:.1f}%")
        
        # Investment recommendation
        if cash_flow['monthly_cash_flow'] > 0 and profitability['cap_rate'] > 6:
            print("\n🎯 RECOMMENDATION: ✅ STRONG BUY")
            print("   This property shows excellent cash flow and ROI potential.")
        elif cash_flow['monthly_cash_flow'] > 0:
            print("\n🎯 RECOMMENDATION: ⚠️ CONSIDER")
            print("   Positive cash flow but moderate returns.")
        else:
            print("\n🎯 RECOMMENDATION: ❌ AVOID")
            print("   Negative cash flow - high risk investment.")
            
    except Exception as e:
        print(f"❌ Calculation error: {e}")

def demo_monte_carlo_simulation():
    """Demonstrate Monte Carlo risk modeling"""
    print("\n🎲 Monte Carlo Risk Simulation Demo")
    print("=" * 50)
    
    from app.analytics.monte_carlo import MonteCarloSimulator
    
    # Property for risk analysis
    property_data = {
        'purchase_price': 550000,
        'down_payment': 110000,
        'loan_amount': 440000,
        'interest_rate': 6.75,
        'loan_term_years': 30,
        'monthly_rent': 3200,
        'monthly_expenses': {
            'property_tax': 400,
            'insurance': 200,
            'maintenance': 250,
            'property_management': 256,
            'vacancy_allowance': 267
        }
    }
    
    # Simulation parameters
    simulation_params = {
        'simulations': 1000,  # Reduced for demo speed
        'years': 5,
        'rent_growth_range': [0.01, 0.06],    # 1-6% annual rent growth
        'expense_volatility': 0.15,            # 15% expense volatility
        'vacancy_rate_range': [0.05, 0.20],   # 5-20% vacancy rate
        'interest_rate_volatility': 0.02       # 2% interest rate volatility
    }
    
    print(f"🏘️ Analyzing: ${property_data['purchase_price']:,} investment property")
    print(f"🎲 Running {simulation_params['simulations']} scenarios over {simulation_params['years']} years...")
    print()
    
    try:
        simulator = MonteCarloSimulator(property_data, simulation_params)
        results = simulator.run_simulation()
        
        stats = results['statistics']['total_returns']
        risk_metrics = results['risk_metrics']
        summary = results['summary']
        
        print("📊 MONTE CARLO RESULTS:")
        print(f"   • Expected Total Return: ${stats['mean']:,.2f}")
        print(f"   • Best Case (95th %ile): ${stats['percentile_95']:,.2f}")
        print(f"   • Worst Case (5th %ile): ${stats['percentile_5']:,.2f}")
        print(f"   • Standard Deviation: ${stats['std']:,.2f}")
        print()
        
        print("⚠️ RISK ANALYSIS:")
        print(f"   • Probability of Loss: {risk_metrics['probability_of_loss']:.1f}%")
        print(f"   • Value at Risk (95%): ${risk_metrics['var_95']:,.2f}")
        print(f"   • Expected Shortfall: ${risk_metrics['expected_shortfall']:,.2f}")
        print(f"   • Sharpe Ratio: {risk_metrics['sharpe_ratio']:.2f}")
        print()
        
        print(f"🎯 RISK ASSESSMENT: {summary['risk_level']}")
        print(f"📋 RECOMMENDATION: {summary['recommendation']}")
        
    except Exception as e:
        print(f"❌ Simulation error: {e}")

def demo_user_interface():
    """Show how to access the user interface"""
    print("\n🌐 User Interface Demo")
    print("=" * 50)
    
    print("✅ Streamlit Frontend: http://localhost:8502")
    print("✅ Flask API Backend: http://localhost:5002")
    print()
    print("🔐 Test User Accounts:")
    print("   • investor1@example.com / password123 (Pro Tier)")
    print("   • investor2@example.com / password123 (Free Tier)")
    print("   • investor3@example.com / password123 (Enterprise)")
    print()
    print("📱 Features Available:")
    print("   • Interactive property analysis dashboard")
    print("   • Real-time financial calculations")
    print("   • Monte Carlo risk simulations")
    print("   • Professional PDF report generation")
    print("   • Portfolio tracking and management")
    print("   • User authentication and subscriptions")

def main():
    """Run the complete demo"""
    print("🏠 REAL ESTATE ANALYTICS SAAS - LIVE DEMO")
    print("🚀 Production-Ready Investment Analysis Platform")
    print("=" * 60)
    
    # Test if servers are running
    if not demo_api_functionality():
        print("\n❌ Demo requires servers to be running.")
        print("📝 Please run: python scripts/run_dev.py")
        return
    
    # Show financial calculations
    demo_financial_calculations()
    
    # Show Monte Carlo simulation
    demo_monte_carlo_simulation()
    
    # Show user interface access
    demo_user_interface()
    
    print("\n" + "=" * 60)
    print("🎉 DEMO COMPLETE - Ready for Production!")
    print("💰 This platform is ready to generate revenue through:")
    print("   • SaaS subscriptions ($29-99/month)")
    print("   • Professional reports ($5-15 each)")
    print("   • API access for developers")
    print("   • White-label solutions for firms")
    print("\n📞 Contact: Ready for investor presentations!")

if __name__ == "__main__":
    main()
