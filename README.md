# Sentiment-Driven Stock Prediction

A machine learning project analyzing financial news sentiment and its correlation with stock price movements.

## Project Description

This project analyzes over 1.4 million financial news headlines and analyst ratings to extract sentiment and correlate it with stock returns. The project was developed across three sequential tasks, each building upon the previous work:

### Task 1: Git and GitHub Setup & Exploratory Data Analysis

**Objectives:**
- Set up Python development environment with proper version control
- Establish GitHub repository with CI/CD workflows
- Perform comprehensive Exploratory Data Analysis (EDA)

**Deliverables:**
- ✅ Git repository with proper branching strategy (`task-1` branch)
- ✅ CI/CD pipeline with unit tests (`.github/workflows/unittests.yml`)
- ✅ Project structure following best practices
- ✅ **Descriptive Statistics**: Headline length analysis, publisher activity metrics, publication date trends
- ✅ **Text Analysis**: NLP-based keyword extraction, topic modeling using LDA, phrase analysis (bigrams/trigrams)
- ✅ **Time Series Analysis**: Publication frequency trends, hourly patterns, monthly trends, event spike identification
- ✅ **Publisher Analysis**: Publisher activity distribution, email domain analysis, publisher characteristics

**Notebook:** `01_eda_analysis.ipynb`

### Task 2: Quantitative Analysis with TA-Lib and PyNance

**Objectives:**
- Integrate financial data sources
- Calculate technical indicators using TA-Lib
- Compute financial metrics using PyNance
- Create comprehensive visualizations

**Deliverables:**
- ✅ Merged `task-1` into main via Pull Request
- ✅ Stock price data loading (CSV and Yahoo Finance API)
- ✅ **Technical Indicators**: SMA, EMA, RSI, MACD, Bollinger Bands
- ✅ **Financial Metrics**: Volatility, Sharpe ratio, returns, risk metrics
- ✅ Interactive dashboards and visualizations
- ✅ Analysis for 6 stocks: AAPL, AMZN, GOOG, META, MSFT, NVDA

**Notebook:** `02_financial_analysis.ipynb`

### Task 3: Sentiment-Return Correlation Analysis

**Objectives:**
- Align news and stock price datasets by dates
- Perform sentiment analysis on news headlines
- Calculate correlation between sentiment and stock returns

**Deliverables:**
- ✅ Merged `task-2` into main via Pull Request
- ✅ **Date Alignment**: Normalized timestamps between news and stock datasets
- ✅ **Sentiment Analysis**: VADER-based sentiment scoring (positive, negative, neutral)
- ✅ **Daily Returns Calculation**: Simple and log returns for stock price movements
- ✅ **Correlation Analysis**: Pearson correlation coefficients with statistical significance testing
- ✅ **Daily Aggregation**: Average sentiment scores when multiple articles appear per day
- ✅ Same-day and lagged (1-day) correlation analysis
- ✅ Per-stock correlation breakdown

**Notebook:** `03_correlation_analysis.ipynb`

## Project Architecture

The project follows a modular, layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  ┌──────────────┐         ┌──────────────────┐            │
│  │ DataLoader    │         │ StockDataLoader  │            │
│  │ (News Data)   │         │ (Price Data)     │            │
│  └──────┬────────┘         └────────┬─────────┘            │
│         │                           │                       │
│         └───────────┬───────────────┘                       │
│                     ▼                                         │
│         ┌──────────────────────┐                             │
│         │  DataPreprocessor    │                             │
│         │  - Date conversion   │                             │
│         │  - Feature extraction│                             │
│         └──────────┬───────────┘                             │
└─────────────────────┼─────────────────────────────────────────┘
                      │
┌─────────────────────┼─────────────────────────────────────────┐
│                    Processing Layer                          │
│         ┌───────────▼───────────┐                            │
│         │  TextProcessor        │                            │
│         │  - Cleaning            │                            │
│         │  - Tokenization       │                            │
│         │  - Keyword extraction │                            │
│         └───────────┬────────────┘                            │
│                     │                                         │
│         ┌───────────▼────────────┐                            │
│         │  SentimentAnalyzer     │                            │
│         │  - VADER analysis     │                            │
│         │  - Sentiment scoring   │                            │
│         └───────────┬────────────┘                            │
└─────────────────────┼─────────────────────────────────────────┘
                      │
┌─────────────────────┼─────────────────────────────────────────┐
│                    Analysis Layer                              │
│  ┌──────────────────▼──────────────────┐                     │
│  │  DescriptiveAnalyzer               │                     │
│  │  TimeSeriesAnalyzer                 │                     │
│  │  PublisherAnalyzer                  │                     │
│  └──────────────────┬──────────────────┘                     │
│                     │                                        │
│  ┌──────────────────▼──────────────────┐                     │
│  │  TechnicalAnalyzer                  │                     │
│  │  - Technical indicators             │                     │
│  │  - Financial metrics                │                     │
│  └──────────────────┬──────────────────┘                     │
│                     │                                        │
│  ┌──────────────────▼──────────────────┐                     │
│  │  SentimentReturnLinker              │                     │
│  │  - Date alignment                   │                     │
│  │  - Correlation analysis             │                     │
│  └─────────────────────────────────────┘                     │
└───────────────────────────────────────────────────────────────┘
```

### Architecture Layers

**Data Layer**
- `DataLoader`: Chunked loading of large CSV files (1.4M+ rows)
- `StockDataLoader`: Stock price data from CSV or Yahoo Finance API
- `DataPreprocessor`: Date normalization, temporal features, text features

**Processing Layer**
- `TextProcessor`: NLP preprocessing, tokenization, keyword extraction
- `SentimentAnalyzer`: VADER-based sentiment analysis and scoring

**Analysis Layer**
- `DescriptiveAnalyzer`: Statistical summaries and distributions
- `TimeSeriesAnalyzer`: Temporal pattern analysis
- `PublisherAnalyzer`: Publisher activity and characteristics
- `TechnicalAnalyzer`: Technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands)
- `SentimentReturnLinker`: Correlation between sentiment and stock returns

### Data Flow

```
Raw Data (CSV)
    ↓
[DataLoader] → Load chunked data
    ↓
[DataPreprocessor] → Normalize dates, extract features
    ↓
[TextProcessor] → Clean and tokenize text
    ↓
[SentimentAnalyzer] → Calculate sentiment scores
    ↓
[SentimentReturnLinker] → Align with stock returns
    ↓
[Analysis Modules] → Generate insights and visualizations
```

### Design Principles

- **Modularity**: Each module has a single, well-defined responsibility
- **Reusability**: Components can be used independently or in combination
- **Scalability**: Chunked loading handles large datasets efficiently
- **Extensibility**: Easy to add new analyzers or data sources
- **Testability**: Each module is independently testable
