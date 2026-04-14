#!/bin/bash
# AquaMetric AI - Installation Script
# This script automates the setup process

set -e

echo "=========================================="
echo "🚀 AquaMetric AI - Installation Script"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}[1/5]${NC} Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo -e "${BLUE}[2/5]${NC} Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
else
    python -m venv venv
    echo "Virtual environment created"
fi

# Activate virtual environment
echo -e "${BLUE}[3/5]${NC} Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null || venv\Scripts\activate.bat

# Install dependencies
echo -e "${BLUE}[4/5]${NC} Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
echo -e "${BLUE}[5/5]${NC} Setting up configuration..."
if [ -f ".env" ]; then
    echo "Environment file already exists"
else
    cp .env.example .env
    echo "Environment file created - update with your API key"
fi

echo ""
echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENAI_API_KEY"
echo "2. Run validation: python quickstart.py"
echo "3. Start application: python app.py"
echo "4. Open browser: http://localhost:5000"
echo ""
