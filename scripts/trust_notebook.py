#!/usr/bin/env python3
"""
Script to trust Jupyter notebooks.
This fixes the "notebook is not trusted" warning in Jupyter.
"""

import sys
from pathlib import Path
import subprocess

def trust_notebook(notebook_path):
    """Trust a Jupyter notebook by modifying metadata directly."""
    try:
        import json
        
        # Read notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Set trusted flag in metadata
        if 'metadata' not in notebook:
            notebook['metadata'] = {}
        notebook['metadata']['trusted'] = True
        
        # Write back
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        
        print(f"✓ Successfully trusted: {notebook_path}")
        return True
    except Exception as e:
        print(f"✗ Error trusting notebook: {e}")
        return False

if __name__ == "__main__":
    # Get project root
    project_root = Path(__file__).parent.parent
    notebook_path = project_root / "notebooks" / "01_eda_analysis.ipynb"
    
    if not notebook_path.exists():
        print(f"✗ Notebook not found: {notebook_path}")
        sys.exit(1)
    
    print("Trusting Jupyter notebook...")
    print(f"Notebook: {notebook_path}")
    print("-" * 70)
    
    if trust_notebook(notebook_path):
        print("\n✓ Notebook is now trusted. You can run it without warnings.")
        sys.exit(0)
    else:
        print("\n✗ Failed to trust notebook.")
        sys.exit(1)

