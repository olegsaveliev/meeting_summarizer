#!/bin/bash

echo "🎬 Running Meeting Summarizer Examples"
echo "======================================"
echo ""

# Activate venv
source venv/bin/activate

# Example 1
echo "📝 Example 1: Basic Summary"
python agent.py --input examples/example_input.txt --quiet
echo ""

# Example 2
echo "📝 Example 2: Summary + Email + Brief"
python agent.py --input examples/example_input.txt --email --brief --quiet
echo ""

# Example 3
echo "📝 Example 3: Interactive Mode"
echo "Skipping (requires user input)"
echo ""

echo "✅ Examples complete! Check output/ folder"