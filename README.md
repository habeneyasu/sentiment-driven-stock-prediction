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
├── src/                           # Source code modules
├── tests/                         # Unit tests
└── requirements.txt               # Python dependencies
```

## Dataset

The dataset contains over 1.4 million analyst ratings and news headlines with the following features:
- **headline**: News headline text
- **url**: Source URL
- **publisher**: Publisher name or email
- **date**: Publication timestamp
- **stock**: Stock ticker symbol

## Features

### Exploratory Data Analysis (EDA)
- **Descriptive Statistics**: Headline length analysis, publisher activity metrics
- **Text Analysis**: Keyword extraction, topic modeling using LDA, phrase analysis
- **Time Series Analysis**: Publication frequency trends, hourly patterns, monthly trends
- **Publisher Analysis**: Publisher activity, email domain analysis, publisher characteristics

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
nltk.download('stopwords')
nltk.download('wordnet')
```

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

## Dependencies

See `requirements.txt` for the complete list of dependencies. Key libraries include:
- pandas, numpy: Data manipulation
- matplotlib, seaborn, plotly: Visualization
- nltk, scikit-learn: Natural language processing
- gensim: Topic modeling
- statsmodels: Time series analysis

## Branches

- `main`: Main development branch
- `task-1`: EDA analysis branch

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Commit with descriptive messages
4. Push and create a pull request

## License

[Add your license here]

## Author

[Add your name/contact information here]
