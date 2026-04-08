import sys
from static_analyzer import run_static_analysis
from llm_integrator import integrate_llm
from report_generator import generate_report

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    print("Running static analysis...")
    static_results = run_static_analysis(file_path)
    
    print("Getting LLM feedback...")
    user_level = "Beginner"  # temporary (later from UI)

    llm_feedback = integrate_llm(code, static_results, user_level)
    
    print("Generating report...")
    report = generate_report(static_results, llm_feedback)
    print("\n" + report)
    print("\nReport saved to: reports/review_report.txt")

if __name__ == '__main__':
    main()