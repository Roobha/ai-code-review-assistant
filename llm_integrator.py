import os
import json
import re

def integrate_llm(code, static_results, user_level="Beginner"):
    
    # 🧠 Code Understanding
    intent = "This code defines functions and performs logical operations."

    # ⚡ Performance Prediction
    performance = []
    if code.count("for") >= 2:
        performance.append({
            "issue": "Nested loops detected",
            "suggestion": "Time complexity may be O(n²), consider optimizing"
        })

    # 🎯 Personalized Feedback
    if user_level == "Beginner":
        personalized_feedback = [
            {"tip": "Add proper error handling and comments"}
        ]
    else:
        personalized_feedback = [
            {"tip": "Focus on performance optimization and modular design"}
        ]

    # 🎓 Difficulty
    difficulty = "Beginner"
    if code.count("for") >= 2:
        difficulty = "Intermediate"
    if code.count("for") >= 3:
        difficulty = "Advanced"

    return {
        "intent": intent,
        "bugs": [],
        "style": [],
        "optimizations": [],
        "performance": performance,
        "personalized_feedback": personalized_feedback,
        "difficulty": difficulty
    }
    


def build_prompt(code, static_results):
    """Builds a detailed prompt for the LLM with specific instructions."""
    

    radon_info = static_results.get('radon', [])
    complexity_summary = "\n".join([
        f"  - Function '{r.get('name')}': Complexity {r.get('complexity')}" 
        for r in radon_info
    ]) if radon_info else "  - No complexity data"
    
    return f"""You are an expert Python code reviewer. Analyze this code and find REAL issues.

CODE TO REVIEW:
```python
{code}
```

STATIC ANALYSIS SUMMARY:
Complexity Analysis:
{complexity_summary}

Security Issues Found: {len(static_results.get('bandit', {}).get('results', []))}
Style Issues Found: {len(static_results.get('flake8', []))}

YOUR TASK - BE THOROUGH:

1.  BUGS AND LOGICAL ERRORS - Look for:
   - Division by zero vulnerabilities
   - Index out of bounds errors (off-by-one errors)
   - Unreachable code after return statements
   - Mutable default arguments (def func(x=[]))
   - Infinite loops (missing loop counters)
   - Missing error handling (no try-except for risky operations)
   - Race conditions in global variable usage
   - Type errors and None handling issues

2.  CODE STYLE ISSUES - Look for:
   - Missing docstrings for functions
   - Poor variable naming (single letters, unclear names)
   - Functions doing too many things (SRP violation)
   - Magic numbers without explanation
   - Inconsistent naming conventions

3.  OPTIMIZATION OPPORTUNITIES - Look for:
   - Nested loops creating O(n²) or O(n³) complexity
   - Using list.append in loops instead of list comprehension
   - Inefficient string concatenation (using + instead of join)
   - Loading entire files into memory instead of streaming
   - Using list when set would be more efficient
   - Creating unnecessary intermediate data structures
   - Not using generators for large sequences

CRITICAL: Focus on issues that static tools MISSED. Don't repeat what Flake8/Bandit already found.

RESPONSE FORMAT - VALID JSON ONLY:
{{
  "bugs": [
    {{
      "issue": "Function 'divide_numbers' at line X: Missing zero division check",
      "suggestion": "Add 'if b == 0: raise ValueError(\"Cannot divide by zero\")' before division"
    }}
  ],
  "style": [
    {{
      "issue": "Function 'calc' at line X: Missing docstring and unclear name",
      "suggestion": "Rename to 'calculate_sum' and add docstring explaining parameters"
    }}
  ],
  "optimizations": [
    {{
      "issue": "Function 'calc' at line X: O(n³) complexity from triple nested loops",
      "suggestion": "Reconsider algorithm - triple nested loops are extremely inefficient. If this is intentional for demonstration, add a comment"
    }}
  ]
}}

RESPOND WITH ONLY THE JSON OBJECT. NO MARKDOWN, NO EXPLANATIONS, JUST THE JSON."""


def parse_llm_response(response_text):
    """Parses LLM's JSON response with robust error handling."""
    try:
        # Remove any markdown formatting
        cleaned = response_text.strip()
        
        # Remove markdown code blocks
        cleaned = re.sub(r'^```json\s*', '', cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r'^```\s*', '', cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r'\s*```$', '', cleaned, flags=re.MULTILINE)
        cleaned = cleaned.strip()
        
        # Try to extract JSON object
        json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if json_match:
            cleaned = json_match.group(0)
        
        # Parse JSON
        parsed = json.loads(cleaned)
        
        # Validate structure
        if not isinstance(parsed, dict):
            raise ValueError("Response is not a dictionary")
        
        result = {
            "bugs": parsed.get("bugs", []),
            "style": parsed.get("style", []),
            "optimizations": parsed.get("optimizations", [])
        }
        
        # Validate each section is a list
        for key in ["bugs", "style", "optimizations"]:
            if not isinstance(result[key], list):
                result[key] = []
        
        # Print summary of what LLM found
        print(f"   LLM found: {len(result['bugs'])} bugs, {len(result['style'])} style issues, {len(result['optimizations'])} optimizations")
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"  JSON Parse Error: {e}")
        print(f"   Response preview: {response_text[:200]}...")
        
        # Try to salvage partial information
        return try_fallback_parsing(response_text)
        
    except Exception as e:
        print(f"  Parse Error: {str(e)}")
        return {
            'error': str(e),
            'bugs': [],
            'style': [],
            'optimizations': []
        }


def try_fallback_parsing(response_text):
    """Attempt to extract information even if JSON parsing fails."""
    print("   Attempting fallback parsing...")
    
    result = {
        'bugs': [],
        'style': [],
        'optimizations': [],
        'error': 'Fallback parsing used'
    }
    
    # Try to find structured information even in plain text
    lines = response_text.split('\n')
    current_section = None
    
    for line in lines:
        line_lower = line.lower().strip()
        
        if 'bug' in line_lower and ':' in line_lower:
            current_section = 'bugs'
        elif 'style' in line_lower and ':' in line_lower:
            current_section = 'style'
        elif 'optimization' in line_lower and ':' in line_lower:
            current_section = 'optimizations'
        elif current_section and line.strip().startswith('-'):
            # Extract bullet point
            issue_text = line.strip('- ').strip()
            if issue_text:
                result[current_section].append({
                    'issue': issue_text,
                    'suggestion': 'See above'
                })
    
    print(f"   Fallback found: {len(result['bugs'])} bugs, {len(result['style'])} style, {len(result['optimizations'])} opts")
    return result