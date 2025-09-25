#!/usr/bin/env python3
"""
Container-compatible installation script for WikiExtractor.
This script provides multiple fallback methods for installation in container environments.
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def is_container_environment():
    """Detect if we're running in a container environment"""
    container_indicators = [
        '/.dockerenv',  # Docker
        '/proc/1/cgroup',  # Check cgroup for container indicators
        os.environ.get('CONTAINER', ''),  # Common container env var
        os.environ.get('KUBERNETES_SERVICE_HOST', ''),  # Kubernetes
    ]
    
    # Check for Docker
    if os.path.exists('/.dockerenv'):
        return True
    
    # Check cgroup (if available)
    try:
        with open('/proc/1/cgroup', 'r') as f:
            content = f.read()
            if 'docker' in content or 'containerd' in content or 'kubepods' in content:
                return True
    except (FileNotFoundError, PermissionError):
        pass
    
    # Check environment variables
    if any(os.environ.get(var) for var in ['CONTAINER', 'KUBERNETES_SERVICE_HOST']):
        return True
    
    return False

def run_with_timeout(cmd, timeout=60):
    """Run a command with timeout"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", f"Command timed out after {timeout} seconds"
    except Exception as e:
        return False, "", str(e)

def add_to_pythonpath():
    """Add current directory to Python path"""
    current_dir = str(Path.cwd())
    pythonpath = os.environ.get('PYTHONPATH', '')
    
    if current_dir not in pythonpath:
        if pythonpath:
            new_pythonpath = f"{pythonpath}:{current_dir}"
        else:
            new_pythonpath = current_dir
        
        os.environ['PYTHONPATH'] = new_pythonpath
        print(f"✅ Added {current_dir} to PYTHONPATH")
        return True
    return False

def test_import():
    """Test if the package can be imported"""
    try:
        import wikiextractor
        print("✅ Package import successful")
        return True
    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        return False

def main():
    print("🚀 WikiExtractor Container Installation Script")
    print("=" * 50)
    
    # Detect container environment
    if is_container_environment():
        print("🐳 Detected container environment")
        os.environ['PIP_NO_CACHE_DIR'] = '1'
        os.environ['PIP_DISABLE_PIP_VERSION_CHECK'] = '1'
    
    # Method 1: pip install -e .
    print("\n🔄 Method 1: pip install -e . (60s timeout)")
    success, stdout, stderr = run_with_timeout("pip install -e .", 60)
    if success:
        print("✅ Successfully installed with pip install -e .")
        if test_import():
            return 0
    else:
        print(f"❌ Failed: {stderr}")
    
    # Method 2: pip install .
    print("\n🔄 Method 2: pip install . (60s timeout)")
    success, stdout, stderr = run_with_timeout("pip install .", 60)
    if success:
        print("✅ Successfully installed with pip install .")
        if test_import():
            return 0
    else:
        print(f"❌ Failed: {stderr}")
    
    # Method 3: setup.py develop
    print("\n🔄 Method 3: python setup.py develop")
    success, stdout, stderr = run_with_timeout("python setup.py develop", 30)
    if success:
        print("✅ Successfully installed with setup.py develop")
        if test_import():
            return 0
    else:
        print(f"❌ Failed: {stderr}")
    
    # Method 4: Add to Python path
    print("\n🔄 Method 4: Add to Python path")
    if add_to_pythonpath():
        if test_import():
            print("✅ Package available via PYTHONPATH")
            print("💡 Note: This is a temporary installation. Add to your shell profile for persistence.")
            return 0
    
    print("\n❌ All installation methods failed")
    print("💡 Try running the commands manually or check for dependency issues")
    return 1

if __name__ == "__main__":
    sys.exit(main())
