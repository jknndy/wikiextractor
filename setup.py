from setuptools import setup, find_packages
import re
import os

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
