#!/bin/bash
# Quick start script for Loop Box Financial Dashboard

echo "🔄 Starting Loop Box Financial Dashboard..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "⚠️  Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Run the dashboard
streamlit run app.py
