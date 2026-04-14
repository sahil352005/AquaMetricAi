#!/usr/bin/env python
"""
AquaMetric AI - Quick Start Guide & Validation Script

This script helps you set up and validate the AquaMetric AI system.
Run this before starting the application.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_python_version():
    """Check if Python version is 3.10+."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 10:
        print("✓ Python version OK")
        return True
    else:
        print("✗ Python 3.10+ required")
        return False


def check_env_file():
    """Check if .env file exists and has API key."""
    print_header("Checking Environment Configuration")
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists():
        print(f"✗ .env file not found")
        if env_example_path.exists():
            print(f"  Creating .env from .env.example...")
            with open(env_example_path, 'r') as f:
                content = f.read()
            with open(env_path, 'w') as f:
                f.write(content)
            print(f"✓ Created .env file (update OPENAI_API_KEY)")
        return False
    else:
        print(f"✓ .env file found")
        
        # Check for API key
        with open(env_path, 'r') as f:
            content = f.read()
        
        if 'OPENAI_API_KEY=' in content:
            api_key = content.split('OPENAI_API_KEY=')[1].split('\n')[0].strip()
            if api_key and api_key != 'your_api_key_here':
                print(f"✓ OPENAI_API_KEY configured")
                return True
            else:
                print(f"✗ OPENAI_API_KEY is empty or default")
                return False
        else:
            print(f"✗ OPENAI_API_KEY not found in .env")
            return False


def check_directories():
    """Check if required directories exist."""
    print_header("Checking Directory Structure")
    
    required_dirs = [
        'backend',
        'templates',
        'static',
        'data',
        'vectorstore'
    ]
    
    all_ok = True
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"✓ {dir_name}/ found")
        else:
            print(f"✗ {dir_name}/ not found")
            all_ok = False
    
    return all_ok


def check_files():
    """Check if required files exist."""
    print_header("Checking Required Files")
    
    required_files = [
        'app.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        'templates/index.html',
        'static/style.css',
        'static/script.js',
        'backend/pdf_extractor.py',
        'backend/table_extractor.py',
        'backend/data_processor.py',
        'backend/rag_pipeline.py',
        'backend/agent.py',
        'data/water_scarcity.csv'
    ]
    
    all_ok = True
    for file_name in required_files:
        if os.path.isfile(file_name):
            print(f"✓ {file_name}")
        else:
            print(f"✗ {file_name} not found")
            all_ok = False
    
    return all_ok


def check_dependencies():
    """Check if required Python packages are installed."""
    print_header("Checking Python Dependencies")
    
    required_packages = [
        'flask',
        'langchain',
        'openai',
        'chromadb',
        'pymupdf',
        'camelot',
        'pandas',
        'dotenv'
    ]
    
    all_ok = True
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} not installed")
            all_ok = False
    
    return all_ok


def install_dependencies():
    """Ask user if they want to install missing dependencies."""
    print_header("Installing Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False


def create_sample_env():
    """Create sample .env file if it doesn't exist."""
    if not os.path.exists('.env'):
        print("Creating .env from template...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✓ .env created (update with your API key)")


def run_validation():
    """Run complete validation."""
    print_header("AQUAMETRIC AI - System Validation")
    
    results = {
        'python': check_python_version(),
        'env': check_env_file(),
        'dirs': check_directories(),
        'files': check_files(),
        'deps': check_dependencies(),
    }
    
    print_header("Validation Summary")
    
    all_ok = all(results.values())
    
    status_map = {True: '✓ PASS', False: '✗ FAIL'}
    for check, result in results.items():
        print(f"{status_map[result]} - {check.upper()}")
    
    if not all_ok:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        
        if not results['deps']:
            print("\n💡 Tip: Run the following to install dependencies:")
            print("   pip install -r requirements.txt")
        
        if not results['env']:
            print("\n💡 Tip: Update your .env file with:")
            print("   export OPENAI_API_KEY='your-api-key-here'")
        
        return False
    else:
        print("\n✅ All checks passed! Ready to start.")
        print("\n💡 To start the application, run:")
        print("   python app.py")
        print("\nThen open your browser to: http://localhost:5000")
        return True


def main():
    """Main entry point."""
    print("\n" + "🚀 " + "AQUAMETRIC AI - Quick Start".center(66) + " 🚀")
    
    # Create .env if missing
    create_sample_env()
    
    # Run validation
    success = run_validation()
    
    if success:
        print("\n📚 Documentation: See README.md for detailed information")
        print("🔗 API Docs: See README.md for API endpoint documentation")
        print("📝 Sample Data: Check sample_data.py for test data")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
