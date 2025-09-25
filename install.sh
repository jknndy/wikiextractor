#!/bin/bash
# Alternative installation script for container environments

set -e

echo "Installing WikiExtractor in development mode..."

# Try pip install first
if pip install -e .; then
    echo "✅ Successfully installed with pip install -e ."
    exit 0
fi

echo "⚠️  pip install -e . failed, trying alternative methods..."

# Alternative 1: Install without editable mode
if pip install .; then
    echo "✅ Successfully installed with pip install ."
    exit 0
fi

# Alternative 2: Use setup.py directly
if python setup.py develop; then
    echo "✅ Successfully installed with setup.py develop"
    exit 0
fi

# Alternative 3: Just add to Python path (for development)
echo "📁 Adding current directory to Python path..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "export PYTHONPATH=\"\${PYTHONPATH}:$(pwd)\"" >> ~/.bashrc

echo "✅ WikiExtractor available via PYTHONPATH"
echo "You can now run: python -m wikiextractor.WikiExtractor --help"
