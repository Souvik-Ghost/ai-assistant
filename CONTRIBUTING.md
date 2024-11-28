# Contributing to AI Assistant

First off, thank you for considering contributing to AI Assistant! It's people like you that make AI Assistant such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible
* Include your environment details (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful
* List some other applications where this enhancement exists, if applicable

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python style guide
* Include screenshots in your pull request whenever possible
* End files with a newline
* Avoid platform-dependent code
* Use Python 3.8 or higher

## Development Process

1. Fork the repo
2. Create a new branch from `main`
3. Make your changes
4. Run the tests
5. Push to your fork and submit a pull request

### Setting up your environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ai_assistant.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov flake8 black
```

### Running Tests

```bash
# Run all tests
pytest tests.py

# Run with coverage report
pytest tests.py --cov=ai_assistant
```

### Code Style

* Follow PEP 8
* Use [Black](https://github.com/psf/black) for code formatting
* Use meaningful variable names
* Comment your code when necessary
* Keep functions small and focused

## Project Structure

```
ai_assistant/
├── ai_assistant/
│   ├── modules/
│   │   ├── visual_detection.py
│   │   ├── audio_detection.py
│   │   ├── device_monitoring.py
│   │   ├── internet_search.py
│   │   └── osint_tools.py
│   └── main.py
├── tests/
├── docs/
└── resources/
```

## Documentation

* Keep README.md up to date
* Document all functions and classes
* Include docstrings in your code
* Update documentation for any new features

## Community

* Join our discussions in GitHub Discussions
* Help others in issues and pull requests
* Share your ideas and feedback

## Questions?

Feel free to open an issue with your question or contact the maintainers directly.

Thank you for contributing to AI Assistant!
