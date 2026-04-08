# Code Review Analyzer

A comprehensive Python code analyzer that detects bugs, style issues, and optimization opportunities using both static analysis and AI-powered insights.

## Features

- **Bug Detection**: Catches logical errors, runtime issues, and edge cases
- **Style Analysis**: Enforces PEP 8 and best practices
- **Optimization**: Identifies performance bottlenecks and complexity issues
- **Security Scanning**: Detects vulnerabilities and security risks
- **AI-Powered**: Uses Google Gemini for intelligent code review
- **Dual Interface**: Both CLI and Web UI (Streamlit)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd code-review-analyzer

# Install dependencies
pip install -r requirements.txt
```

### Setup Gemini API (Optional but Recommended)

1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set environment variable:

```bash
# Linux/Mac
export GEMINI_API_KEY="your_api_key_here"

# Windows
set GEMINI_API_KEY=your_api_key_here
```

## Usage

### Option 1: Command Line Interface (CLI)

```bash
python main.py sample_bad_code.py
```

**Output**: Analysis report printed to console and saved to `reports/review_report.txt`

### Google Colab CLI Demo

A Google Colab notebook is provided to demonstrate the CLI-based workflow of the Code Review Analyzer without requiring local setup.

🔗 Colab Notebook: https://colab.research.google.com/drive/1BO9liraKOedM8cWvMAiSyAF6zfiuQWdZ#scrollTo=2118rW8JjHDa

This notebook runs the core CLI analysis and showcases report generation in a cloud-based environment.


### Option 2: Web Interface (Streamlit)

```bash
streamlit run app.py
```

**Web Interface Features**:
- Upload Python files or paste code directly
- Configure analysis options
- Interactive results with tabbed views
- Download reports as files

### Streamlit UI Demo

A live interactive Streamlit interface for the Code Review Analyzer is available here:  
🔗 Live Streamlit App: http://automated-code-review-tool.streamlit.app/

This web interface allows users to upload Python files or paste code directly and view analysis results in an interactive format.


## Project Structure

```
code-review-analyzer/
├── main.py                  # CLI entry point
├── app.py                   # Streamlit web UI
├── config.py                # Configuration settings
├── static_analyzer.py       # Static analysis tools
├── llm_integrator.py        # Gemini AI integration
├── report_generator.py      # Report generation
├── requirements.txt         # Dependencies
├── sample_bad_code.py       # Sample code for testing
└── reports/                 # Generated reports
    └── review_report.txt
```

## Approach

The analyzer combines multiple specialized tools for comprehensive code review:

**Static Analysis Tools** (Free, unlimited):
- **Pylint**: Detects code errors and enforces coding standards
- **Flake8**: Checks code style and formatting
- **Radon**: Analyzes code complexity and maintainability metrics
- **Bandit**: Identifies common security vulnerabilities

**AI-Powered Analysis** (Gemini API):
- Provides intelligent, context-aware code review
- Identifies nuanced bugs and optimization opportunities
- Generates detailed explanations and suggestions

This hybrid approach combines the precision of static analysis with the contextual understanding of AI.

## Configuration

Edit `config.py` to customize:

- **Gemini Models**: Choose which models to use
- **Complexity Thresholds**: Adjust analysis sensitivity
- **Enabled Tools**: Toggle specific analyzers on/off
- **Report Settings**: Output format and location

## Gemini API Limitations

The tool uses Google's free tier Gemini API with the following rate limits:

**gemini-1.5-flash**
- Up to 15 requests per minute
- Up to 1,000,000 tokens per minute

**gemini-1.5-pro**
- Up to 2 requests per minute
- Up to 32,000 tokens per minute

**Automatic Fallback**: If quota is exceeded on one model, the tool automatically tries the next model in the configured list.

## Sample Output

```
Code Review Report
==================================================

Bugs and Logical Errors:
--------------------------------------------------
  • Line 29: Index out of bounds: Using len(arr) instead of len(arr)-1
    Code: return arr[len(arr)]
  • Line 20: Potential division by zero without validation
    Code: return a / b
  • Line 74: Mutable default argument (list)
    Code: def add_to_list(item, my_list=[]):

Optimization Opportunities:
--------------------------------------------------
  • High complexity in 'calc': Score 15
    → Fix: Simplify function logic, break into smaller functions
  • Security [HIGH/HIGH] at line 41:
    Command injection detected in os.system()

Summary:
--------------------------------------------------
  Total issues found: 35
  • Bugs: 8
  • Style: 22
  • Optimizations: 5
```

## Troubleshooting

### Quota Exceeded Error
```
gemini-1.5-pro quota exceeded, trying next model...
```
**Solution**: Wait 60 seconds or the system will automatically use `gemini-1.5-flash` which has higher limits.

### No API Key Warning
```
WARNING: GEMINI_API_KEY environment variable not set.
```
**Solution**: Set your API key to enable AI analysis, or continue with static analysis only.

### Import Errors
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Run `pip install -r requirements.txt` to install all dependencies.

## Dependencies

All required packages are listed in `requirements.txt`. Install with:
```bash
pip install -r requirements.txt
```

Key dependencies include:
- `streamlit` - Web UI framework
- `pylint` - Code analysis
- `flake8` - Style checking
- `radon` - Complexity analysis
- `bandit` - Security scanning
- `google-generativeai` - Gemini API client

## Acknowledgments

- Built with [Pylint](https://pylint.org/), [Flake8](https://flake8.pycqa.org/), [Radon](https://radon.readthedocs.io/), and [Bandit](https://bandit.readthedocs.io/)
- AI powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- UI built with [Streamlit](https://streamlit.io/)

---

**Happy Coding!**