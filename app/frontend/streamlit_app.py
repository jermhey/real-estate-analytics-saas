"""
Streamlit Frontend Application
Production-grade dashboard for Real Estate Analytics SaaS
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Real Estate Analytics Pro",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:5002/api"

class APIClient:
    """Client for communicating with Flask backend"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def login(self, email: str, password: str) -> tuple[dict, int]:
        """Authenticate user"""
        response = self.session.post(f"{self.base_url}/auth/login", 
                                   json={"email": email, "password": password})
        return response.json(), response.status_code
    
    def register(self, user_data: dict) -> tuple[dict, int]:
        """Register new user"""
        response = self.session.post(f"{self.base_url}/auth/register", json=user_data)
        return response.json(), response.status_code
    
    def get_properties(self) -> tuple[dict, int]:
        """Get user properties"""
        response = self.session.get(f"{self.base_url}/properties/")
        return response.json(), response.status_code
    
    def create_property(self, property_data: dict) -> tuple[dict, int]:
        """Create new property"""
        response = self.session.post(f"{self.base_url}/properties/", json=property_data)
        return response.json(), response.status_code
    
    def analyze_property(self, property_id: int) -> tuple[dict, int]:
        """Get property analysis"""
        response = self.session.get(f"{self.base_url}/properties/{property_id}/analysis")
        return response.json(), response.status_code
    
    def run_monte_carlo(self, property_id: int, params: dict) -> tuple[dict, int]:
        """Run Monte Carlo simulation"""
        response = self.session.post(f"{self.base_url}/properties/{property_id}/monte-carlo", 
                                   json=params)
        return response.json(), response.status_code
    
    def get_dashboard_data(self) -> tuple[dict, int]:
        """Get dashboard data"""
        response = self.session.get(f"{self.base_url}/dashboard")
        return response.json(), response.status_code

# Initialize API client
@st.cache_resource
def get_api_client():
    return APIClient(API_BASE_URL)

api = get_api_client()

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .positive-metric {
        background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
    }
    
    .negative-metric {
        background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
    }
    
    .warning-metric {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
    }
    
    .sidebar-content {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .success-box {
        padding: 1rem;
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .error-box {
        padding: 1rem;
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'current_property' not in st.session_state:
        st.session_state.current_property = None
    if 'properties' not in st.session_state:
        st.session_state.properties = []

def show_login_page():
    """Display login/register page"""
    st.markdown('<h1 class="main-header">🏠 Real Estate Analytics Pro</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Welcome to Professional Real Estate Investment Analysis")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                st.markdown("#### Sign In")
                email = st.text_input("Email", placeholder="your.email@example.com")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Sign In", use_container_width=True):
                    if email and password:
                        with st.spinner("Authenticating..."):
                            result, status = api.login(email, password)
                            
                        if status == 200:
                            st.session_state.authenticated = True
                            st.session_state.user_data = result.get('user', {})
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error(f"Login failed: {result.get('error', 'Unknown error')}")
                    else:
                        st.error("Please enter both email and password")
        
        with tab2:
            with st.form("register_form"):
                st.markdown("#### Create Account")
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password", 
                                       help="Must be at least 8 characters with uppercase, lowercase, and number")
                
                if st.form_submit_button("Create Account", use_container_width=True):
                    if all([first_name, last_name, email, password]):
                        user_data = {
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "password": password
                        }
                        
                        with st.spinner("Creating account..."):
                            result, status = api.register(user_data)
                        
                        if status == 201:
                            st.success("Account created successfully! Please sign in.")
                        else:
                            st.error(f"Registration failed: {result.get('error', 'Unknown error')}")
                    else:
                        st.error("Please fill in all fields")

def show_dashboard():
    """Display main dashboard"""
    st.markdown('<h1 class="main-header">📊 Investment Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.user_data.get('first_name', 'User')}!")
        
        if st.button("🔄 Refresh Data"):
            st.session_state.properties = []
            st.rerun()
        
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.session_state.properties = []
            st.rerun()
        
        st.markdown("---")
        
        # Navigation
        page = st.selectbox("Navigate to:", [
            "Dashboard Overview",
            "Add New Property", 
            "Property Analysis",
            "Portfolio View",
            "Account Settings"
        ])
    
    # Load properties if not cached
    if not st.session_state.properties:
        with st.spinner("Loading your properties..."):
            properties_data, status = api.get_properties()
            if status == 200:
                st.session_state.properties = properties_data.get('properties', [])
    
    # Route to appropriate page
    if page == "Dashboard Overview":
        show_dashboard_overview()
    elif page == "Add New Property":
        show_add_property()
    elif page == "Property Analysis":
        show_property_analysis()
    elif page == "Portfolio View":
        show_portfolio_view()
    elif page == "Account Settings":
        show_account_settings()

def show_dashboard_overview():
    """Display dashboard overview"""
    properties = st.session_state.properties
    
    if not properties:
        st.info("👋 Welcome! Start by adding your first property to begin analysis.")
        if st.button("Add Your First Property", type="primary"):
            st.session_state.page = "Add New Property"
            st.rerun()
        return
    
    # Summary metrics
    total_properties = len(properties)
    total_investment = sum(p['purchase_price'] for p in properties)
    total_monthly_rent = sum(p['monthly_rent'] for p in properties)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Properties", total_properties)
    
    with col2:
        st.metric("Total Investment", f"${total_investment:,.0f}")
    
    with col3:
        st.metric("Monthly Rent", f"${total_monthly_rent:,.0f}")
    
    with col4:
        avg_rent = total_monthly_rent / total_properties if total_properties > 0 else 0
        st.metric("Avg Rent/Property", f"${avg_rent:,.0f}")
    
    # Recent Properties
    st.markdown("### Recent Properties")
    df = pd.DataFrame(properties)
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d')
    
    st.dataframe(
        df[['name', 'address', 'purchase_price', 'monthly_rent', 'created_at']],
        use_container_width=True,
        column_config={
            "purchase_price": st.column_config.NumberColumn("Purchase Price", format="$%.0f"),
            "monthly_rent": st.column_config.NumberColumn("Monthly Rent", format="$%.0f"),
            "created_at": "Date Added"
        }
    )

def show_add_property():
    """Display add property form"""
    st.markdown("### 🏠 Add New Property")
    
    with st.form("property_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Property Details")
            name = st.text_input("Property Name*", placeholder="e.g., 123 Main Street Rental")
            address = st.text_area("Address*", placeholder="Full property address")
            purchase_price = st.number_input("Purchase Price*", min_value=0, step=1000, format="%d")
            down_payment = st.number_input("Down Payment*", min_value=0, step=1000, format="%d")
        
        with col2:
            st.markdown("#### Financing")
            loan_amount = st.number_input("Loan Amount*", min_value=0, step=1000, format="%d")
            interest_rate = st.number_input("Interest Rate (%)*", min_value=0.0, max_value=20.0, step=0.1, format="%.2f")
            loan_term = st.selectbox("Loan Term*", [15, 20, 25, 30], index=3)
            monthly_rent = st.number_input("Monthly Rent*", min_value=0, step=100, format="%d")
        
        st.markdown("#### Monthly Expenses")
        exp_col1, exp_col2, exp_col3 = st.columns(3)
        
        with exp_col1:
            property_tax = st.number_input("Property Tax", min_value=0, step=50, format="%d")
            insurance = st.number_input("Insurance", min_value=0, step=25, format="%d")
            maintenance = st.number_input("Maintenance", min_value=0, step=50, format="%d")
        
        with exp_col2:
            vacancy_allowance = st.number_input("Vacancy Allowance", min_value=0, step=25, format="%d")
            property_mgmt = st.number_input("Property Management", min_value=0, step=25, format="%d")
            hoa_fees = st.number_input("HOA Fees", min_value=0, step=25, format="%d")
        
        with exp_col3:
            other_expenses = st.number_input("Other Expenses", min_value=0, step=25, format="%d")
            closing_costs = st.number_input("Closing Costs (one-time)", min_value=0, step=500, format="%d")
        
        submitted = st.form_submit_button("Add Property", type="primary", use_container_width=True)
        
        if submitted:
            if all([name, address, purchase_price, down_payment, loan_amount, interest_rate, monthly_rent]):
                property_data = {
                    "name": name,
                    "address": address,
                    "purchase_price": purchase_price,
                    "down_payment": down_payment,
                    "loan_amount": loan_amount,
                    "interest_rate": interest_rate,
                    "loan_term_years": loan_term,
                    "monthly_rent": monthly_rent,
                    "monthly_expenses": {
                        "property_tax": property_tax,
                        "insurance": insurance,
                        "maintenance": maintenance,
                        "vacancy_allowance": vacancy_allowance,
                        "property_management": property_mgmt,
                        "hoa_fees": hoa_fees,
                        "other_expenses": other_expenses,
                        "closing_costs": closing_costs
                    }
                }
                
                with st.spinner("Creating property..."):
                    result, status = api.create_property(property_data)
                
                if status == 201:
                    st.success("Property added successfully!")
                    st.session_state.properties = []  # Force refresh
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Failed to add property: {result.get('error', 'Unknown error')}")
            else:
                st.error("Please fill in all required fields marked with *")

def show_property_analysis():
    """Display property analysis page"""
    st.markdown("### 📈 Property Analysis")
    
    properties = st.session_state.properties
    
    if not properties:
        st.info("No properties found. Please add a property first.")
        return
    
    # Property selection
    property_names = [f"{p['name']} - ${p['purchase_price']:,.0f}" for p in properties]
    selected_idx = st.selectbox("Select Property for Analysis", range(len(property_names)), 
                               format_func=lambda x: property_names[x])
    
    if selected_idx is not None:
        selected_property = properties[selected_idx]
        property_id = selected_property['id']
        
        tab1, tab2, tab3 = st.tabs(["📊 Financial Analysis", "🎲 Monte Carlo", "📋 Scenarios"])
        
        with tab1:
            show_financial_analysis(property_id, selected_property)
        
        with tab2:
            show_monte_carlo_analysis(property_id, selected_property)
        
        with tab3:
            show_scenario_analysis(property_id, selected_property)

def show_financial_analysis(property_id: int, property_data: dict):
    """Display financial analysis for selected property"""
    
    if st.button("🔄 Run Analysis", type="primary"):
        with st.spinner("Calculating financial metrics..."):
            result, status = api.analyze_property(property_id)
        
        if status == 200:
            analysis = result['analysis']
            
            # Key Metrics
            st.markdown("#### 📊 Key Financial Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                cash_flow = analysis['cash_flow']
                color = "positive-metric" if cash_flow > 0 else "negative-metric"
                st.markdown(f"""
                <div class="metric-card {color}">
                    <h3>${cash_flow:,.0f}</h3>
                    <p>Monthly Cash Flow</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                cap_rate = analysis['cap_rate']
                color = "positive-metric" if cap_rate > 6 else "warning-metric" if cap_rate > 4 else "negative-metric"
                st.markdown(f"""
                <div class="metric-card {color}">
                    <h3>{cap_rate:.2f}%</h3>
                    <p>Cap Rate</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                coc_return = analysis['cash_on_cash_return']
                color = "positive-metric" if coc_return > 8 else "warning-metric" if coc_return > 5 else "negative-metric"
                st.markdown(f"""
                <div class="metric-card {color}">
                    <h3>{coc_return:.2f}%</h3>
                    <p>Cash-on-Cash Return</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                dscr = analysis['dscr']
                color = "positive-metric" if dscr > 1.25 else "warning-metric" if dscr > 1.0 else "negative-metric"
                st.markdown(f"""
                <div class="metric-card {color}">
                    <h3>{dscr:.2f}</h3>
                    <p>DSCR</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Detailed Breakdown
            st.markdown("#### 💰 Cash Flow Breakdown")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Monthly Income**")
                st.write(f"Rental Income: ${property_data['monthly_rent']:,.0f}")
                
                st.markdown("**Monthly Expenses**")
                monthly_payment = analysis['monthly_payment']
                total_expenses = analysis['total_monthly_expenses']
                st.write(f"Mortgage Payment: ${monthly_payment:,.0f}")
                st.write(f"Operating Expenses: ${total_expenses:,.0f}")
                st.write(f"**Total Expenses: ${monthly_payment + total_expenses:,.0f}**")
                
                net_income = property_data['monthly_rent'] - monthly_payment - total_expenses
                st.write(f"**Net Monthly Income: ${net_income:,.0f}**")
            
            with col2:
                # Create pie chart of expenses
                expenses_data = {
                    'Mortgage Payment': monthly_payment,
                    'Operating Expenses': total_expenses
                }
                
                fig = px.pie(values=list(expenses_data.values()), 
                           names=list(expenses_data.keys()),
                           title="Monthly Expense Breakdown")
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")

def show_monte_carlo_analysis(property_id: int, property_data: dict):
    """Display Monte Carlo simulation interface and results"""
    st.markdown("#### 🎲 Monte Carlo Risk Analysis")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Simulation Parameters**")
        simulations = st.slider("Number of Simulations", 1000, 10000, 5000, step=1000)
        years = st.slider("Analysis Period (Years)", 5, 20, 10)
        
        st.markdown("**Market Assumptions**")
        rent_growth_min = st.slider("Min Annual Rent Growth (%)", 0.0, 10.0, 2.0, 0.5)
        rent_growth_max = st.slider("Max Annual Rent Growth (%)", rent_growth_min, 15.0, 5.0, 0.5)
        
        expense_volatility = st.slider("Expense Volatility (%)", 5.0, 25.0, 10.0, 2.5)
        
        vacancy_min = st.slider("Min Vacancy Rate (%)", 0.0, 20.0, 5.0, 1.0)
        vacancy_max = st.slider("Max Vacancy Rate (%)", vacancy_min, 30.0, 15.0, 1.0)
        
        if st.button("🚀 Run Monte Carlo Simulation", type="primary"):
            params = {
                "simulations": simulations,
                "years": years,
                "rent_growth_range": [rent_growth_min/100, rent_growth_max/100],
                "expense_volatility": expense_volatility/100,
                "vacancy_rate_range": [vacancy_min/100, vacancy_max/100]
            }
            
            with st.spinner("Running simulation... This may take a moment."):
                result, status = api.run_monte_carlo(property_id, params)
            
            if status == 200:
                st.session_state.monte_carlo_results = result
                st.success("Simulation complete!")
            else:
                st.error(f"Simulation failed: {result.get('error', 'Unknown error')}")
    
    with col2:
        if hasattr(st.session_state, 'monte_carlo_results'):
            results = st.session_state.monte_carlo_results
            show_monte_carlo_results(results)

def show_monte_carlo_results(results: dict):
    """Display Monte Carlo simulation results"""
    stats = results['statistics']
    risk_metrics = results['risk_metrics']
    summary = results['summary']
    
    # Summary Cards
    st.markdown("**Simulation Results**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        expected_return = stats['total_returns']['mean']
        st.metric("Expected Total Return", f"${expected_return:,.0f}")
    
    with col2:
        prob_loss = risk_metrics['probability_of_loss'] * 100
        st.metric("Probability of Loss", f"{prob_loss:.1f}%")
    
    with col3:
        st.metric("Risk Level", summary['risk_level'])
    
    # Distribution Chart
    returns_data = results['raw_results']['total_returns']
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=returns_data, nbinsx=50, name="Total Returns"))
    fig.add_vline(x=expected_return, line_dash="dash", line_color="red", 
                 annotation_text="Expected Return")
    fig.update_layout(title="Distribution of Total Returns", 
                     xaxis_title="Total Return ($)", 
                     yaxis_title="Frequency")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk Metrics Table
    st.markdown("**Risk Analysis**")
    
    risk_data = {
        "Metric": ["Value at Risk (5%)", "Value at Risk (10%)", "Best Case (95th %ile)", "Worst Case (5th %ile)"],
        "Value": [
            f"${risk_metrics['value_at_risk_5']:,.0f}",
            f"${risk_metrics['value_at_risk_10']:,.0f}",
            f"${stats['total_returns']['percentiles']['95th']:,.0f}",
            f"${stats['total_returns']['percentiles']['5th']:,.0f}"
        ]
    }
    
    st.table(pd.DataFrame(risk_data))
    
    # Investment Recommendation
    recommendation = summary['recommendation']
    if recommendation == "Strong Buy":
        st.success(f"🎯 **Recommendation: {recommendation}**")
    elif recommendation == "Buy":
        st.info(f"👍 **Recommendation: {recommendation}**")
    elif recommendation == "Hold":
        st.warning(f"⚠️ **Recommendation: {recommendation}**")
    else:
        st.error(f"❌ **Recommendation: {recommendation}**")

def show_scenario_analysis(property_id: int, property_data: dict):
    """Display scenario analysis interface"""
    st.markdown("#### 📋 Scenario Analysis")
    st.info("Compare different market scenarios to understand potential outcomes.")
    
    # Pre-defined scenarios
    scenarios = {
        "Base Case": "Current market conditions",
        "Economic Downturn": "Reduced rent growth, higher vacancy",
        "Market Boom": "High rent growth, low vacancy", 
        "Interest Rate Spike": "Significant interest rate increases",
        "Maintenance Heavy": "Higher than normal maintenance costs"
    }
    
    selected_scenario = st.selectbox("Select Scenario", list(scenarios.keys()))
    st.write(f"**{selected_scenario}**: {scenarios[selected_scenario]}")
    
    if st.button(f"Analyze {selected_scenario}", type="primary"):
        st.info("Scenario analysis feature coming soon!")

def show_portfolio_view():
    """Display portfolio overview"""
    st.markdown("### 📊 Portfolio Overview")
    
    properties = st.session_state.properties
    
    if not properties:
        st.info("No properties in your portfolio yet.")
        return
    
    # Portfolio summary
    df = pd.DataFrame(properties)
    
    total_value = df['purchase_price'].sum()
    total_rent = df['monthly_rent'].sum()
    avg_price = df['purchase_price'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Portfolio Value", f"${total_value:,.0f}")
    with col2:
        st.metric("Total Monthly Rent", f"${total_rent:,.0f}")
    with col3:
        st.metric("Average Property Value", f"${avg_price:,.0f}")
    with col4:
        annual_rent = total_rent * 12
        portfolio_yield = (annual_rent / total_value * 100) if total_value > 0 else 0
        st.metric("Portfolio Yield", f"{portfolio_yield:.2f}%")
    
    # Property comparison chart
    st.markdown("#### Property Comparison")
    
    fig = make_subplots(rows=1, cols=2, 
                       subplot_titles=("Purchase Price", "Monthly Rent"))
    
    fig.add_trace(go.Bar(x=df['name'], y=df['purchase_price'], name="Purchase Price"), row=1, col=1)
    fig.add_trace(go.Bar(x=df['name'], y=df['monthly_rent'], name="Monthly Rent"), row=1, col=2)
    
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.markdown("#### Portfolio Details")
    st.dataframe(df[['name', 'address', 'purchase_price', 'monthly_rent']], use_container_width=True)

def show_account_settings():
    """Display account settings page"""
    st.markdown("### ⚙️ Account Settings")
    
    user_data = st.session_state.user_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Profile Information")
        st.write(f"**Name:** {user_data.get('first_name', '')} {user_data.get('last_name', '')}")
        st.write(f"**Email:** {user_data.get('email', '')}")
        st.write(f"**Subscription:** {user_data.get('subscription_tier', 'free').title()}")
        
        if st.button("Update Profile"):
            st.info("Profile update feature coming soon!")
    
    with col2:
        st.markdown("#### Subscription")
        
        current_tier = user_data.get('subscription_tier', 'free')
        
        if current_tier == 'free':
            st.info("**Free Plan**\n- 1 Property\n- Basic Analysis\n- Limited Reports")
            if st.button("Upgrade to Pro", type="primary"):
                st.info("Subscription upgrade coming soon!")
        elif current_tier == 'pro':
            st.success("**Pro Plan**\n- 10 Properties\n- Full Analysis\n- Unlimited Reports")
        else:
            st.success("**Enterprise Plan**\n- Unlimited Properties\n- Advanced Features\n- Priority Support")

def main():
    """Main application entry point"""
    apply_custom_css()
    initialize_session_state()
    
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
