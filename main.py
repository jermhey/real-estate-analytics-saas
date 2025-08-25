#!/usr/bin/env python3
"""
Real Estate Analytics SaaS - Main Application Entry Point
Streamlit Cloud deployment entry point
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set page config first
st.set_page_config(
    page_title="Real Estate Analytics Pro",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application entry point"""
    
    # Import and run the Streamlit app
    try:
        from app.frontend.streamlit_app import main as run_app
        run_app()
    except ImportError as e:
        st.error(f"Failed to import application: {e}")
        st.info("Please ensure all dependencies are installed.")
        
        # Fallback simple demo
        st.title("🏠 Real Estate Analytics SaaS")
        st.markdown("""
        ## Welcome to Real Estate Analytics Pro
        
        **Your Intelligent Real Estate Investment Platform**
        
        ### 🚀 Key Features:
        - **Smart Property Analysis**: AI-powered investment recommendations
        - **Risk Assessment**: Comprehensive market risk modeling
        - **Portfolio Management**: Track and optimize your real estate investments
        - **Market Intelligence**: Real-time market data and trends
        
        ### 📊 Platform Capabilities:
        - Analyze 20+ property metrics instantly
        - Generate professional investment reports
        - Risk-adjusted ROI calculations
        - Market comparison analysis
        
        ---
        *Platform currently in setup mode. Please check back soon for full functionality.*
        """)

if __name__ == "__main__":
    main()
