#!/usr/bin/env python3
"""
Production server for Real Estate Analytics SaaS
Optimized for Railway, Heroku, and other cloud platforms
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Start production server"""
    port = int(os.environ.get('PORT', 8080))
    
    # Start Streamlit app
    os.system(f"streamlit run demo.py --server.port {port} --server.address 0.0.0.0 --server.headless true")

if __name__ == "__main__":
    main()
