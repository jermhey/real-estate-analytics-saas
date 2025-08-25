# 🌐 Web Deployment Guide - Real Estate Analytics SaaS
## Get Your Platform Live on the Internet

---

## 🎯 **DEPLOYMENT OVERVIEW**

Your Real Estate Analytics SaaS platform is **production-ready** and can be deployed to the web immediately. I'll show you **5 deployment options** ranging from beginner-friendly to enterprise-grade.

---

## 🚀 **QUICK DEPLOYMENT OPTIONS**

### **Option 1: Streamlit Community Cloud (FREE & FASTEST)**
**⏱️ Time to deploy: 5 minutes**
**💰 Cost: FREE**
**🎯 Best for: MVP testing, demos**

#### Steps:
1. **Push your code to GitHub**:
   ```bash
   cd "/Users/jeremy/Desktop/DSCI 112 Project/real_estate_saas"
   git init
   git add .
   git commit -m "Initial commit - Real Estate Analytics SaaS"
   git branch -M main
   git remote add origin https://github.com/yourusername/real-estate-saas.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file: `app/frontend/streamlit_app.py`
   - Click "Deploy"

3. **Result**: Your app will be live at `https://yourusername-real-estate-saas-app-frontend-streamlit-app.streamlit.app`

**⚠️ Limitation**: Frontend only - no Flask backend. Good for demos but limited functionality.

---

### **Option 2: Railway (RECOMMENDED FOR BEGINNERS)**
**⏱️ Time to deploy: 15 minutes**
**💰 Cost: $0-5/month**
**🎯 Best for: Full-stack deployment with minimal setup**

#### Steps:
1. **Prepare for Railway**:
   ```bash
   cd "/Users/jeremy/Desktop/DSCI 112 Project/real_estate_saas"
   ```

2. **Create Railway configuration**:
   Create `railway.json`:
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python scripts/run_production.py",
       "restartPolicyType": "ON_FAILURE"
     }
   }
   ```

3. **Deploy to Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variables:
     - `SECRET_KEY`: your-secret-key-here
     - `FLASK_ENV`: production
   - Deploy

4. **Result**: Live at `https://your-app.up.railway.app`

---

### **Option 3: DigitalOcean App Platform**
**⏱️ Time to deploy: 30 minutes**
**💰 Cost: $5-12/month**
**🎯 Best for: Professional deployment with database**

#### Steps:
1. **Create DigitalOcean account** at [digitalocean.com](https://digitalocean.com)

2. **Create App**:
   - Go to Apps → Create App
   - Connect GitHub repository
   - Configure services:

   **Backend Service:**
   - Source: Your repository
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `python scripts/run_production.py`
   - Environment Variables:
     ```
     SECRET_KEY=your-production-secret-key
     FLASK_ENV=production
     DATABASE_URL=${db.DATABASE_URL}
     ```

   **Database:**
   - Add PostgreSQL database
   - Name: `real-estate-db`

3. **Deploy**: Click "Create Resources"

4. **Result**: Live at `https://your-app-name.ondigitalocean.app`

---

### **Option 4: AWS (ENTERPRISE-GRADE)**
**⏱️ Time to deploy: 1-2 hours**
**💰 Cost: $10-50/month**
**🎯 Best for: Scalable production deployment**

#### Steps:
1. **Create AWS account** at [aws.amazon.com](https://aws.amazon.com)

2. **Deploy with Elastic Beanstalk**:
   ```bash
   # Install EB CLI
   pip install awsebcli
   
   # Initialize EB application
   cd "/Users/jeremy/Desktop/DSCI 112 Project/real_estate_saas"
   eb init
   # Choose region, platform (Python), etc.
   
   # Create environment
   eb create production
   
   # Deploy
   eb deploy
   ```

3. **Configure RDS Database**:
   - Go to AWS RDS
   - Create PostgreSQL database
   - Update environment variables in EB

4. **Result**: Live at `https://your-app.region.elasticbeanstalk.com`

---

### **Option 5: Docker + VPS (FULL CONTROL)**
**⏱️ Time to deploy: 2-3 hours**
**💰 Cost: $5-20/month**
**🎯 Best for: Maximum control and customization**

#### Steps:
1. **Get a VPS** (DigitalOcean Droplet, Linode, Vultr)

2. **Setup server**:
   ```bash
   # SSH into your server
   ssh root@your-server-ip
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo usermod -aG docker $USER
   
   # Clone your repository
   git clone https://github.com/yourusername/real-estate-saas.git
   cd real-estate-saas
   ```

3. **Deploy with Docker Compose**:
   ```bash
   # Set production environment variables
   export SECRET_KEY="your-production-secret-key"
   export FLASK_ENV="production"
   
   # Deploy
   docker-compose up -d --build
   ```

4. **Setup domain** (optional):
   - Point your domain to server IP
   - Setup SSL with Let's Encrypt

---

## 🔧 **PRE-DEPLOYMENT SETUP**

Before deploying, let's prepare your application:

<function_calls>
<invoke name="create_file">
<parameter name="content">#!/usr/bin/env python3
"""
Production deployment script
Prepares and runs the Real Estate Analytics SaaS platform for production
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_production_environment():
    """Setup production environment variables"""
    print("🔧 Setting up production environment...")
    
    # Production environment variables
    production_env = {
        'FLASK_ENV': 'production',
        'SECRET_KEY': os.getenv('SECRET_KEY', 'change-this-in-production-' + os.urandom(16).hex()),
        'DATABASE_URL': os.getenv('DATABASE_URL', 'sqlite:///production.db'),
        'PORT': os.getenv('PORT', '8000'),
    }
    
    # Set environment variables
    for key, value in production_env.items():
        os.environ[key] = value
        print(f"   ✅ {key}: {'*' * min(len(value), 20)}")
    
    return production_env

def start_production_server():
    """Start production server"""
    print("🚀 Starting production server...")
    
    # Add project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # Import after path setup
    from app.backend.app import create_app
    
    # Create Flask app
    app = create_app()
    
    # Get port from environment
    port = int(os.getenv('PORT', 8000))
    
    print(f"🌐 Server starting on port {port}")
    print(f"🏠 Real Estate Analytics SaaS - Production Mode")
    print("="*50)
    
    # Run with Gunicorn if available, otherwise use Flask dev server
    try:
        import gunicorn
        # Use Gunicorn for production
        subprocess.run([
            'gunicorn',
            '--bind', f'0.0.0.0:{port}',
            '--workers', '4',
            '--timeout', '120',
            '--worker-class', 'sync',
            '--access-logfile', '-',
            '--error-logfile', '-',
            'app.backend.app:create_app()'
        ])
    except ImportError:
        print("⚠️ Gunicorn not found, using Flask dev server")
        app.run(host='0.0.0.0', port=port, debug=False)

def main():
    """Main production deployment function"""
    print("🏠 Real Estate Analytics SaaS - Production Deployment")
    print("="*60)
    
    # Setup environment
    env = setup_production_environment()
    
    # Start server
    start_production_server()

if __name__ == "__main__":
    main()
