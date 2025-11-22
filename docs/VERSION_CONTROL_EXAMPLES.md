# Version Control Examples

This document demonstrates how to break down large changes into smaller, focused commits and use pull requests effectively.

## Example: Breaking Down a Large Feature

### Scenario: Adding a Complete Analysis Module

**❌ Bad Approach: One Large Commit**
```bash
git checkout -b feat/analysis-module
# ... write all code ...
git add src/analyzer.py tests/test_analyzer.py docs/analyzer.md README.md
git commit -m "feat: Add complete analysis module with tests and docs"
```

**✅ Good Approach: Multiple Focused Commits**

```bash
# Step 1: Create branch
git checkout -b feat/analysis-module

# Step 2: Add base class structure
git add src/analyzer.py
git commit -m "feat(analyzer): Add DescriptiveAnalyzer class skeleton"

# Step 3: Implement headline statistics
git add src/analyzer.py
git commit -m "feat(analyzer): Implement headline_stats method"

# Step 4: Implement publisher statistics
git add src/analyzer.py
git commit -m "feat(analyzer): Implement publisher_stats method"

# Step 5: Add TimeSeriesAnalyzer class
git add src/analyzer.py
git commit -m "feat(analyzer): Add TimeSeriesAnalyzer class"

# Step 6: Implement daily counts method
git add src/analyzer.py
git commit -m "feat(analyzer): Add daily_counts method to TimeSeriesAnalyzer"

# Step 7: Add hourly distribution method
git add src/analyzer.py
git commit -m "feat(analyzer): Add hourly_distribution method"

# Step 8: Add PublisherAnalyzer class
git add src/analyzer.py
git commit -m "feat(analyzer): Add PublisherAnalyzer class"

# Step 9: Add email domain extraction
git add src/analyzer.py
git commit -m "feat(analyzer): Add email domain extraction to PublisherAnalyzer"

# Step 10: Add unit tests for DescriptiveAnalyzer
git add tests/test_analyzer.py
git commit -m "test(analyzer): Add unit tests for DescriptiveAnalyzer"

# Step 11: Add unit tests for TimeSeriesAnalyzer
git add tests/test_analyzer.py
git commit -m "test(analyzer): Add unit tests for TimeSeriesAnalyzer"

# Step 12: Add unit tests for PublisherAnalyzer
git add tests/test_analyzer.py
git commit -m "test(analyzer): Add unit tests for PublisherAnalyzer"

# Step 13: Update module exports
git add src/__init__.py
git commit -m "feat(analyzer): Export analyzer classes in __init__.py"

# Step 14: Add documentation
git add docs/analyzer.md
git commit -m "docs(analyzer): Add analyzer module documentation"

# Step 15: Update README
git add README.md
git commit -m "docs: Update README with analyzer usage examples"

# Step 16: Push and create PR
git push origin feat/analysis-module
```

## Example: Fixing Multiple Issues

### Scenario: Fixing Several Related Bugs

**❌ Bad Approach: One Commit for All Fixes**
```bash
git checkout -b fix/multiple-bugs
# ... fix all bugs ...
git commit -m "fix: Fix date conversion, NLTK download, and path issues"
```

**✅ Good Approach: One Fix Per Commit**

```bash
# Step 1: Create branch
git checkout -b fix/multiple-bugs

# Step 2: Fix date conversion issue
git add src/data_loader.py
git commit -m "fix(data_loader): Ensure date column is datetime before conversion"

# Step 3: Fix NLTK download issue
git add src/text_processor.py
git commit -m "fix(text_processor): Add punkt_tab download check"

# Step 4: Fix path resolution issue
git add notebooks/01_eda_analysis.ipynb
git commit -m "fix(notebook): Improve path resolution for data file"

# Step 5: Add tests for date conversion fix
git add tests/test_data_loader.py
git commit -m "test(data_loader): Add test for date conversion fix"

# Step 6: Update documentation
git add README.md
git commit -m "docs: Update troubleshooting for fixed issues"

# Step 7: Push and create PR
git push origin fix/multiple-bugs
```

## Example: Refactoring with Tests

### Scenario: Refactoring a Large Function

**❌ Bad Approach: Refactor and Test Together**
```bash
git checkout -b refactor/processor
# ... refactor and add tests ...
git commit -m "refactor: Refactor text processor and add tests"
```

**✅ Good Approach: Separate Refactor and Test Commits**

```bash
# Step 1: Create branch
git checkout -b refactor/processor

# Step 2: Extract helper method
git add src/text_processor.py
git commit -m "refactor(text_processor): Extract _clean_text helper method"

# Step 3: Extract tokenization method
git add src/text_processor.py
git commit -m "refactor(text_processor): Extract _tokenize_text helper method"

# Step 4: Simplify main preprocess method
git add src/text_processor.py
git commit -m "refactor(text_processor): Simplify preprocess using helper methods"

# Step 5: Add tests for helper methods
git add tests/test_text_processor.py
git commit -m "test(text_processor): Add tests for _clean_text helper"

# Step 6: Add tests for tokenization
git add tests/test_text_processor.py
git commit -m "test(text_processor): Add tests for _tokenize_text helper"

# Step 7: Update integration tests
git add tests/test_text_processor.py
git commit -m "test(text_processor): Update integration tests for refactored code"

# Step 8: Push and create PR
git push origin refactor/processor
```

## Pull Request Best Practices

### Creating a Good PR

1. **Small, Focused PRs**
   - Aim for < 400 lines changed
   - One feature or fix per PR
   - Easy to review and understand

2. **Clear Description**
   ```markdown
   ## Description
   Adds sentiment analysis functionality to analyze headline sentiment.
   
   ## Changes
   - Add SentimentAnalyzer class
   - Implement VADER sentiment analysis
   - Add sentiment scoring methods
   - Add unit tests
   - Update documentation
   
   ## Testing
   - [x] Unit tests pass
   - [x] Manual testing completed
   - [x] Documentation updated
   ```

3. **Link Related Issues**
   ```markdown
   Closes #123
   Related to #456
   ```

4. **Request Specific Reviewers**
   - Tag relevant team members
   - Explain what you'd like reviewed

### PR Review Process

1. **Self-Review First**
   ```bash
   # Review your own changes
   git diff origin/main...HEAD
   
   # Run tests
   pytest tests/
   
   # Check linting
   flake8 src/ tests/
   ```

2. **Address Feedback**
   ```bash
   # Make requested changes
   git add src/module.py
   git commit -m "fix(module): Address review feedback on method naming"
   
   # Push updates
   git push origin feat/your-feature
   ```

3. **Squash Commits (if requested)**
   ```bash
   # Interactive rebase
   git rebase -i origin/main
   
   # Mark commits as 'squash' or 'fixup'
   # Save and close editor
   
   # Force push (with lease for safety)
   git push --force-with-lease origin feat/your-feature
   ```

## Commit Frequency Guidelines

### When to Commit

✅ **Commit After:**
- Completing a small logical unit of work
- Fixing a bug
- Adding a test
- Updating documentation
- Before leaving work (even if incomplete)

❌ **Don't Commit:**
- Broken code that doesn't compile
- Code with failing tests
- Work in progress without clear purpose
- Multiple unrelated changes together

### Daily Workflow Example

```bash
# Morning: Start feature
git checkout -b feat/new-feature

# Work on feature
# ... write code ...

# Commit progress
git add src/module.py
git commit -m "feat(module): Add initial implementation"

# Continue work
# ... add more code ...

# Commit again
git add src/module.py
git commit -m "feat(module): Add error handling"

# After lunch: Add tests
# ... write tests ...

git add tests/test_module.py
git commit -m "test(module): Add unit tests"

# Afternoon: Add documentation
# ... write docs ...

git add docs/module.md
git commit -m "docs(module): Add usage documentation"

# End of day: Push progress
git push origin feat/new-feature
```

## Tools and Tips

### Interactive Staging
```bash
# Stage specific parts of a file
git add -p src/module.py

# Review what will be committed
git diff --staged
```

### Commit Message Editor
```bash
# Configure editor
git config --global core.editor "code --wait"

# Use multi-line commit messages
git commit
# Opens editor for detailed message
```

### View Commit History
```bash
# See commit log
git log --oneline --graph

# See what changed in a commit
git show <commit-hash>

# See changes between commits
git diff <commit1> <commit2>
```

### Amend Last Commit
```bash
# Fix last commit message
git commit --amend -m "feat(module): Corrected commit message"

# Add changes to last commit
git add forgotten_file.py
git commit --amend --no-edit
```

## Summary

**Key Principles:**
1. ✅ Small, focused commits
2. ✅ One logical change per commit
3. ✅ Clear, descriptive commit messages
4. ✅ Test before committing
5. ✅ Use pull requests for review
6. ✅ Address feedback promptly

**Remember:** Good commits tell a story. Each commit should be a complete, reviewable unit of work that builds logically on previous commits.

