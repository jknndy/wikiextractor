from setuptools import setup, find_packages
import re
import os
import sys

# Try to import version, fallback to default if it fails
try:
    from wikiextractor.WikiExtractor import __version__
except ImportError:
    __version__ = '3.0.7'  # fallback version


def get_version(version):
    if re.match(r'^\d+\.\d+$', version):
        return version + '.0'
    return version

# Try to read README, fallback to empty string if it fails
try:
    with open("README.md", "r", encoding='utf-8') as fh:
        long_description = fh.read()
except (FileNotFoundError, UnicodeDecodeError):
    long_description = "A tool for extracting plain text from Wikipedia dumps"

# Check for container environment
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

setup(
    name='wikiextractor',
    version=get_version(__version__),
    author='Giuseppe Attardi',
    author_email='attardi@gmail.com',
    description='A tool for extracting plain text from Wikipedia dumps',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GNU Affero General Public License',
    install_requires=[],
    url="https://github.com/attardi/wikiextractor",
    packages=find_packages(include=["wikiextractor"]),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3'
     ],
    entry_points={
        "console_scripts": [
            "wikiextractor = wikiextractor.WikiExtractor:main",
            "extractPage = wikiextractor.extractPage:main",
            ]
        },
    python_requires='>=3.6',
)
