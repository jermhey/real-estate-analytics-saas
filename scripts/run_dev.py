#!/usr/bin/env python3
"""
Development server launcher
Starts both Flask backend and Streamlit frontend in development mode
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path
from multiprocessing import Process

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def start_flask_server():
    """Start Flask backend server"""
    print("🔥 Starting Flask backend server...")
    
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    # Change to project root directory
    os.chdir(project_root)
    
    # Start Flask app
    from app.backend.app import create_app
    app = create_app()
    app.run(
        host='127.0.0.1',
        port=5002,  # Changed to 5002 to avoid conflicts
        debug=True,
        use_reloader=False  # Disable reloader to prevent issues with multiprocessing
    )

def start_streamlit_server():
    """Start Streamlit frontend server"""
    print("🚀 Starting Streamlit frontend server...")
    
    # Change to project root directory
    os.chdir(project_root)
    
    # Start Streamlit app
    streamlit_script = project_root / "app" / "frontend" / "streamlit_app.py"
    
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        str(streamlit_script),
        "--server.port", "8502",
        "--server.address", "127.0.0.1",
        "--browser.gatherUsageStats", "false",
        "--server.headless", "true"
    ]
    
    subprocess.run(cmd)

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask',
        'streamlit', 
        'pandas',
        'plotly',
        'requests',
        'sqlalchemy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("📦 Install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def check_environment():
    """Check environment setup"""
    print("🔧 Checking environment setup...")
    
    env_file = project_root / ".env"
    
    if not env_file.exists():
        print("⚠️  .env file not found. Creating from template...")
        
        env_example = project_root / ".env.example"
        if env_example.exists():
            # Copy .env.example to .env
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✅ Created .env file from template")
            print("📝 Please update the database URL and other settings in .env")
        else:
            print("❌ .env.example file not found")
            return False
    
    return True

def main():
    """Main development server launcher"""
    print("🏠 Real Estate Analytics SaaS - Development Server")
    print("=" * 50)
    
    # Check dependencies and environment
    if not check_dependencies():
        sys.exit(1)
    
    if not check_environment():
        sys.exit(1)
    
    print("\n🚀 Starting development servers...")
    print("📡 Flask API will be available at: http://localhost:5002")
    print("🌐 Streamlit app will be available at: http://localhost:8502")
    print("\n⚠️  Make sure you've run 'python scripts/setup_database.py' first")
    print("\n🛑 Press Ctrl+C to stop all servers")
    
    # Start both servers
    flask_process = None
    streamlit_process = None
    
    try:
        # Start Flask server in background
        flask_process = Process(target=start_flask_server)
        flask_process.start()
        
        # Give Flask a moment to start
        time.sleep(2)
        
        # Start Streamlit server (this will block)
        start_streamlit_server()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        
        if flask_process and flask_process.is_alive():
            flask_process.terminate()
            flask_process.join(timeout=5)
        
        if streamlit_process and streamlit_process.is_alive():
            streamlit_process.terminate()
            streamlit_process.join(timeout=5)
        
        print("✅ Servers stopped")
        
    except Exception as e:
        print(f"❌ Error starting servers: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
