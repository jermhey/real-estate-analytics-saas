"""
Financial Calculator Module
Comprehensive real estate investment calculations
"""

import numpy as np
from typing import Dict, Any
from decimal import Decimal

class FinancialCalculator:
    """
    Production-grade financial calculator for real estate investments
    Handles all standard real estate investment metrics with high precision
    """
    
    def __init__(self, property_data):
        """
        Initialize calculator with property data
        
        Args:
            property_data: Property model instance or dictionary with property details
        """
        if hasattr(property_data, 'to_dict'):
            self.property = property_data.to_dict()
        else:
            self.property = property_data
            
        self._validate_inputs()
    
    def _validate_inputs(self):
        """Validate required property inputs"""
        required_fields = [
            'purchase_price', 'down_payment', 'loan_amount', 
            'interest_rate', 'loan_term_years', 'monthly_rent'
        ]
        
        for field in required_fields:
            if field not in self.property:
                raise ValueError(f"Missing required field: {field}")
    
    def calculate_monthly_payment(self) -> float:
        """
        Calculate monthly mortgage payment (Principal + Interest)
        Uses standard mortgage formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
        """
        principal = float(self.property['loan_amount'])
        annual_rate = float(self.property['interest_rate']) / 100
        monthly_rate = annual_rate / 12
        num_payments = self.property['loan_term_years'] * 12
        
        if monthly_rate == 0:
            return principal / num_payments
        
        monthly_payment = principal * (
            monthly_rate * (1 + monthly_rate) ** num_payments
        ) / ((1 + monthly_rate) ** num_payments - 1)
        
        return round(monthly_payment, 2)
    
    def calculate_total_monthly_expenses(self) -> float:
        """Calculate total monthly operating expenses"""
        expenses = self.property.get('monthly_expenses', {})
        
        total = sum([
            expenses.get('property_tax', 0),
            expenses.get('insurance', 0),
            expenses.get('maintenance', 0),
            expenses.get('vacancy_allowance', 0),
            expenses.get('property_management', 0),
            expenses.get('hoa_fees', 0),
            expenses.get('other_expenses', 0)
        ])
        
        return round(float(total), 2)
    
    def calculate_monthly_cash_flow(self) -> float:
        """
        Calculate monthly cash flow
        Cash Flow = Monthly Rent - Monthly Payment - Monthly Expenses
        """
        monthly_rent = float(self.property['monthly_rent'])
        monthly_payment = self.calculate_monthly_payment()
        monthly_expenses = self.calculate_total_monthly_expenses()
        
        cash_flow = monthly_rent - monthly_payment - monthly_expenses
        return round(cash_flow, 2)
    
    def calculate_annual_cash_flow(self) -> float:
        """Calculate annual cash flow"""
        return round(self.calculate_monthly_cash_flow() * 12, 2)
    
    def calculate_noi(self) -> float:
        """
        Calculate Net Operating Income (NOI)
        NOI = Annual Rental Income - Annual Operating Expenses (excluding debt service)
        """
        annual_rent = float(self.property['monthly_rent']) * 12
        annual_expenses = self.calculate_total_monthly_expenses() * 12
        
        noi = annual_rent - annual_expenses
        return round(noi, 2)
    
    def calculate_cap_rate(self) -> float:
        """
        Calculate Capitalization Rate
        Cap Rate = NOI / Purchase Price
        """
        noi = self.calculate_noi()
        purchase_price = float(self.property['purchase_price'])
        
        if purchase_price == 0:
            return 0
        
        cap_rate = (noi / purchase_price) * 100
        return round(cap_rate, 3)
    
    def calculate_cash_on_cash_return(self) -> float:
        """
        Calculate Cash-on-Cash Return
        CoC = Annual Cash Flow / Total Cash Invested
        """
        annual_cash_flow = self.calculate_annual_cash_flow()
        total_investment = float(self.property['down_payment'])
        
        # Add closing costs if available
        expenses = self.property.get('monthly_expenses', {})
        closing_costs = expenses.get('closing_costs', 0)
        total_investment += float(closing_costs)
        
        if total_investment == 0:
            return 0
        
        coc_return = (annual_cash_flow / total_investment) * 100
        return round(coc_return, 3)
    
    def calculate_roi(self) -> float:
        """
        Calculate Return on Investment (ROI)
        ROI = (Annual Cash Flow + Principal Paydown + Appreciation) / Total Investment
        Note: This simplified version excludes appreciation
        """
        annual_cash_flow = self.calculate_annual_cash_flow()
        principal_paydown = self.calculate_annual_principal_paydown()
        total_investment = float(self.property['down_payment'])
        
        # Add closing costs if available
        expenses = self.property.get('monthly_expenses', {})
        closing_costs = expenses.get('closing_costs', 0)
        total_investment += float(closing_costs)
        
        if total_investment == 0:
            return 0
        
        roi = ((annual_cash_flow + principal_paydown) / total_investment) * 100
        return round(roi, 3)
    
    def calculate_annual_principal_paydown(self) -> float:
        """Calculate annual principal paydown amount"""
        monthly_payment = self.calculate_monthly_payment()
        annual_interest = self.calculate_annual_interest_payment()
        annual_payment = monthly_payment * 12
        
        principal_paydown = annual_payment - annual_interest
        return round(principal_paydown, 2)
    
    def calculate_annual_interest_payment(self) -> float:
        """Calculate annual interest payment (first year approximation)"""
        loan_amount = float(self.property['loan_amount'])
        annual_rate = float(self.property['interest_rate']) / 100
        
        # First year interest approximation
        annual_interest = loan_amount * annual_rate
        return round(annual_interest, 2)
    
    def calculate_dscr(self) -> float:
        """
        Calculate Debt Service Coverage Ratio
        DSCR = NOI / Annual Debt Service
        """
        noi = self.calculate_noi()
        annual_debt_service = self.calculate_monthly_payment() * 12
        
        if annual_debt_service == 0:
            return 0
        
        dscr = noi / annual_debt_service
        return round(dscr, 3)
    
    def calculate_break_even_ratio(self) -> float:
        """
        Calculate Break-Even Ratio
        BER = (Monthly Payment + Monthly Expenses) / Monthly Rent
        """
        monthly_payment = self.calculate_monthly_payment()
        monthly_expenses = self.calculate_total_monthly_expenses()
        monthly_rent = float(self.property['monthly_rent'])
        
        if monthly_rent == 0:
            return 0
        
        ber = (monthly_payment + monthly_expenses) / monthly_rent
        return round(ber, 3)
    
    def calculate_gross_rent_multiplier(self) -> float:
        """
        Calculate Gross Rent Multiplier
        GRM = Purchase Price / Annual Gross Rent
        """
        purchase_price = float(self.property['purchase_price'])
        annual_rent = float(self.property['monthly_rent']) * 12
        
        if annual_rent == 0:
            return 0
        
        grm = purchase_price / annual_rent
        return round(grm, 2)
    
    def get_comprehensive_analysis(self) -> Dict[str, Any]:
        """
        Generate comprehensive financial analysis
        
        Returns:
            Dictionary containing all calculated metrics
        """
        try:
            analysis = {
                'cash_flow_analysis': {
                    'monthly_cash_flow': self.calculate_monthly_cash_flow(),
                    'annual_cash_flow': self.calculate_annual_cash_flow(),
                    'monthly_payment': self.calculate_monthly_payment(),
                    'total_monthly_expenses': self.calculate_total_monthly_expenses(),
                    'net_operating_income': self.calculate_noi()
                },
                'profitability_ratios': {
                    'cap_rate': self.calculate_cap_rate(),
                    'cash_on_cash_return': self.calculate_cash_on_cash_return(),
                    'roi': self.calculate_roi(),
                    'gross_rent_multiplier': self.calculate_gross_rent_multiplier()
                },
                'risk_metrics': {
                    'dscr': self.calculate_dscr(),
                    'break_even_ratio': self.calculate_break_even_ratio(),
                    'loan_to_value': self.property.get('loan_to_value_ratio', 0)
                },
                'loan_analysis': {
                    'annual_principal_paydown': self.calculate_annual_principal_paydown(),
                    'annual_interest_payment': self.calculate_annual_interest_payment(),
                    'loan_amount': float(self.property['loan_amount']),
                    'interest_rate': float(self.property['interest_rate'])
                }
            }
            
            return analysis
            
        except Exception as e:
            raise ValueError(f"Error calculating comprehensive analysis: {str(e)}")
    
    def sensitivity_analysis(self, variable: str, range_percent: float = 0.2) -> Dict[str, float]:
        """
        Perform sensitivity analysis on a specific variable
        
        Args:
            variable: Variable to analyze ('rent', 'expenses', 'interest_rate', etc.)
            range_percent: Percentage range for analysis (0.2 = ±20%)
        
        Returns:
            Dictionary with sensitivity results
        """
        original_value = self.property.get(variable)
        if not original_value:
            raise ValueError(f"Variable '{variable}' not found in property data")
        
        scenarios = {}
        
        # Test different scenarios
        for multiplier in [1 - range_percent, 1, 1 + range_percent]:
            # Temporarily modify the value
            original_property = self.property.copy()
            self.property[variable] = float(original_value) * multiplier
            
            # Calculate key metrics
            scenarios[f"{variable}_{int(multiplier * 100)}%"] = {
                'cash_flow': self.calculate_monthly_cash_flow(),
                'cap_rate': self.calculate_cap_rate(),
                'coc_return': self.calculate_cash_on_cash_return()
            }
            
            # Restore original value
            self.property = original_property
        
        return scenarios
