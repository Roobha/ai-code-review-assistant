import subprocess
import json
import sys
from io import StringIO
from pylint.lint import Run
from pylint.reporters.json_reporter import JSONReporter
import radon.complexity as radon_cc

def run_static_analysis(file_path):
    """
    Runs static analysis on the given Python file using pylint, flake8, radon, and bandit.
    Returns results as a structured dictionary.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        return {
            'pylint': [{"error": f"Failed to read file: {str(e)}"}],
            'flake8': [],
            'radon': [],
            'bandit': {},
            'manual_bugs': []
        }
    
    results = {
        'pylint': run_pylint(file_path),
        'flake8': run_flake8(file_path),
        'radon': run_radon(code),
        'bandit': run_bandit(file_path),
        'manual_bugs': detect_common_bugs(code)  
    }
    return results

def run_pylint(file_path):
    """Runs pylint and captures JSON output."""
    output_stream = StringIO()
    reporter = JSONReporter(output=output_stream)

    try:
        Run([file_path], reporter=reporter, exit=False)
        json_str = output_stream.getvalue().strip()
        
        if not json_str:
            return []
            
        return json.loads(json_str)
    
    except Exception as e:
        return [{"error": f"Pylint failed: {str(e)}"}]

def run_flake8(file_path):
    """Runs flake8 via subprocess and captures output."""
    try:
        result = subprocess.run(
            ["flake8", file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout.strip()
        if not output:
            return []

        return output.splitlines()

    except FileNotFoundError:
        return ["Flake8 is not installed or not found in PATH"]
    except subprocess.TimeoutExpired:
        return ["Flake8 timed out"]
    except Exception as e:
        return [f"Flake8 error: {str(e)}"]

def run_radon(code):
    """Runs radon for complexity metrics."""
    try:
        complexity = radon_cc.cc_visit(code)
        return [{'name': item.name, 'complexity': item.complexity} for item in complexity]
    except Exception as e:
        return [{"error": f"Radon failed: {str(e)}"}]

def run_bandit(file_path):
    """Runs bandit and captures JSON output."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "bandit", "-r", file_path, "-f", "json"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.stdout.strip():
            return json.loads(result.stdout)

        return {"results": []}

    except FileNotFoundError:
        return {"error": "Bandit is not installed", "results": []}
    except subprocess.TimeoutExpired:
        return {"error": "Bandit timed out", "results": []}
    except json.JSONDecodeError:
        return {"error": "Failed to parse Bandit output", "results": []}
    except Exception as e:
        return {"error": str(e), "results": []}


def detect_common_bugs(code):
    """
    Manual detection of common Python bugs that static analyzers might miss.
    Returns a list of detected bug patterns.
    """
    import re
    bugs = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        if re.search(r'return\s+\w+\s*/\s*\w+', line) and i > 1:
            prev_lines = '\n'.join(lines[max(0, i-5):i])
            if 'if' not in prev_lines or '== 0' not in prev_lines:
                bugs.append({
                    'line': i,
                    'issue': 'Potential division by zero without validation',
                    'code': line.strip()
                })
        
        if re.search(r'\[len\(\w+\)\]', line):
            bugs.append({
                'line': i,
                'issue': 'Index out of bounds: Using len(arr) instead of len(arr)-1',
                'code': line.strip()
            })
        
        if re.search(r'def\s+\w+\([^)]*=\s*\[\]', line):
            bugs.append({
                'line': i,
                'issue': 'Mutable default argument (list) - will persist across calls',
                'code': line.strip()
            })
        
        if re.search(r'def\s+\w+\([^)]*=\s*\{\}', line):
            bugs.append({
                'line': i,
                'issue': 'Mutable default argument (dict) - will persist across calls',
                'code': line.strip()
            })
        
        if i < len(lines):
            if 'return' in line and not line.strip().startswith('#'):
                next_line = lines[i].strip() if i < len(lines) else ''
                if next_line and not next_line.startswith('#') and not next_line.startswith('def') and not next_line.startswith('class'):
                    # Check indentation to see if it's at same level
                    current_indent = len(line) - len(line.lstrip())
                    next_indent = len(lines[i]) - len(lines[i].lstrip())
                    if next_indent == current_indent and next_line:
                        bugs.append({
                            'line': i + 1,
                            'issue': 'Unreachable code after return statement',
                            'code': next_line
                        })

        if re.match(r'\s*while\s+\w+\s*[><=]', line):
            next_lines = '\n'.join(lines[i:min(i+10, len(lines))])
            var_match = re.search(r'while\s+(\w+)', line)
            if var_match:
                var_name = var_match.group(1)
                if var_name not in next_lines or f'{var_name} -=' not in next_lines and f'{var_name} +=' not in next_lines and f'{var_name}-=' not in next_lines:
                    bugs.append({
                        'line': i,
                        'issue': f'Potential infinite loop: variable "{var_name}" may not be modified',
                        'code': line.strip()
                    })
        
        if 'int(' in line and 'try' not in '\n'.join(lines[max(0, i-3):i]):
            bugs.append({
                'line': i,
                'issue': 'Missing error handling for int() conversion',
                'code': line.strip()
            })
    
    return bugs