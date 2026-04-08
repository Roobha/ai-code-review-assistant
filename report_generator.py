import json
import os

def generate_report(static_results, llm_feedback, output_path='reports/review_report.txt'):
    """
    Merges static and LLM results, generates a comprehensive readable report.
    Saves to file and returns the content.
    """
    report = "Code Review Report\n"
    report += "=" * 50 + "\n\n"

    report += "Bugs and Logical Errors:\n"
    report += "-" * 50 + "\n"
    
    bugs_found = False
    

    manual_bugs = static_results.get('manual_bugs', [])
    for bug in manual_bugs:
        line = bug.get('line', 'N/A')
        issue = bug.get('issue', 'Unknown issue')
        code = bug.get('code', '')
        report += f"  • Line {line}: {issue}\n"
        if code:
            report += f"    Code: {code}\n"
        bugs_found = True
    
    pylint_bugs = []
    for msg in static_results.get('pylint', []):
        if msg.get('type') == 'error':
            line = msg.get('line', 'N/A')
            message = msg.get('message', 'Unknown pylint error')
            pylint_bugs.append(f"Line {line}: {message}")
    
    for bug in pylint_bugs:
        report += f"  • {bug}\n"
        bugs_found = True

    llm_bugs = llm_feedback.get('bugs', [])
    for item in llm_bugs:
        issue = item.get('issue', 'Unknown issue')
        suggestion = item.get('suggestion', 'No suggestion')
        report += f"  • {issue}\n    → Fix: {suggestion}\n"
        bugs_found = True
    
    if not bugs_found:
        report += "  ✓ No bugs detected.\n"
    
    report += "\n"
    

    report += "Code Style Issues:\n"
    report += "-" * 50 + "\n"
    
    style_found = False
    

    flake8_issues = static_results.get('flake8', [])
    for issue in flake8_issues:
        if issue and not issue.startswith("Flake8"):  
            report += f"  • {issue}\n"
            style_found = True
    

    llm_style = llm_feedback.get('style', [])
    for item in llm_style:
        issue = item.get('issue', 'Unknown issue')
        suggestion = item.get('suggestion', 'No suggestion')
        report += f"  • {issue}\n    → Fix: {suggestion}\n"
        style_found = True
    
    if not style_found:
        report += "  ✓ No style issues detected.\n"
    
    report += "\n"
    

    report += "Optimization Opportunities:\n"
    report += "-" * 50 + "\n"
    
    optimizations_found = False
    

    radon_results = static_results.get('radon', [])
    for item in radon_results:
        complexity = item.get('complexity', 0)
        name = item.get('name', 'Unknown')
        
        if complexity > 10:
            report += f"  • High complexity in '{name}': Score {complexity}\n"
            report += f"    → Fix: Simplify function logic, break into smaller functions\n"
            optimizations_found = True
        elif complexity > 5:
            report += f"  • Medium complexity in '{name}': Score {complexity}\n"
            report += f"    → Consider: Refactoring for better readability\n"
            optimizations_found = True
    

    bandit_results = static_results.get('bandit', {})
    bandit_issues = bandit_results.get('results', [])
    
    for issue in bandit_issues:
        severity = issue.get('issue_severity', 'UNKNOWN')
        confidence = issue.get('issue_confidence', 'UNKNOWN')
        test_name = issue.get('test_name', 'Unknown test')
        issue_text = issue.get('issue_text', 'No description')
        line = issue.get('line_number', 'N/A')
        
        report += f"  • Security [{severity}/{confidence}] at line {line}:\n"
        report += f"    {test_name}: {issue_text}\n"
        optimizations_found = True
    

    llm_optimizations = llm_feedback.get('optimizations', [])
    for item in llm_optimizations:
        issue = item.get('issue', 'Unknown issue')
        suggestion = item.get('suggestion', 'No suggestion')
        report += f"  • {issue}\n    → Fix: {suggestion}\n"
        optimizations_found = True
    
    if not optimizations_found:
        report += "  ✓ No optimization issues detected.\n"
    
    report += "\n"
    

    report += "Summary:\n"
    report += "-" * 50 + "\n"
    total_issues = (
        len(manual_bugs) +
        len(pylint_bugs) + 
        len(llm_bugs) + 
        len([i for i in flake8_issues if i and not i.startswith("Flake8")]) +
        len(llm_style) +
        len([i for i in radon_results if i.get('complexity', 0) > 5]) +
        len(bandit_issues) +
        len(llm_optimizations)
    )
    report += f"  Total issues found: {total_issues}\n"
    report += f"  • Bugs: {len(manual_bugs) + len(pylint_bugs) + len(llm_bugs)}\n"
    report += f"  • Style: {len([i for i in flake8_issues if i and not i.startswith('Flake8')]) + len(llm_style)}\n"
    report += f"  • Optimizations: {len([i for i in radon_results if i.get('complexity', 0) > 5]) + len(bandit_issues) + len(llm_optimizations)}\n"
    

    try:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
    except Exception as e:
        print(f"Warning: Failed to save report to file: {e}")
    
    return report