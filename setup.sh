#!/bin/bash

# Payload Generator Pecha Setup Script
# This script helps you set up the project environment

echo "🚀 Setting up Payload Generator Pecha..."

# Check if Python 3.12+ is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.12 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.12"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "⚠️  Warning: Python $python_version detected. Python 3.12+ is recommended."
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "❌ requirements.txt not found. Installing basic dependencies..."
    pip install requests Levenshtein pydantic pytest python-dotenv
fi

# Setup environment file
echo "🔧 Setting up environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f "env.template" ]; then
        cp env.template .env
        echo "✅ Created .env file from template"
        echo "⚠️  Please edit .env file with your actual API configuration"
    else
        echo "⚠️  env.template not found. You'll need to create .env manually"
    fi
else
    echo "✅ .env file already exists"
fi

# Verify installation
echo "🧪 Verifying installation..."
python -c "import requests, Levenshtein, pydantic, pytest; print('✅ All dependencies installed successfully')" || {
    echo "❌ Some dependencies failed to install"
    exit 1
}

# Run tests to verify everything works
echo "🧪 Running tests to verify setup..."
python -m pytest test/test_segment_uploader_webuddhist.py -v

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Activate the virtual environment: source .venv/bin/activate"
    echo "2. Configure your .env file with actual API endpoints and credentials"
    echo "3. Prepare your text files in the required directory structure"
    echo "4. Run the segment uploader: python segment_uploader_webuddhist.py"
    echo "5. Check the README.md for detailed usage instructions"
    echo ""
    echo "📖 For help, run: cat README.md | head -50"
else
    echo "❌ Tests failed. Please check the installation."
    exit 1
fi
