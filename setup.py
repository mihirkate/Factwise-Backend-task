#!/usr/bin/env python3
"""
Setup script for Team Project Planner.
Industry standard setup with environment configuration and dependency management.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def create_virtual_environment():
    """Create virtual environment if it doesn't exist."""
    venv_path = Path(".venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment created")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        sys.exit(1)

def get_pip_command():
    """Get the appropriate pip command for the virtual environment."""
    if os.name == 'nt':  # Windows
        return str(Path(".venv") / "Scripts" / "pip.exe")
    else:  # Unix/Linux/macOS
        return str(Path(".venv") / "bin" / "pip")

def install_dependencies():
    """Install project dependencies."""
    pip_cmd = get_pip_command()
    print("📚 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def setup_directories():
    """Create necessary directories."""
    directories = ["db", "out", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directory created/verified: {directory}")

def create_environment_file():
    """Create .env file with default settings."""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Environment file already exists")
        return
    
    env_content = """# Team Project Planner Environment Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Django settings
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
"""
    
    with open(env_file, "w") as f:
        f.write(env_content)
    print("✅ Environment file created")

def run_django_setup():
    """Run Django migrations and setup."""
    python_cmd = sys.executable
    if os.name == 'nt':  # Windows
        python_cmd = str(Path(".venv") / "Scripts" / "python.exe")
    else:  # Unix/Linux/macOS
        python_cmd = str(Path(".venv") / "bin" / "python")
    
    print("🔧 Running Django setup...")
    
    try:
        # Run migrations
        subprocess.run([python_cmd, "manage.py", "migrate"], check=True)
        print("✅ Django migrations completed")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Django migrations failed (this is normal for first run): {e}")

def display_usage_instructions():
    """Display usage instructions."""
    python_cmd = "python"
    if os.name == 'nt':  # Windows
        python_cmd = str(Path(".venv") / "Scripts" / "python.exe")
    else:
        python_cmd = str(Path(".venv") / "bin" / "python")
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\n📋 HOW TO RUN THE PROJECT:")
    print("\n1. Run the demo script:")
    print(f"   {python_cmd} main.py")
    print("\n2. Start the Django API server:")
    print(f"   {python_cmd} manage.py runserver")
    print("   Then visit: http://localhost:8000/api/")
    print("\n3. View API documentation:")
    print("   Check README.md for complete API documentation")
    print("\n🔧 DEVELOPMENT:")
    print(f"   Activate virtual environment: .venv/Scripts/activate (Windows) or source .venv/bin/activate (Unix)")
    print("   Install dev dependencies: pip install pytest black flake8")
    print("\n📁 PROJECT STRUCTURE:")
    print("   - db/: Data storage (JSON files)")
    print("   - out/: Exported board files")
    print("   - logs/: Application logs")
    print("   - config/: Configuration settings")
    print("   - utils/: Utility functions")
    print("="*60)

def main():
    """Main setup function."""
    print("🚀 Setting up Team Project Planner...")
    print("="*50)
    
    # Check system requirements
    check_python_version()
    
    # Setup virtual environment
    create_virtual_environment()
    
    # Install dependencies
    install_dependencies()
    
    # Setup project structure
    setup_directories()
    create_environment_file()
    
    # Django setup
    run_django_setup()
    
    # Display instructions
    display_usage_instructions()

if __name__ == "__main__":
    main()
