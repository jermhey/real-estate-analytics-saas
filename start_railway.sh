#!/bin/bash

# Railway Deployment Start Script
# This script is optimized for Railway deployment

echo "🚀 Starting Real Estate Analytics SaaS on Railway..."

# Set default port if not provided
export PORT=${PORT:-8080}

# Configure Streamlit for production
export STREAMLIT_SERVER_PORT=$PORT
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Start Streamlit
echo "🌐 Starting Streamlit server on port $PORT..."
streamlit run demo.py \
    --server.port $PORT \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false
