#!/bin/bash

echo "🚀 Installing Meeting Summarizer..."

# Check Python version
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11+ required"
    echo "Install with: brew install python@3.11"
    exit 1
fi

# Create venv
echo "📦 Creating virtual environment..."
python3.11 -m venv venv

# Activate
source venv/bin/activate

# Install packages
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check for .env
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    echo "OPENAI_API_KEY=your-key-here" > .env
    echo "⚠️  Please edit .env and add your OpenAI API key"
fi

# Create output directory
mkdir -p output

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API key"
echo "2. Run: python agent.py --input examples/example_input.txt"
echo "3. Check output/ folder for results"