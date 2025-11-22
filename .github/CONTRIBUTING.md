# Contributing Guide

This guide outlines best practices for contributing to this project, including commit conventions and pull request workflows.

## Version Control Best Practices

### Commit Guidelines

#### Commit Message Format

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(data_loader): Add chunked reading for large files

Implement chunked CSV reading to handle datasets >1GB efficiently.
Add progress bar support using tqdm.

Closes #123
```

```
fix(text_processor): Handle missing punkt_tab resource

Add automatic download of punkt_tab when missing during tokenization.
Prevents LookupError in newer NLTK versions.

Fixes #456
```

#### Commit Size Guidelines

**Make small, focused commits:**
- ✅ One logical change per commit
- ✅ Each commit should be reviewable independently
- ✅ Commits should build on each other logically
- ❌ Don't mix unrelated changes
- ❌ Don't commit multiple features together
- ❌ Don't commit "work in progress" code

**Good commit examples:**
```
feat(data_loader): Add DataLoader class
feat(data_loader): Add chunked reading support
feat(data_loader): Add progress bar integration
test(data_loader): Add unit tests for DataLoader
docs(data_loader): Add class documentation
```

**Bad commit example:**
```
feat: Add data loader, text processor, and analyzer classes with tests and docs
```

### Branch Strategy

#### Branch Naming

- `main`: Production-ready code
- `task-<number>`: Feature branches (e.g., `task-1`, `task-2`)
- `fix/<description>`: Bug fix branches (e.g., `fix/nltk-download`)
- `feat/<description>`: Feature branches (e.g., `feat/sentiment-analysis`)
- `docs/<description>`: Documentation branches (e.g., `docs/api-reference`)

#### Branch Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feat/new-feature
   ```

2. **Make small, focused commits:**
   ```bash
   git add src/module.py
   git commit -m "feat(module): Add new function"
   
   git add tests/test_module.py
   git commit -m "test(module): Add tests for new function"
   ```

3. **Push branch regularly:**
   ```bash
   git push origin feat/new-feature
   ```

4. **Create Pull Request** (see PR workflow below)

### Pull Request Workflow

#### Creating a Pull Request

1. **Ensure your branch is up to date:**
   ```bash
   git checkout main
   git pull origin main
   git checkout feat/your-feature
   git rebase main  # or merge main into your branch
   ```

2. **Push your branch:**
   ```bash
   git push origin feat/your-feature
   ```

3. **Create PR on GitHub:**
   - Use the PR template
   - Provide clear description
   - Link related issues
   - Request reviewers

#### PR Review Process

1. **Self-review first:**
   - Review your own changes
   - Ensure all tests pass
   - Check for code quality issues

2. **Address feedback:**
   - Make requested changes in new commits
   - Respond to comments
   - Update PR description if needed

3. **Squash commits (if requested):**
   ```bash
   git rebase -i HEAD~n  # n = number of commits
   # Mark commits as 'squash' or 'fixup'
   git push --force-with-lease origin feat/your-feature
   ```

#### PR Size Guidelines

- **Small PRs are better:** Aim for < 400 lines changed
- **Break large features into multiple PRs:**
  - PR 1: Core functionality
  - PR 2: Tests
  - PR 3: Documentation
  - PR 4: Integration

### Example: Breaking Down a Large Change

**Instead of one large commit:**
```
feat: Add complete EDA pipeline with all analyses
```

**Break into smaller commits:**
```
feat(data_loader): Add DataLoader class for CSV loading
feat(data_loader): Add chunked reading support
feat(data_preprocessor): Add date conversion functionality
feat(data_preprocessor): Add temporal feature extraction
feat(text_processor): Add TextPreprocessor class
feat(text_processor): Add keyword extraction
feat(analyzer): Add DescriptiveAnalyzer class
feat(analyzer): Add TimeSeriesAnalyzer class
test(data_loader): Add unit tests for DataLoader
test(data_preprocessor): Add unit tests for DataPreprocessor
docs: Add module documentation
docs: Update README with usage examples
```

### Commit Frequency

**Commit often:**
- After completing a small logical unit of work
- After fixing a bug
- After adding a test
- After updating documentation
- Before leaving work (even if incomplete)

**Example workflow:**
```bash
# Morning: Start feature
git checkout -b feat/new-analysis
# ... write code ...
git add src/analyzer.py
git commit -m "feat(analyzer): Add basic analysis method"

# After lunch: Add tests
# ... write tests ...
git add tests/test_analyzer.py
git commit -m "test(analyzer): Add unit tests for analysis method"

# Afternoon: Add documentation
# ... write docs ...
git add docs/analyzer.md
git commit -m "docs(analyzer): Add usage documentation"

# End of day: Push progress
git push origin feat/new-analysis
```

## Code Review Checklist

Before requesting review, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New code has tests
- [ ] Documentation is updated
- [ ] No commented-out code
- [ ] No debugging print statements
- [ ] Commit messages are clear and descriptive
- [ ] Commits are logically organized

## Questions?

If you have questions about contributing, please:
1. Check existing documentation
2. Review similar PRs
3. Ask in project discussions or issues

