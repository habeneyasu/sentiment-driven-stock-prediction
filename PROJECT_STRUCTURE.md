# Project Structure

This document describes the organization of the sentiment-driven stock prediction project.

```
sentiment-driven-stock-prediction/
├── .gitignore                 # Git ignore patterns
├── CHANGELOG.md              # Project changelog
├── PROJECT_STRUCTURE.md      # This file
├── README.md                 # Main project documentation
├── requirements.txt          # Python dependencies
│
├── data/                     # Data directory
│   └── raw_analyst_ratings.csv    # Raw dataset (1.4M+ rows)
│
├── notebooks/                # Jupyter notebooks
│   ├── __init__.py          # Package initialization
│   ├── README.md            # Notebook documentation
│   ├── 01_eda_analysis.ipynb    # Main EDA notebook
│   └── figures/             # Generated visualizations
│       ├── headline_length_distributions.png
│       ├── top_publishers.png
│       ├── wordcloud.png
│       ├── key_phrases.png
│       ├── hourly_distribution.png
│       ├── monthly_trends.png
│       ├── email_domains.png
│       ├── publisher_trends.png
│       └── time_series.html
│
├── scripts/                  # Utility scripts
│   ├── __init__.py          # Package initialization
│   ├── README.md            # Scripts documentation
│   ├── test_setup.py        # Environment verification script
│   └── trust_notebook.py    # Notebook trust script
│
├── src/                      # Source code modules
│   ├── __init__.py          # Package exports
│   ├── data_loader.py      # Data loading and preprocessing
│   ├── text_processor.py    # Text processing and NLP
│   └── analyzer.py          # Statistical analysis classes
│
└── tests/                    # Unit tests
    └── __init__.py          # Package initialization
```

## Directory Descriptions

### `/data/`
Contains raw and processed datasets. The main dataset `raw_analyst_ratings.csv` contains over 1.4 million analyst ratings and news headlines.

### `/notebooks/`
Jupyter notebooks for exploratory data analysis and visualization. The main notebook `01_eda_analysis.ipynb` performs comprehensive EDA including:
- Descriptive statistics
- Text analysis and topic modeling
- Time series analysis
- Publisher analysis

### `/scripts/`
Utility scripts for project setup and maintenance:
- `test_setup.py`: Verifies environment and dependencies
- `trust_notebook.py`: Trusts Jupyter notebooks to avoid warnings

### `/src/`
Modular source code organized into focused modules:
- `data_loader.py`: `DataLoader` and `DataPreprocessor` classes
- `text_processor.py`: `TextPreprocessor`, `KeywordExtractor`, and `NLTKDataManager` classes
- `analyzer.py`: `DescriptiveAnalyzer`, `TimeSeriesAnalyzer`, and `PublisherAnalyzer` classes

### `/tests/`
Unit tests for source code modules (to be implemented).

## File Naming Conventions

- **Python modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/variables**: `snake_case`
- **Notebooks**: `##_descriptive_name.ipynb` (numbered for execution order)
- **Scripts**: `snake_case.py`
- **Documentation**: `UPPERCASE.md` (README, CHANGELOG, etc.)

## Module Dependencies

```
src/
├── data_loader.py      (independent)
├── text_processor.py   (depends on: data_loader for types)
└── analyzer.py         (depends on: data_loader for types)
```

## Data Flow

1. **Data Loading**: `DataLoader` → loads CSV → `DataPreprocessor` → extracts features
2. **Text Processing**: `TextPreprocessor` → cleans text → `KeywordExtractor` → extracts keywords
3. **Analysis**: `DescriptiveAnalyzer` / `TimeSeriesAnalyzer` / `PublisherAnalyzer` → generates statistics

