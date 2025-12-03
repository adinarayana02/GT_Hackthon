#!/bin/bash

# AI Auto-Creative Engine - Run Script
# This script sets up and runs the Streamlit application

echo "🎨 AI Auto-Creative Engine - Starting..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate  # For Mac/Linux
# venv\Scripts\activate   # For Windows (uncomment if needed)

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please update .env with your API keys"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/input
mkdir -p data/outputs/images
mkdir -p data/outputs/captions
mkdir -p data/temp
mkdir -p data/metadata

# Run Streamlit app
echo "🚀 Starting Streamlit application..."
streamlit run app.py

