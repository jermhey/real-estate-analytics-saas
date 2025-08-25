#!/usr/bin/env python3
"""
Quick functionality test for Real Estate Analytics SaaS
"""
import sys
sys.path.insert(0, '.')

from app.analytics.financial_calculator import FinancialCalculator
from app.analytics.monte_carlo import MonteCarloSimulator

def test_functionality():
    """Test core analytics functionality"""
    
    # Test property data
    property_data = {
        'purchase_price': 300000,
        'down_payment': 60000,
        'loan_amount': 240000,
        'interest_rate': 6.5,
        'loan_term_years': 30,
        'monthly_rent': 2500,
        'monthly_expenses': {
            'property_tax': 250,
            'insurance': 100,
            'maintenance': 200,
            'management': 125
        }
    }

    print('🧮 Testing Financial Calculator...')
    try:
        calculator = FinancialCalculator(property_data)
        analysis = calculator.get_comprehensive_analysis()
        
        # Get metrics from the structured analysis
        cap_rate = analysis['profitability_ratios']['cap_rate']
        cash_on_cash = analysis['profitability_ratios']['cash_on_cash_return']
        monthly_cash_flow = analysis['cash_flow_analysis']['monthly_cash_flow']
        
        print(f'   Cap Rate: {cap_rate:.2f}%')
        print(f'   Cash-on-Cash Return: {cash_on_cash:.2f}%')
        print(f'   Monthly Cash Flow: ${monthly_cash_flow:.2f}')
        print('   ✅ Financial Calculator Working')
    except Exception as e:
        print(f'   ❌ Financial Calculator Error: {e}')
        return False

    print('\n🎲 Testing Monte Carlo Simulation...')
    try:
        mc_params = {
            'simulations': 50,  # Small number for testing speed
            'years': 3,
            'rent_growth_range': [0.02, 0.05],
            'expense_volatility': 0.1
        }

        simulator = MonteCarloSimulator(property_data, mc_params)
        results = simulator.run_simulation()
        print(f'   Expected Return: ${results["statistics"]["total_returns"]["mean"]:.2f}')
        print(f'   Probability of Loss: {results["risk_metrics"]["probability_of_loss"]:.1%}')
        print(f'   Risk Level: {results["summary"]["risk_level"]}')
        print('   ✅ Monte Carlo Simulation Working')
    except Exception as e:
        print(f'   ❌ Monte Carlo Error: {e}')
        return False

    print('\n🎉 All core components tested successfully!')
    return True

if __name__ == '__main__':
    success = test_functionality()
    sys.exit(0 if success else 1)
