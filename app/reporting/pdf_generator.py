"""
PDF Report Generator
Professional-grade PDF reports for real estate investment analysis
"""

from typing import Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO
import base64
from datetime import datetime
import numpy as np
import tempfile
import os

class ReportGenerator:
    """
    Production-grade PDF report generator for real estate analysis
    Creates professional investor-ready reports with charts and analysis
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1f2937'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#374151'),
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            textColor=colors.HexColor('#4b5563'),
            fontName='Helvetica-Bold',
            leftIndent=0
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=colors.HexColor('#1f2937'),
            fontName='Helvetica'
        ))
        
        # Metric value
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            parent=self.styles['Normal'],
            fontSize=18,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#059669'),
            alignment=TA_CENTER
        ))
        
        # Risk warning
        self.styles.add(ParagraphStyle(
            name='RiskWarning',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#dc2626'),
            fontName='Helvetica-Bold',
            leftIndent=20,
            rightIndent=20,
            spaceBefore=10,
            spaceAfter=10
        ))
    
    def generate_investment_analysis_report(self, property_data: dict, analysis_data: dict, 
                                          monte_carlo_results: Optional[dict] = None) -> bytes:
        """
        Generate comprehensive investment analysis report
        
        Args:
            property_data: Property information
            analysis_data: Financial analysis results
            monte_carlo_results: Monte Carlo simulation results (optional)
        
        Returns:
            PDF report as bytes
        """
        
        # Create temporary file for PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        
        try:
            # Create document
            doc = SimpleDocTemplate(
                temp_file.name,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build report content
            story = []
            
            # Header and title
            story.extend(self._create_report_header(property_data))
            
            # Executive Summary
            story.extend(self._create_executive_summary(property_data, analysis_data))
            
            # Property Details
            story.extend(self._create_property_details(property_data))
            
            # Financial Analysis
            story.extend(self._create_financial_analysis(analysis_data))
            
            # Cash Flow Analysis
            story.extend(self._create_cash_flow_analysis(property_data, analysis_data))
            
            # Risk Analysis
            if monte_carlo_results:
                story.extend(self._create_risk_analysis(monte_carlo_results))
            
            # Investment Recommendation
            story.extend(self._create_investment_recommendation(analysis_data, monte_carlo_results))
            
            # Appendix
            story.extend(self._create_appendix())
            
            # Build PDF
            doc.build(story)
            
            # Read the PDF content
            with open(temp_file.name, 'rb') as f:
                pdf_content = f.read()
            
            return pdf_content
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
    
    def _create_report_header(self, property_data: dict) -> list:
        """Create report header with title and property info"""
        story = []
        
        # Main title
        title = f"Investment Analysis Report"
        story.append(Paragraph(title, self.styles['CustomTitle']))
        
        # Property name
        property_name = property_data.get('name', 'Property Analysis')
        story.append(Paragraph(property_name, self.styles['CustomSubtitle']))
        
        # Report date
        report_date = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(f"Report Date: {report_date}", self.styles['CustomBody']))
        
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_executive_summary(self, property_data: dict, analysis_data: dict) -> list:
        """Create executive summary section"""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        # Key metrics table
        purchase_price = property_data.get('purchase_price', 0)
        monthly_rent = property_data.get('monthly_rent', 0)
        cash_flow = analysis_data.get('cash_flow', 0)
        cap_rate = analysis_data.get('cap_rate', 0)
        coc_return = analysis_data.get('cash_on_cash_return', 0)
        
        summary_data = [
            ['Metric', 'Value'],
            ['Purchase Price', f"${purchase_price:,.0f}"],
            ['Monthly Rent', f"${monthly_rent:,.0f}"],
            ['Monthly Cash Flow', f"${cash_flow:,.0f}"],
            ['Cap Rate', f"{cap_rate:.2f}%"],
            ['Cash-on-Cash Return', f"{coc_return:.2f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Investment summary text
        investment_summary = f"""
        This analysis evaluates the investment potential of {property_data.get('name', 'the property')} 
        located at {property_data.get('address', 'the specified address')}. The property is priced at 
        ${purchase_price:,.0f} with an expected monthly rental income of ${monthly_rent:,.0f}.
        
        Key findings indicate a monthly cash flow of ${cash_flow:,.0f}, representing a 
        {coc_return:.2f}% cash-on-cash return on the initial investment. The property generates 
        a cap rate of {cap_rate:.2f}%, which should be compared against market benchmarks 
        for similar properties in the area.
        """
        
        story.append(Paragraph(investment_summary, self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_property_details(self, property_data: dict) -> list:
        """Create property details section"""
        story = []
        
        story.append(Paragraph("Property Details", self.styles['SectionHeader']))
        
        # Property information table
        property_details = [
            ['Property Information', ''],
            ['Name', property_data.get('name', 'N/A')],
            ['Address', property_data.get('address', 'N/A')],
            ['Property Type', property_data.get('property_type', 'Residential')],
            ['Purchase Price', f"${property_data.get('purchase_price', 0):,.0f}"],
            ['Down Payment', f"${property_data.get('down_payment', 0):,.0f}"],
            ['Loan Amount', f"${property_data.get('loan_amount', 0):,.0f}"],
            ['Interest Rate', f"{property_data.get('interest_rate', 0):.2f}%"],
            ['Loan Term', f"{property_data.get('loan_term_years', 0)} years"],
            ['Monthly Rent', f"${property_data.get('monthly_rent', 0):,.0f}"]
        ]
        
        details_table = Table(property_details, colWidths=[2.5*inch, 3*inch])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold')
        ]))
        
        story.append(details_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_financial_analysis(self, analysis_data: dict) -> list:
        """Create financial analysis section"""
        story = []
        
        story.append(Paragraph("Financial Analysis", self.styles['SectionHeader']))
        
        # Financial metrics
        metrics_text = f"""
        <b>Return Metrics:</b><br/>
        • Cash-on-Cash Return: {analysis_data.get('cash_on_cash_return', 0):.2f}%<br/>
        • Cap Rate: {analysis_data.get('cap_rate', 0):.2f}%<br/>
        • ROI: {analysis_data.get('roi', 0):.2f}%<br/>
        • DSCR: {analysis_data.get('dscr', 0):.2f}<br/><br/>
        
        <b>Cash Flow Analysis:</b><br/>
        • Monthly Cash Flow: ${analysis_data.get('cash_flow', 0):,.0f}<br/>
        • Annual Cash Flow: ${analysis_data.get('annual_cash_flow', 0):,.0f}<br/>
        • Net Operating Income: ${analysis_data.get('net_operating_income', 0):,.0f}<br/>
        """
        
        story.append(Paragraph(metrics_text, self.styles['CustomBody']))
        story.append(Spacer(1, 15))
        
        return story
    
    def _create_cash_flow_analysis(self, property_data: dict, analysis_data: dict) -> list:
        """Create detailed cash flow analysis"""
        story = []
        
        story.append(Paragraph("Cash Flow Analysis", self.styles['SectionHeader']))
        
        # Cash flow breakdown table
        monthly_rent = property_data.get('monthly_rent', 0)
        monthly_payment = analysis_data.get('monthly_payment', 0)
        total_expenses = analysis_data.get('total_monthly_expenses', 0)
        net_cash_flow = monthly_rent - monthly_payment - total_expenses
        
        cash_flow_data = [
            ['Cash Flow Component', 'Monthly Amount', 'Annual Amount'],
            ['Rental Income', f"${monthly_rent:,.0f}", f"${monthly_rent * 12:,.0f}"],
            ['Mortgage Payment', f"-${monthly_payment:,.0f}", f"-${monthly_payment * 12:,.0f}"],
            ['Operating Expenses', f"-${total_expenses:,.0f}", f"-${total_expenses * 12:,.0f}"],
            ['Net Cash Flow', f"${net_cash_flow:,.0f}", f"${net_cash_flow * 12:,.0f}"]
        ]
        
        cash_flow_table = Table(cash_flow_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        cash_flow_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecfdf5')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
        ]))
        
        story.append(cash_flow_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_risk_analysis(self, monte_carlo_results: dict) -> list:
        """Create risk analysis section with Monte Carlo results"""
        story = []
        
        story.append(PageBreak())
        story.append(Paragraph("Risk Analysis", self.styles['SectionHeader']))
        
        risk_metrics = monte_carlo_results.get('risk_metrics', {})
        summary = monte_carlo_results.get('summary', {})
        
        # Risk summary
        risk_text = f"""
        <b>Monte Carlo Risk Analysis Summary:</b><br/><br/>
        
        Based on {monte_carlo_results.get('simulation_parameters', {}).get('simulations', 0):,} simulations 
        over {monte_carlo_results.get('simulation_parameters', {}).get('years', 0)} years:<br/><br/>
        
        • <b>Risk Level:</b> {summary.get('risk_level', 'Unknown')}<br/>
        • <b>Probability of Loss:</b> {risk_metrics.get('probability_of_loss', 0) * 100:.1f}%<br/>
        • <b>Expected Return:</b> ${summary.get('expected_return', 0):,.0f}<br/>
        • <b>Value at Risk (5%):</b> ${risk_metrics.get('value_at_risk_5', 0):,.0f}<br/>
        • <b>Best Case Scenario (95th percentile):</b> ${summary.get('best_case_scenario', 0):,.0f}<br/>
        • <b>Worst Case Scenario (5th percentile):</b> ${summary.get('worst_case_scenario', 0):,.0f}<br/>
        """
        
        story.append(Paragraph(risk_text, self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_investment_recommendation(self, analysis_data: dict, 
                                        monte_carlo_results: Optional[dict] = None) -> list:
        """Create investment recommendation section"""
        story = []
        
        story.append(Paragraph("Investment Recommendation", self.styles['SectionHeader']))
        
        # Determine recommendation based on metrics
        cap_rate = analysis_data.get('cap_rate', 0)
        coc_return = analysis_data.get('cash_on_cash_return', 0)
        cash_flow = analysis_data.get('cash_flow', 0)
        
        if monte_carlo_results:
            prob_loss = monte_carlo_results.get('risk_metrics', {}).get('probability_of_loss', 0)
            recommendation = monte_carlo_results.get('summary', {}).get('recommendation', 'Hold')
        else:
            # Simple recommendation logic
            if cap_rate > 8 and coc_return > 10 and cash_flow > 0:
                recommendation = "Strong Buy"
                prob_loss = 0.1  # Estimated
            elif cap_rate > 6 and coc_return > 8 and cash_flow > 0:
                recommendation = "Buy"
                prob_loss = 0.2  # Estimated
            elif cash_flow > 0:
                recommendation = "Hold"
                prob_loss = 0.3  # Estimated
            else:
                recommendation = "Avoid"
                prob_loss = 0.5  # Estimated
        
        # Color-code recommendation
        if recommendation == "Strong Buy":
            rec_color = colors.HexColor('#059669')
        elif recommendation == "Buy":
            rec_color = colors.HexColor('#0891b2')
        elif recommendation == "Hold":
            rec_color = colors.HexColor('#d97706')
        else:
            rec_color = colors.HexColor('#dc2626')
        
        # Recommendation paragraph
        story.append(Paragraph(f'<font color="{rec_color}"><b>Recommendation: {recommendation}</b></font>', 
                             self.styles['MetricValue']))
        
        # Detailed recommendation text
        recommendation_text = f"""
        Based on the comprehensive financial analysis, this property receives a 
        <b>{recommendation}</b> recommendation. Key factors supporting this recommendation include:
        
        • Cap Rate of {cap_rate:.2f}% (Market benchmark comparison needed)
        • Cash-on-Cash Return of {coc_return:.2f}%
        • Monthly Cash Flow of ${cash_flow:,.0f}
        """
        
        if monte_carlo_results:
            recommendation_text += f"""
        • Risk analysis shows {prob_loss * 100:.1f}% probability of loss
        • Expected total return of ${monte_carlo_results.get('summary', {}).get('expected_return', 0):,.0f}
        """
        
        story.append(Paragraph(recommendation_text, self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_appendix(self) -> list:
        """Create appendix with disclaimers and assumptions"""
        story = []
        
        story.append(PageBreak())
        story.append(Paragraph("Appendix", self.styles['SectionHeader']))
        
        # Disclaimers
        disclaimer_text = """
        <b>Important Disclaimers:</b><br/><br/>
        
        This analysis is for informational purposes only and should not be considered as investment advice. 
        Real estate investments carry inherent risks, and past performance does not guarantee future results.
        
        <b>Key Assumptions:</b><br/>
        • Market conditions remain relatively stable
        • Property maintenance costs are estimated based on industry averages
        • Rental income projections are based on current market rates
        • Interest rates and loan terms remain constant unless otherwise specified
        
        <b>Limitations:</b><br/>
        • Analysis does not account for potential changes in local regulations
        • Property appreciation estimates are based on historical averages
        • Actual results may vary significantly from projections
        
        <b>Recommendation:</b><br/>
        Consult with qualified real estate professionals, accountants, and financial advisors 
        before making any investment decisions.
        """
        
        story.append(Paragraph(disclaimer_text, self.styles['CustomBody']))
        
        # Risk warning
        risk_warning = """
        <b>RISK WARNING:</b> Real estate investment involves substantial risk of loss. 
        Property values can decrease, rental income may be lower than projected, and 
        unexpected expenses can significantly impact returns. Never invest more than 
        you can afford to lose.
        """
        
        story.append(Paragraph(risk_warning, self.styles['RiskWarning']))
        
        return story
    
    def generate_portfolio_report(self, user_data: dict, properties_data: list, 
                                portfolio_analysis: dict) -> bytes:
        """
        Generate portfolio-level analysis report
        
        Args:
            user_data: User information
            properties_data: List of properties
            portfolio_analysis: Portfolio-level metrics
        
        Returns:
            PDF report as bytes
        """
        # Create temporary file for PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        
        try:
            # Create document
            doc = SimpleDocTemplate(temp_file.name, pagesize=letter,
                                  rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
            
            # Build story
            story = []
            
            # Title
            title = f"Portfolio Analysis Report - {user_data.get('name', 'Investor')}"
            story.append(Paragraph(title, self.styles['CustomTitle']))
            story.append(Spacer(1, 30))
            
            # Portfolio summary
            story.append(Paragraph("Portfolio Summary", self.styles['SectionHeader']))
            
            # Basic portfolio metrics
            total_value = portfolio_analysis.get('total_value', 0)
            total_equity = portfolio_analysis.get('total_equity', 0) 
            total_cash_flow = portfolio_analysis.get('total_cash_flow', 0)
            avg_cap_rate = portfolio_analysis.get('avg_cap_rate', 0)
            
            portfolio_data = [
                ['Total Portfolio Value', f'${total_value:,.2f}'],
                ['Total Equity', f'${total_equity:,.2f}'],
                ['Monthly Cash Flow', f'${total_cash_flow:,.2f}'],
                ['Average Cap Rate', f'{avg_cap_rate:.2f}%'],
                ['Number of Properties', str(len(properties_data))]
            ]
            
            portfolio_table = Table(portfolio_data, colWidths=[3*inch, 2*inch])
            portfolio_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(portfolio_table)
            story.append(Spacer(1, 30))
            
            # Individual properties summary
            story.append(Paragraph("Properties Overview", self.styles['SectionHeader']))
            
            properties_summary = [['Address', 'Value', 'Cash Flow', 'Cap Rate']]
            for prop in properties_data:
                properties_summary.append([
                    prop.get('address', 'N/A'),
                    f"${prop.get('purchase_price', 0):,.0f}",
                    f"${prop.get('monthly_cash_flow', 0):,.0f}",
                    f"{prop.get('cap_rate', 0):.1f}%"
                ])
            
            props_table = Table(properties_summary, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1*inch])
            props_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(props_table)
            
            # Build PDF
            doc.build(story)
            
            # Read file content
            with open(temp_file.name, 'rb') as f:
                pdf_content = f.read()
            
            return pdf_content
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file.name)
            except OSError:
                pass
