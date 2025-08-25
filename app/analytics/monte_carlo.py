"""
Monte Carlo Simulation Module
Advanced risk modeling for real estate investments
"""

import numpy as np
import numpy_financial as npf
import pandas as pd
from typing import Dict, List, Tuple, Any
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from app.analytics.financial_calculator import FinancialCalculator

class MonteCarloSimulator:
    """
    Production-grade Monte Carlo simulator for real estate risk analysis
    Simulates various market scenarios to assess investment risk and returns
    """
    
    def __init__(self, property_data, simulation_params: Dict[str, Any]):
        """
        Initialize Monte Carlo simulator
        
        Args:
            property_data: Property model instance or dictionary
            simulation_params: Simulation parameters and assumptions
        """
        self.calculator = FinancialCalculator(property_data)
        self.property = self.calculator.property
        self.params = self._validate_params(simulation_params)
        
    def _validate_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default simulation parameters"""
        default_params = {
            'simulations': 10000,
            'years': 10,
            'rent_growth_range': [0.02, 0.05],  # 2-5% annual rent growth
            'expense_volatility': 0.1,  # 10% standard deviation
            'vacancy_rate_range': [0.05, 0.15],  # 5-15% vacancy
            'interest_rate_volatility': 0.02,  # 2% standard deviation
            'appreciation_range': [0.02, 0.04],  # 2-4% annual appreciation
            'major_repair_probability': 0.1,  # 10% chance per year
            'major_repair_cost_range': [5000, 15000]  # $5k-$15k when it occurs
        }
        
        # Merge with provided params
        validated_params = {**default_params, **params}
        
        # Validate ranges
        for key in ['rent_growth_range', 'vacancy_rate_range', 'appreciation_range']:
            if key in validated_params and len(validated_params[key]) != 2:
                raise ValueError(f"{key} must be a list of two values [min, max]")
        
        return validated_params
    
    def run_simulation(self) -> Dict[str, Any]:
        """
        Run complete Monte Carlo simulation
        
        Returns:
            Dictionary containing simulation results and statistics
        """
        simulations = self.params['simulations']
        years = self.params['years']
        
        # Initialize result arrays
        results = {
            'annual_cash_flows': np.zeros((simulations, years)),
            'cumulative_cash_flows': np.zeros(simulations),
            'total_returns': np.zeros(simulations),
            'final_property_values': np.zeros(simulations),
            'irr_values': np.zeros(simulations),
            'worst_year_cash_flows': np.zeros(simulations),
            'best_year_cash_flows': np.zeros(simulations)
        }
        
        # Run simulations
        for i in range(simulations):
            sim_result = self._run_single_simulation(years)
            
            results['annual_cash_flows'][i] = sim_result['annual_cash_flows']
            results['cumulative_cash_flows'][i] = sim_result['cumulative_cash_flow']
            results['total_returns'][i] = sim_result['total_return']
            results['final_property_values'][i] = sim_result['final_property_value']
            results['irr_values'][i] = sim_result['irr']
            results['worst_year_cash_flows'][i] = sim_result['worst_year_cash_flow']
            results['best_year_cash_flows'][i] = sim_result['best_year_cash_flow']
        
        # Calculate statistics
        statistics = self._calculate_statistics(results)
        
        # Generate risk metrics
        risk_metrics = self._calculate_risk_metrics(results)
        
        return {
            'simulation_parameters': self.params,
            'raw_results': {k: v.tolist() if isinstance(v, np.ndarray) else v 
                          for k, v in results.items()},
            'statistics': statistics,
            'risk_metrics': risk_metrics,
            'summary': self._generate_summary(statistics, risk_metrics)
        }
    
    def _run_single_simulation(self, years: int) -> Dict[str, Any]:
        """Run a single simulation scenario"""
        
        # Initialize variables
        initial_rent = float(self.property['monthly_rent'])
        initial_expenses = self.calculator.calculate_total_monthly_expenses()
        initial_property_value = float(self.property['purchase_price'])
        monthly_payment = self.calculator.calculate_monthly_payment()
        
        annual_cash_flows = []
        current_rent = initial_rent
        current_property_value = initial_property_value
        
        for year in range(years):
            # Generate random factors for this year
            rent_growth = np.random.uniform(*self.params['rent_growth_range'])
            expense_multiplier = np.random.normal(1.0, self.params['expense_volatility'])
            vacancy_rate = np.random.uniform(*self.params['vacancy_rate_range'])
            appreciation_rate = np.random.uniform(*self.params['appreciation_range'])
            
            # Major repair event
            major_repair_cost = 0
            if np.random.random() < self.params['major_repair_probability']:
                major_repair_cost = np.random.uniform(*self.params['major_repair_cost_range'])
            
            # Update rent (compound growth)
            current_rent *= (1 + rent_growth)
            
            # Calculate effective rent (accounting for vacancy)
            effective_monthly_rent = current_rent * (1 - vacancy_rate)
            
            # Calculate expenses for this year
            current_expenses = initial_expenses * expense_multiplier
            
            # Calculate monthly cash flow
            monthly_cash_flow = effective_monthly_rent - monthly_payment - current_expenses
            
            # Calculate annual cash flow (subtract major repairs)
            annual_cash_flow = (monthly_cash_flow * 12) - major_repair_cost
            annual_cash_flows.append(annual_cash_flow)
            
            # Update property value
            current_property_value *= (1 + appreciation_rate)
        
        # Calculate metrics
        cumulative_cash_flow = sum(annual_cash_flows)
        
        # Calculate total return (cash flow + appreciation - initial investment)
        initial_investment = float(self.property['down_payment'])
        expenses = self.property.get('monthly_expenses', {})
        closing_costs = expenses.get('closing_costs', 0)
        total_investment = initial_investment + float(closing_costs)
        
        appreciation_gain = current_property_value - initial_property_value
        total_return = cumulative_cash_flow + appreciation_gain - total_investment
        
        # Calculate IRR (simplified)
        irr = self._calculate_irr(annual_cash_flows, total_investment, appreciation_gain)
        
        return {
            'annual_cash_flows': annual_cash_flows,
            'cumulative_cash_flow': cumulative_cash_flow,
            'total_return': total_return,
            'final_property_value': current_property_value,
            'irr': irr,
            'worst_year_cash_flow': min(annual_cash_flows),
            'best_year_cash_flow': max(annual_cash_flows)
        }
    
    def _calculate_irr(self, cash_flows: List[float], initial_investment: float, 
                      final_value: float) -> float:
        """Calculate Internal Rate of Return using numpy-financial"""
        try:
            # Create cash flow series (negative initial investment, annual flows, final sale)
            cf_series = [-initial_investment] + cash_flows[:-1] + [cash_flows[-1] + final_value]
            
            # Use numpy-financial's IRR calculation
            irr_result = npf.irr(cf_series)
            
            # Handle complex numbers or invalid results
            if isinstance(irr_result, complex) or np.isnan(irr_result):
                raise ValueError("IRR calculation returned invalid result")
            
            return float(irr_result) * 100
        except:
            # Fallback: simple annualized return
            total_years = len(cash_flows)
            total_return = sum(cash_flows) + final_value - initial_investment
            if total_years > 0 and initial_investment > 0:
                return ((total_return / initial_investment) ** (1/total_years) - 1) * 100
            return 0.0
    
    def _calculate_statistics(self, results: Dict[str, np.ndarray]) -> Dict[str, Any]:
        """Calculate comprehensive statistics from simulation results"""
        stats_dict = {}
        
        for metric_name, values in results.items():
            if metric_name == 'annual_cash_flows':
                continue  # Skip multi-dimensional array
                
            stats_dict[metric_name] = {
                'mean': float(np.mean(values)),
                'median': float(np.median(values)),
                'std': float(np.std(values)),
                'min': float(np.min(values)),
                'max': float(np.max(values)),
                'percentiles': {
                    '5th': float(np.percentile(values, 5)),
                    '10th': float(np.percentile(values, 10)),
                    '25th': float(np.percentile(values, 25)),
                    '75th': float(np.percentile(values, 75)),
                    '90th': float(np.percentile(values, 90)),
                    '95th': float(np.percentile(values, 95))
                }
            }
        
        return stats_dict
    
    def _calculate_risk_metrics(self, results: Dict[str, np.ndarray]) -> Dict[str, Any]:
        """Calculate risk-specific metrics"""
        cumulative_cf = results['cumulative_cash_flows']
        total_returns = results['total_returns']
        
        risk_metrics = {
            'probability_of_loss': float(np.sum(total_returns < 0) / len(total_returns)),
            'probability_of_negative_cash_flow': float(np.sum(cumulative_cf < 0) / len(cumulative_cf)),
            'value_at_risk_5': float(np.percentile(total_returns, 5)),
            'value_at_risk_10': float(np.percentile(total_returns, 10)),
            'expected_shortfall_5': float(np.mean(total_returns[total_returns <= np.percentile(total_returns, 5)])),
            'sharpe_ratio': self._calculate_sharpe_ratio(total_returns),
            'coefficient_of_variation': float(np.std(total_returns) / np.mean(total_returns)) if np.mean(total_returns) != 0 else 0
        }
        
        return risk_metrics
    
    def _calculate_sharpe_ratio(self, returns: np.ndarray, risk_free_rate: float = 0.03) -> float:
        """Calculate Sharpe ratio for the investment"""
        try:
            excess_returns = returns - risk_free_rate
            return float(np.mean(excess_returns) / np.std(excess_returns)) if np.std(excess_returns) != 0 else 0
        except:
            return 0.0
    
    def _generate_summary(self, statistics: Dict, risk_metrics: Dict) -> Dict[str, Any]:
        """Generate executive summary of simulation results"""
        total_return_stats = statistics.get('total_returns', {})
        
        # Determine risk level
        prob_loss = risk_metrics.get('probability_of_loss', 0)
        if prob_loss < 0.1:
            risk_level = "Low"
        elif prob_loss < 0.25:
            risk_level = "Moderate"
        elif prob_loss < 0.4:
            risk_level = "High"
        else:
            risk_level = "Very High"
        
        # Investment recommendation
        expected_return = total_return_stats.get('mean', 0)
        if expected_return > 50000 and prob_loss < 0.2:
            recommendation = "Strong Buy"
        elif expected_return > 20000 and prob_loss < 0.3:
            recommendation = "Buy"
        elif expected_return > 0 and prob_loss < 0.4:
            recommendation = "Hold"
        else:
            recommendation = "Avoid"
        
        return {
            'risk_level': risk_level,
            'recommendation': recommendation,
            'expected_return': expected_return,
            'probability_of_loss': prob_loss,
            'best_case_scenario': total_return_stats.get('percentiles', {}).get('95th', 0),
            'worst_case_scenario': total_return_stats.get('percentiles', {}).get('5th', 0),
            'confidence_interval_80': [
                total_return_stats.get('percentiles', {}).get('10th', 0),
                total_return_stats.get('percentiles', {}).get('90th', 0)
            ]
        }
    
    def scenario_analysis(self, scenarios: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Run specific scenario analysis
        
        Args:
            scenarios: Dictionary of scenarios with parameter modifications
        
        Returns:
            Results for each scenario
        """
        scenario_results = {}
        
        for scenario_name, scenario_params in scenarios.items():
            # Temporarily modify parameters
            original_params = self.params.copy()
            self.params.update(scenario_params)
            
            # Run smaller simulation for speed
            temp_params = self.params.copy()
            temp_params['simulations'] = min(1000, self.params['simulations'])
            self.params = temp_params
            
            # Run simulation
            results = self.run_simulation()
            scenario_results[scenario_name] = {
                'expected_return': results['statistics']['total_returns']['mean'],
                'probability_of_loss': results['risk_metrics']['probability_of_loss'],
                'value_at_risk_5': results['risk_metrics']['value_at_risk_5']
            }
            
            # Restore original parameters
            self.params = original_params
        
        return scenario_results
