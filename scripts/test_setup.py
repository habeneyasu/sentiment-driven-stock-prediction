#!/usr/bin/env python3
"""
Quick test script to verify the setup and identify potential issues.
Run this before executing the EDA notebook.
"""

import sys
from pathlib import Path

print("=" * 70)
print("SETUP VERIFICATION")
print("=" * 70)

# Check Python version
print(f"\n1. Python version: {sys.version}")

# Check required packages
print("\n2. Checking required packages...")
required_packages = [
    'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
    'nltk', 'sklearn', 'wordcloud', 'statsmodels', 'tqdm'
]

missing_packages = []
for package in required_packages:
    try:
        if package == 'sklearn':
            __import__('sklearn')
        elif package == 'plotly':
            __import__('plotly')
        else:
            __import__(package)
        print(f"   ✓ {package}")
    except ImportError:
        print(f"   ✗ {package} - MISSING")
        missing_packages.append(package)

if missing_packages:
    print(f"\n⚠ Missing packages: {', '.join(missing_packages)}")
    print("   Install with: pip install -r requirements.txt")
else:
    print("\n✓ All required packages are installed")

# Check data file
print("\n3. Checking data file...")
project_root = Path(__file__).parent.parent
data_path = project_root / "data" / "raw_analyst_ratings.csv"

if data_path.exists():
    file_size_mb = data_path.stat().st_size / (1024 * 1024)
    print(f"   ✓ Data file found: {data_path}")
    print(f"   ✓ File size: {file_size_mb:.2f} MB")
else:
    print(f"   ✗ Data file NOT found: {data_path}")
    print("   Please ensure the data file is in the correct location")

# Check project structure
print("\n4. Checking project structure...")
required_dirs = ['notebooks', 'data', 'scripts', 'src', 'tests']
for dir_name in required_dirs:
    dir_path = project_root / dir_name
    if dir_path.exists():
        print(f"   ✓ {dir_name}/")
    else:
        print(f"   ✗ {dir_name}/ - MISSING")

# Check NLTK data
print("\n5. Checking NLTK data...")
try:
    import nltk
    nltk_data_path = Path(nltk.data.find('tokenizers/punkt'))
    print(f"   ✓ NLTK data path: {nltk_data_path.parent}")
    
    # Check for required NLTK resources
    required_nltk = ['tokenizers/punkt', 'corpora/stopwords', 'corpora/wordnet']
    for resource in required_nltk:
        try:
            nltk.data.find(resource)
            print(f"   ✓ {resource}")
        except LookupError:
            print(f"   ✗ {resource} - Will be downloaded automatically")
except Exception as e:
    print(f"   ⚠ NLTK check failed: {e}")

print("\n" + "=" * 70)
if missing_packages or not data_path.exists():
    print("⚠ Some issues detected. Please fix them before running the notebook.")
    sys.exit(1)
else:
    print("✓ Setup looks good! You can now run the EDA notebook.")
    sys.exit(0)

