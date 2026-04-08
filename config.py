"""
Configuration file for Code Review Analyzer
Centralized settings for better maintainability
"""

import os


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


GEMINI_MODELS = [
    "gemini-1.5-flash",     
    "gemini-1.5-pro",        
    "gemini-2.0-flash-exp"   
]

GEMINI_CONFIG = {
    "temperature": 0.1,      
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}


COMPLEXITY_THRESHOLDS = {
    "low": 5,       
    "medium": 10,   
    "high": 15      
}

SECURITY_SEVERITY_LEVELS = ["LOW", "MEDIUM", "HIGH"]


ENABLED_TOOLS = {
    "pylint": True,
    "flake8": True,
    "radon": True,
    "bandit": True,
    "manual_detection": True,
    "llm_analysis": True
}

TOOL_TIMEOUT = 30

REPORT_OUTPUT_DIR = "reports"
REPORT_FILENAME = "review_report.txt"

BUG_PATTERNS = {
    "division_by_zero": r'return\s+\w+\s*/\s*\w+',
    "index_out_of_bounds": r'\[len\(\w+\)\]',
    "mutable_default_list": r'def\s+\w+\([^)]*=\s*\[\]',
    "mutable_default_dict": r'def\s+\w+\([^)]*=\s*\{\}',
    "infinite_loop": r'\s*while\s+\w+\s*[><=]',
    "missing_int_handling": r'int\(',
}

ENABLE_CACHE = False
CACHE_DIR = ".cache"

ENABLE_PARALLEL = False
MAX_WORKERS = 4

LOG_LEVEL = "INFO" 
LOG_FILE = "analyzer.log"
ENABLE_CONSOLE_LOG = True


UI_CONFIG = {
    "page_title": "Code Review Analyzer",
    "layout": "wide",
    "theme": "dark"  
}