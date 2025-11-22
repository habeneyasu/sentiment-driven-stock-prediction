# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Modular source code structure in `src/` with reusable components
- `DataLoader` class for efficient chunked data loading
- `DataPreprocessor` class for date conversion and feature extraction
- `TextPreprocessor` class for NLP text preprocessing
- `NLTKDataManager` for managing NLTK data downloads
- `DescriptiveAnalyzer`, `TimeSeriesAnalyzer`, and `PublisherAnalyzer` classes
- Comprehensive docstrings and inline comments
- CHANGELOG.md for tracking project changes
- Project structure documentation
- Pull request template for structured reviews
- CONTRIBUTING.md with version control best practices
- COMMIT_GUIDELINES.md with examples and templates
- GitHub Actions workflow for automated PR checks
- Testing framework with example unit tests
- Code quality configuration (flake8, black, isort)

### Changed
- Improved code organization with clear module separation
- Enhanced error handling throughout the codebase
- Better documentation and code comments
- Established commit message conventions (Conventional Commits)
- Improved version control practices with PR workflow

## [0.1.0] - 2024-11-22

### Added
- Initial project setup with comprehensive EDA notebook
- Complete exploratory data analysis pipeline
- Descriptive statistics analysis
- Text analysis and topic modeling (LDA)
- Time series analysis of publication frequency
- Publisher analysis including email domain extraction
- Requirements.txt with all dependencies
- README.md with setup and usage instructions
- .gitignore for Python/data science projects
- Notebook trust script for Jupyter
- Setup verification script

### Fixed
- Path resolution issues in notebook
- NLTK data download and corruption handling
- Missing column error handling
- Date column type conversion issues
- punkt_tab download for newer NLTK versions
- Month index mapping with NaN values
- Temporal feature column creation

### Changed
- Improved error handling in EDA notebook
- Made notebook cells execution-order independent
- Enhanced troubleshooting documentation

## [0.0.1] - 2024-11-22

### Added
- Initial repository structure
- Basic project scaffolding
- Git repository initialization

