# Commit Guidelines

This document provides examples and guidelines for making effective commits.

## Quick Reference

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(analyzer): Add sentiment analysis` |
| `fix` | Bug fix | `fix(data_loader): Handle empty CSV files` |
| `docs` | Documentation | `docs: Update README with examples` |
| `style` | Formatting | `style: Format code with black` |
| `refactor` | Code restructuring | `refactor(text_processor): Simplify tokenization` |
| `test` | Tests | `test(analyzer): Add unit tests` |
| `chore` | Maintenance | `chore: Update dependencies` |

### Commit Size Examples

#### ✅ Good: Small, Focused Commits

```bash
# Commit 1: Add class structure
git add src/data_loader.py
git commit -m "feat(data_loader): Add DataLoader class skeleton"

# Commit 2: Add loading method
git add src/data_loader.py
git commit -m "feat(data_loader): Implement load_data method"

# Commit 3: Add chunking support
git add src/data_loader.py
git commit -m "feat(data_loader): Add chunked reading for large files"

# Commit 4: Add progress bar
git add src/data_loader.py
git commit -m "feat(data_loader): Add progress bar to load_data"

# Commit 5: Add tests
git add tests/test_data_loader.py
git commit -m "test(data_loader): Add unit tests for DataLoader"

# Commit 6: Add documentation
git add src/data_loader.py
git commit -m "docs(data_loader): Add docstrings and examples"
```

#### ❌ Bad: Large, Unfocused Commits

```bash
# Don't do this:
git add src/data_loader.py tests/test_data_loader.py docs/
git commit -m "feat: Add data loader with tests and docs"
```

## Real-World Examples

### Example 1: Adding a New Feature

**Scenario:** Adding a new sentiment analysis feature

```bash
# Step 1: Create branch
git checkout -b feat/sentiment-analysis

# Step 2: Add core class
git add src/sentiment_analyzer.py
git commit -m "feat(sentiment): Add SentimentAnalyzer class"

# Step 3: Add analysis method
git add src/sentiment_analyzer.py
git commit -m "feat(sentiment): Implement analyze method"

# Step 4: Add preprocessing
git add src/sentiment_analyzer.py
git commit -m "feat(sentiment): Add text preprocessing for sentiment"

# Step 5: Add tests
git add tests/test_sentiment_analyzer.py
git commit -m "test(sentiment): Add unit tests for SentimentAnalyzer"

# Step 6: Add integration test
git add tests/test_sentiment_integration.py
git commit -m "test(sentiment): Add integration tests"

# Step 7: Update documentation
git add README.md docs/sentiment.md
git commit -m "docs(sentiment): Add sentiment analysis documentation"

# Step 8: Push and create PR
git push origin feat/sentiment-analysis
```

### Example 2: Fixing a Bug

**Scenario:** Fixing NLTK download issue

```bash
# Step 1: Create fix branch
git checkout -b fix/nltk-download

# Step 2: Fix the issue
git add src/text_processor.py
git commit -m "fix(text_processor): Handle missing punkt_tab resource"

# Step 3: Add error handling
git add src/text_processor.py
git commit -m "fix(text_processor): Add retry logic for NLTK downloads"

# Step 4: Add test for the fix
git add tests/test_text_processor.py
git commit -m "test(text_processor): Add test for NLTK download handling"

# Step 5: Update documentation
git add README.md
git commit -m "docs: Update troubleshooting section for NLTK issues"

# Step 6: Push and create PR
git push origin fix/nltk-download
```

### Example 3: Refactoring

**Scenario:** Improving code organization

```bash
# Step 1: Create refactor branch
git checkout -b refactor/analyzer-structure

# Step 2: Extract method
git add src/analyzer.py
git commit -m "refactor(analyzer): Extract _ensure_date_column method"

# Step 3: Improve error handling
git add src/analyzer.py
git commit -m "refactor(analyzer): Improve error messages"

# Step 4: Update tests
git add tests/test_analyzer.py
git commit -m "test(analyzer): Update tests for refactored code"

# Step 5: Push and create PR
git push origin refactor/analyzer-structure
```

## Commit Message Templates

### Feature Addition
```
feat(<module>): Add <feature description>

<Detailed description of what was added and why>

Closes #<issue_number>
```

### Bug Fix
```
fix(<module>): Fix <bug description>

<Description of the bug and how it was fixed>

Fixes #<issue_number>
```

### Documentation
```
docs(<module>): <Description of documentation change>

<What documentation was added/updated>
```

### Test Addition
```
test(<module>): Add tests for <feature/functionality>

<Description of what is being tested>
```

## Best Practices

1. **Commit Early, Commit Often**
   - Don't wait until everything is perfect
   - Commit working code frequently
   - Use descriptive commit messages

2. **One Logical Change Per Commit**
   - Each commit should represent one complete thought
   - Easy to review and understand
   - Easy to revert if needed

3. **Write Clear Commit Messages**
   - Use imperative mood ("Add" not "Added")
   - Be specific about what changed
   - Explain why if not obvious

4. **Test Before Committing**
   - Run tests locally
   - Ensure code works
   - Fix linting issues

5. **Review Your Commits**
   - Use `git log` to review before pushing
   - Ensure commits tell a story
   - Consider squashing if needed

## Tools for Better Commits

### Interactive Staging
```bash
git add -p  # Stage changes interactively
```

### Commit Message Editor
```bash
git config --global core.editor "code --wait"  # Use VS Code
git commit  # Opens editor for multi-line messages
```

### View Changes Before Committing
```bash
git diff --staged  # See what will be committed
```

### Amend Last Commit
```bash
git commit --amend  # Fix last commit message or add changes
```

## Common Mistakes to Avoid

1. ❌ **Committing unrelated changes together**
   ```bash
   # Bad
   git commit -m "feat: Add feature and fix bug"
   
   # Good
   git commit -m "feat: Add new feature"
   git commit -m "fix: Fix related bug"
   ```

2. ❌ **Vague commit messages**
   ```bash
   # Bad
   git commit -m "fix stuff"
   
   # Good
   git commit -m "fix(data_loader): Handle empty CSV files gracefully"
   ```

3. ❌ **Committing too much at once**
   ```bash
   # Bad - 500 lines changed
   git commit -m "feat: Add complete analysis pipeline"
   
   # Good - multiple small commits
   git commit -m "feat(loader): Add data loading"
   git commit -m "feat(processor): Add text processing"
   git commit -m "feat(analyzer): Add analysis pipeline"
   ```

4. ❌ **Forgetting to test**
   ```bash
   # Always test before committing
   pytest tests/
   git commit -m "feat: Add feature"
   ```

