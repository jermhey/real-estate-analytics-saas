#!/usr/bin/env python3
"""
Quick Start Setup Script
One-command setup for the Real Estate Analytics SaaS platform
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a command with proper error handling"""
    print(f"   • {description}...")
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.returncode != 0 and check:
            print(f"     ❌ Failed: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"     ❌ Error: {e}")
        return False

def main():
    """Main setup function"""
    print("🏠 Real Estate Analytics SaaS - Quick Start Setup")
    print("=" * 50)
    
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("📍 Working in:", project_root)
    
    try:
        # Step 1: Create virtual environment
        print("\n📦 Step 1: Setting up virtual environment...")
        if not Path("venv").exists():
            if not run_command([sys.executable, "-m", "venv", "venv"], "Creating virtual environment"):
                return False
            print("✅ Virtual environment created")
        else:
            print("✅ Virtual environment already exists")
        
        # Determine the correct paths
        if os.name == 'nt':  # Windows
            pip_path = "venv/Scripts/pip"
            python_path = "venv/Scripts/python"
        else:  # Unix/Linux/MacOS
            pip_path = "venv/bin/pip"
            python_path = "venv/bin/python"
        
        # Step 2: Upgrade pip
        print("\n📚 Step 2: Installing dependencies...")
        if not run_command([python_path, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip"):
            print("     ⚠️  Warning: Failed to upgrade pip, continuing...")
        
        # Step 3: Install requirements
        if not run_command([pip_path, "install", "-r", "requirements.txt"], "Installing packages"):
            print("\n     ⚠️  Some packages failed to install. Trying individual installation...")
            
            # Try installing core packages individually
            core_packages = [
                "flask==2.3.3",
                "streamlit==1.28.1", 
                "pandas==2.0.3",
                "numpy==1.24.4",
                "matplotlib==3.7.2",
                "plotly==5.17.0",
                "reportlab==4.0.4",
                "passlib==1.7.4",
                "python-dotenv==1.0.0",
                "requests==2.31.0"
            ]
            
            failed_packages = []
            for package in core_packages:
                if not run_command([pip_path, "install", package], f"Installing {package.split('==')[0]}", check=False):
                    failed_packages.append(package)
            
            if failed_packages:
                print(f"\n     ❌ Failed to install: {', '.join(failed_packages)}")
                print("     📝 You may need to install these manually later")
        
        print("✅ Dependencies installation completed")
        
        # Step 3: Setup environment file
        print("\n⚙️  Step 3: Setting up environment configuration...")
        if not Path(".env").exists():
            if Path(".env.example").exists():
                import shutil
                shutil.copy(".env.example", ".env")
                print("✅ Created .env file from template")
            else:
                # Create a basic .env file
                with open(".env", "w") as f:
                    f.write("# Real Estate Analytics SaaS Environment\n")
                    f.write("SECRET_KEY=dev-secret-key-change-in-production\n")
                    f.write("FLASK_ENV=development\n")
                    f.write("DEBUG=True\n")
                print("✅ Created basic .env file")
        else:
            print("✅ .env file already exists")
        
        # Step 4: Setup database
        print("\n🗄️  Step 4: Setting up database...")
        if not run_command([python_path, "scripts/setup_database.py"], "Setting up database"):
            print("     ⚠️  Database setup failed, you may need to run it manually")
        else:
            print("✅ Database setup completed")
        
        # Step 5: Generate test data
        print("\n🎲 Step 5: Generating test data...")
        if not run_command([python_path, "scripts/generate_test_data.py"], "Generating test data"):
            print("     ⚠️  Test data generation failed, you may need to run it manually")
        else:
            print("✅ Test data generated")
        
        # Success message
        print("\n🎉 Setup completed successfully!")
        print("\n🚀 To start the development server:")
        print("   source venv/bin/activate  # Activate virtual environment")
        print("   python scripts/run_dev.py")
        
        print("\n🌐 Then open your browser to:")
        print("   • Frontend: http://localhost:8501")
        print("   • API: http://localhost:5000")
        
        print("\n🔐 Test login credentials:")
        print("   • investor1@example.com / password123 (Pro)")
        print("   • investor2@example.com / password123 (Free)")
        print("   • investor3@example.com / password123 (Enterprise)")
        
        print("\n📖 For more information, see README.md")
        return True
        
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💡 If you encounter issues:")
        print("   1. Make sure you have Python 3.8+ installed")
        print("   2. Try running the setup steps manually")
        print("   3. Check the README.md for troubleshooting")
    sys.exit(0 if success else 1)
