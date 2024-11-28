# Development Setup

## Development Environment Setup

### Prerequisites
- Python 3.8+
- Git
- Visual Studio Code (recommended)
- PyCharm (alternative)

### Initial Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/Souvik-Ghost/ai_assistant.git
   cd ai_assistant
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

### IDE Setup

#### Visual Studio Code
1. Install Python extension
2. Select virtual environment
3. Install recommended extensions:
   - Python
   - Python Test Explorer
   - GitLens
   - Python Docstring Generator

#### PyCharm
1. Open project
2. Configure Python interpreter
3. Enable version control integration

## Development Workflow

### 1. Creating a New Feature
```bash
git checkout -b feature/your-feature-name
```

### 2. Running Tests
```bash
pytest tests/
pytest tests/ --cov=ai_assistant  # With coverage
```

### 3. Code Style
- Use Black for formatting
- Follow PEP 8
- Run linters:
  ```bash
  flake8 ai_assistant
  black ai_assistant
  ```

### 4. Documentation
- Add docstrings to all functions/classes
- Update README.md if needed
- Create/update wiki pages

### 5. Submitting Changes
1. Create pull request
2. Ensure CI passes
3. Request review
4. Address feedback

## Module Structure
```
ai_assistant/
├── modules/
│   ├── visual_detection/
│   ├── audio_detection/
│   ├── device_monitoring/
│   ├── internet_search/
│   └── osint_tools/
├── utils/
├── config/
└── tests/
```

## Building

### Windows
```bash
.\build_windows.bat
```

### Android
```bash
./build_android.sh
```

## Debugging

### Using VS Code
1. Set breakpoints
2. Use Debug panel
3. Configure launch.json

### Using PyCharm
1. Set breakpoints
2. Right-click -> Debug

## Logging
- Use the built-in logger
- Log levels: DEBUG, INFO, WARNING, ERROR
- Logs stored in `logs/`

## Need Help?
- Check [Issues](https://github.com/Souvik-Ghost/ai_assistant/issues)
- Join [Discussions](https://github.com/Souvik-Ghost/ai_assistant/discussions)
- Review [Wiki](https://github.com/Souvik-Ghost/ai_assistant/wiki)
