#!/bin/bash
# Alternative installation script for container environments

set -e

echo "Installing WikiExtractor in development mode..."

# Detect container environment
if [ -f /.dockerenv ] || [ -n "$CONTAINER" ] || [ -n "$KUBERNETES_SERVICE_HOST" ]; then
    echo "🐳 Detected container environment"
    export CONTAINER_MODE=1
fi

# Set safer defaults for containers
if [ "$CONTAINER_MODE" = "1" ]; then
    export PIP_NO_CACHE_DIR=1
    export PIP_DISABLE_PIP_VERSION_CHECK=1
    echo "📦 Using container-optimized pip settings"
fi

# Try pip install first with timeout
echo "🔄 Attempting pip install -e . (with 60s timeout)..."
if timeout 60 pip install -e .; then
    echo "✅ Successfully installed with pip install -e ."
    exit 0
fi

echo "⚠️  pip install -e . failed or timed out, trying alternative methods..."

# Alternative 1: Install without editable mode
echo "🔄 Attempting pip install . (with 60s timeout)..."
if timeout 60 pip install .; then
    echo "✅ Successfully installed with pip install ."
    exit 0
fi

# Alternative 2: Use setup.py directly
echo "🔄 Attempting setup.py develop..."
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

# Test the installation
echo "🧪 Testing installation..."
if python -c "import wikiextractor; print('Import successful')"; then
    echo "✅ Installation verified"
else
    echo "❌ Installation verification failed"
    exit 1
fi
