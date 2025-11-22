# Project Manifest

This file lists all important files in the project and their purposes.

## Core Documentation

- `README.md` - Main project documentation and setup instructions
- `CHANGELOG.md` - Version history and changes
- `PROJECT_STRUCTURE.md` - Detailed project organization
- `MANIFEST.md` - This file
- `requirements.txt` - Python package dependencies

## Configuration Files

- `.gitignore` - Git ignore patterns
- `.flake8` - Flake8 linting configuration
- `pyproject.toml` - Black, isort, and pylint configuration

## Source Code (`src/`)

- `src/__init__.py` - Package initialization and exports
- `src/data_loader.py` - Data loading and preprocessing classes
- `src/text_processor.py` - Text processing and NLP utilities
- `src/analyzer.py` - Statistical analysis classes

## Notebooks (`notebooks/`)

- `notebooks/01_eda_analysis.ipynb` - Main exploratory data analysis notebook
- `notebooks/README.md` - Notebook-specific documentation
- `notebooks/figures/` - Generated visualization outputs

## Scripts (`scripts/`)

- `scripts/test_setup.py` - Environment verification script
- `scripts/trust_notebook.py` - Jupyter notebook trust script
- `scripts/README.md` - Scripts documentation

## Tests (`tests/`)

- `tests/test_data_loader.py` - Unit tests for data loading module
- `tests/__init__.py` - Test package initialization

## Data (`data/`)

- `data/raw_analyst_ratings.csv` - Main dataset (1.4M+ rows)

## File Count Summary

- Python modules: 6 (src: 3, scripts: 2, tests: 1)
- Notebooks: 1
- Documentation files: 4
- Configuration files: 3
- Test files: 1

