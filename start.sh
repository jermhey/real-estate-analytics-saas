#!/bin/bash
# Real Estate Analytics SaaS - One-Command Startup Script

echo "🏠 Real Estate Analytics SaaS - Starting Application..."
echo "=================================================="

# Change to project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python scripts/quick_start.py"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if database exists
if [ ! -f "instance/real_estate.db" ]; then
    echo "🔧 Setting up database..."
    python scripts/setup_database.py
    echo "📊 Creating sample data..."
    python scripts/generate_test_data.py
fi

echo ""
echo "🚀 Starting servers..."
echo "📡 Flask API: http://localhost:5002"
echo "🌐 Streamlit App: http://localhost:8502"
echo ""
echo "🔐 Test Login Credentials:"
echo "   Email: investor1@example.com"
echo "   Password: password123"
echo ""
echo "⚠️  Press Ctrl+C to stop all servers"
echo ""

# Start the development servers
python scripts/run_dev.py
