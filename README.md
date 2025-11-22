# Sentiment-Driven Stock Prediction

A comprehensive machine learning project for predicting stock movements based on analyst ratings and news sentiment analysis.

## Project Overview

This project analyzes financial news headlines and analyst ratings to extract sentiment and predict stock price movements. The analysis includes exploratory data analysis (EDA), natural language processing, topic modeling, and time series analysis.

## Project Structure

```
sentiment-driven-stock-prediction/
├── data/
│   └── raw_analyst_ratings.csv    # Raw dataset of analyst ratings and headlines
├── notebooks/
│   ├── 01_eda_analysis.ipynb      # Comprehensive EDA notebook
│   └── figures/                    # Generated visualizations
├── scripts/                        # Utility scripts
│   ├── test_setup.py              # Environment verification
│   └── trust_notebook.py          # Notebook trust utility
├── src/                           # Source code modules
│   ├── data_loader.py             # Data loading and preprocessing
│   ├── text_processor.py          # Text processing and NLP
│   └── analyzer.py                # Statistical analysis classes
├── tests/                         # Unit tests
└── requirements.txt               # Python dependencies
```

For detailed structure information, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

## Dataset

The dataset contains over 1.4 million analyst ratings and news headlines with the following features:
- **headline**: News headline text
- **url**: Source URL
- **publisher**: Publisher name or email
- **date**: Publication timestamp
- **stock**: Stock ticker symbol

## Features

### Exploratory Data Analysis (EDA)
- **Descriptive Statistics**: Headline length analysis, publisher activity metrics, comprehensive statistical summaries
- **Text Analysis**: Keyword extraction, topic modeling using LDA, phrase analysis (bigrams/trigrams), word cloud generation
- **Time Series Analysis**: Publication frequency trends, hourly patterns, monthly trends, publication spikes identification
- **Publisher Analysis**: Publisher activity, email domain analysis, publisher characteristics, activity trends over time

### Robust Error Handling
- Automatic date column conversion and temporal feature creation
- NLTK data download and corruption handling
- Missing column detection and auto-creation
- Execution order independence

### Key Analyses Performed
1. Headline length and word count distributions
2. Most active publishers identification
3. Publication date trends and patterns
4. Natural language processing for keyword extraction
5. Topic modeling to identify common themes
6. Time series analysis of publication frequency
7. Publisher type analysis (email vs. named publishers)
8. Email domain extraction and analysis

## Setup

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sentiment-driven-stock-prediction
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download NLTK data (will be done automatically in the notebook):
```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')  # Required for newer NLTK versions
nltk.download('stopwords')
nltk.download('wordnet')
```

**Note:** The notebook will automatically download all required NLTK data when you run it. However, if you encounter issues, you can manually download them as shown above.

## Usage

### Running the EDA Notebook

1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Navigate to `notebooks/01_eda_analysis.ipynb`

3. Run all cells to perform the complete EDA analysis

The notebook will generate:
- Statistical summaries
- Visualizations saved in `notebooks/figures/`
- Interactive Plotly charts

### Troubleshooting

**Notebook "Not Trusted" Warning:**
If you see a warning that the notebook is not trusted, run:
```bash
python3 scripts/trust_notebook.py
```

**NLTK Data Issues:**
If you encounter `BadZipFile` or `LookupError` errors with NLTK, the notebook will automatically attempt to re-download corrupted or missing data files. If issues persist, you can manually clear and re-download:
```python
import nltk
nltk.download('punkt', force=True)
nltk.download('punkt_tab', force=True)  # Required for newer NLTK versions
nltk.download('stopwords', force=True)
nltk.download('wordnet', force=True)
```

**Common NLTK Errors:**
- `BadZipFile`: Corrupted NLTK data file - will be auto-fixed by re-downloading
- `LookupError: punkt_tab not found`: Missing punkt_tab resource - download it manually or let the notebook handle it
- `AttributeError: Can only use .dt accessor with datetimelike values`: Date column not converted to datetime - the notebook handles this automatically

**WebSocket Errors:**
If you see `tornado.websocket.WebSocketClosedError`, this is usually a temporary connection issue. Try:
- Refreshing the browser
- Restarting the Jupyter server
- Checking your network connection

**Missing Column Errors:**
If you encounter `KeyError` for columns like `date_only`, `day_of_week`, `month`, or `hour`, the notebook will automatically create these columns from the `date` column. However, ensure you run the data preprocessing cell (Cell 8) or the notebook will create them automatically when needed.

**Execution Order:**
The notebook is designed to be robust to execution order. You can run cells individually or out of order, and the notebook will:
- Automatically convert date columns to datetime format
- Create missing temporal feature columns (day_of_week, month, hour, etc.)
- Handle missing NLTK data by downloading it automatically
- Provide clear error messages and fallback options

## Dependencies

See `requirements.txt` for the complete list of dependencies. Key libraries include:
- pandas, numpy: Data manipulation
- matplotlib, seaborn, plotly: Visualization
- nltk, scikit-learn: Natural language processing
- gensim: Topic modeling
- statsmodels: Time series analysis

## Project Status

✅ **Completed:**
- Comprehensive EDA notebook with all required analyses
- Robust error handling and data validation
- Automatic NLTK data management
- Professional visualizations and statistical summaries
- Time series and publisher analysis
- Topic modeling and text analysis

## Branches

- `main`: Main development branch
- `task-1`: EDA analysis branch (current)

## Code Organization

The project follows a modular architecture with reusable components:

### Source Modules (`src/`)

- **`data_loader.py`**: 
  - `DataLoader`: Efficient chunked loading of large CSV files
  - `DataPreprocessor`: Date conversion and feature extraction

- **`text_processor.py`**: 
  - `TextPreprocessor`: Text cleaning and tokenization
  - `KeywordExtractor`: Keyword and phrase extraction
  - `NLTKDataManager`: NLTK data download management

- **`analyzer.py`**: 
  - `DescriptiveAnalyzer`: Statistical summaries
  - `TimeSeriesAnalyzer`: Temporal pattern analysis
  - `PublisherAnalyzer`: Publisher pattern analysis

### Usage Example

```python
from src import DataLoader, DataPreprocessor, TextPreprocessor

# Load data
loader = DataLoader('data/raw_analyst_ratings.csv')
df = loader.load_data()

# Preprocess
preprocessor = DataPreprocessor(df)
df = preprocessor.convert_dates().extract_temporal_features().get_dataframe()

# Process text
text_processor = TextPreprocessor()
df['processed_headline'] = text_processor.preprocess_series(df['headline'])
```

## Technical Notes

### Data Processing
- The notebook handles large datasets (1.4M+ rows) efficiently using chunked loading
- All temporal features are automatically created from the date column
- Missing values are handled gracefully throughout the analysis

### Performance
- Text preprocessing uses tqdm for progress tracking (with fallback to standard apply)
- Topic modeling uses a sample of 50,000 rows for computational efficiency
- Visualizations are saved as high-resolution PNG files (300 DPI) and interactive HTML files

### Code Quality
- Code follows PEP 8 style guidelines
- Comprehensive docstrings for all classes and functions
- Linting configuration (`.flake8`, `pyproject.toml`) included
- Unit tests structure in place (see `tests/`)

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/ tests/
isort src/ tests/
flake8 src/ tests/
```

### Contributing

We welcome contributions! Please see our contributing guidelines:

- **[CONTRIBUTING.md](.github/CONTRIBUTING.md)** - Complete contributing guide
- **[COMMIT_GUIDELINES.md](docs/COMMIT_GUIDELINES.md)** - Commit message examples and best practices
- **[Pull Request Template](.github/pull_request_template.md)** - PR template

**Quick Start:**
1. Create a feature branch: `git checkout -b feat/your-feature`
2. Make small, focused commits (see commit guidelines)
3. Push and create a Pull Request
4. Address review feedback

**Commit Guidelines:**
- Use conventional commits: `feat(module): description`
- Make small, focused commits
- One logical change per commit
- Write clear, descriptive messages

See [COMMIT_GUIDELINES.md](docs/COMMIT_GUIDELINES.md) for detailed examples.

### Project Documentation
- See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed structure
- See [CHANGELOG.md](CHANGELOG.md) for version history
- See [MANIFEST.md](MANIFEST.md) for file listing

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Commit with descriptive messages
4. Push and create a pull request

## License

[Add your license here]

## Author

[Add your name/contact information here]
