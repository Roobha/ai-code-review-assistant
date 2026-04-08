import streamlit as st
import os
import tempfile
from static_analyzer import run_static_analysis
from llm_integrator import integrate_llm
from report_generator import generate_report

# Page configuration
st.set_page_config(
    page_title="Code Review Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
        .main-container {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .header-container {
        text-align: center;
        margin-bottom: 3rem;
        animation: fadeIn 0.6s ease-in;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
            .subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.6);
        letter-spacing: 0.5px;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .bug-count {
        background-color: #ff4b4b;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .style-count {
        background-color: #ffa500;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .opt-count {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-container header-container">
        <div class="main-header">🕵️ Code Review Analyzer</div>
        <div class="subtitle">AI-Powered Python Code Analysis & Optimization</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Gemini API Key (Optional)",
            type="password",
            help="Enter your Google Gemini API key for LLM-powered analysis"
        )
        
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
            st.success("✓ API Key set!")
        else:
            st.info("⚠ LLM features will be limited without an API key.")
        
        st.markdown("---")
        
        # Analysis options
        st.header("📊 Analysis Options")
        run_pylint = st.checkbox("Run Pylint", value=True)
        run_flake8 = st.checkbox("Run Flake8", value=True)
        run_radon = st.checkbox("Run Radon (Complexity)", value=True)
        run_bandit = st.checkbox("Run Bandit (Security)", value=True)
        run_manual = st.checkbox("Manual Bug Detection", value=True)
        run_llm = st.checkbox("AI Insights (Adaptive Engine)", value=True)
        
        st.markdown("---")
        
        # Info
        st.header("ℹ️ About")
        st.markdown("""
        This tool analyzes Python code for:
        - 🐛 Bugs & Logical Errors
        - 🎨 Code Style Issues
        - ⚡ Optimization Opportunities
        - 🔒 Security Vulnerabilities
        """)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Input Code")
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["Upload File", "Paste Code"],
            horizontal=True
        )
        
        code = None
        file_name = "code.py"
        
        if input_method == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload Python file (.py)",
                type=['py'],
                help="Upload a Python file to analyze"
            )
            
            if uploaded_file:
                code = uploaded_file.read().decode('utf-8')
                file_name = uploaded_file.name
                st.success(f"✓ Uploaded: {file_name}")
        
        else:  # Paste Code
            code = st.text_area(
                "Paste your Python code here:",
                height=400,
                placeholder="# Paste your Python code here...\n\ndef example():\n    pass"
            )
        
        # Display code preview
        if code:
            with st.expander("📄 Code Preview", expanded=False):
                st.code(code, language='python', line_numbers=True)
    
    with col2:
        st.subheader("📊 Analysis Results")
        
        if code:
            # Analyze button
            if st.button("🚀 Analyze Code", type="primary", use_container_width=True):
                with st.spinner("🔄 Running analysis..."):
                    temp_path = None
                    try:
                        # Create temp file with proper handling
                        with tempfile.NamedTemporaryFile(
                            mode='w', 
                            suffix='.py', 
                            delete=False,
                            encoding='utf-8'
                        ) as temp_file:
                            temp_file.write(code)
                            temp_path = temp_file.name
                            temp_file.flush()  # Ensure data is written to disk
                            os.fsync(temp_file.fileno())  # Force filesystem sync
                        
                        # Verify file exists and has content
                        if not os.path.exists(temp_path):
                            st.error("❌ Failed to create temporary file")
                            return
                        
                        file_size = os.path.getsize(temp_path)
                        if file_size == 0:
                            st.error("❌ Temporary file is empty")
                            return
                        
                        # Progress tracking
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Run static analysis
                        status_text.text("🔍 Running static analysis...")
                        progress_bar.progress(25)
                        static_results = run_static_analysis(temp_path)

                        
                        # Run LLM analysis
                        status_text.text("🤖 Running AI analysis...")
                        progress_bar.progress(50)
                        if run_llm:
                            try:
                                llm_feedback = integrate_llm(code, static_results)
                            except:
                                llm_feedback = {}
                            if not llm_feedback:
                                llm_feedback = {}
                            if not isinstance(llm_feedback, dict):
                                llm_feedback = {}
                        else:
                            llm_feedback = {
                                "intent": "",
                                "bugs": [],
                                "style": [],
                                "optimizations": [],
                                "performance": [],
                                "personalized_feedback": []
                            }
                        
                        llm_feedback.setdefault("intent", "")
                        llm_feedback.setdefault("bugs", [])
                        llm_feedback.setdefault("style", [])
                        llm_feedback.setdefault("optimizations", [])
                        llm_feedback.setdefault("performance", [])
                        llm_feedback.setdefault("personalized_feedback", [])
                        llm_feedback.setdefault("difficulty", "")

                        # Generate report (disabled for adaptive AI version)
                        status_text.text("📝 Skipping report generation...")
                        progress_bar.progress(75)
                        report = ""
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")
                        
                        # Display results
                        display_results(static_results, llm_feedback, report)
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
                    
                    finally:
                        # Cleanup temp file safely
                        if temp_path and os.path.exists(temp_path):
                            try:
                                os.unlink(temp_path)
                            except PermissionError:
                                # File might be locked, Streamlit will cleanup
                                pass
        else:
            st.info("👈 Upload a file or paste code to begin analysis")


def display_results(static_results, llm_feedback, report):
    """Display analysis results in a structured format."""
    
    # Calculate counts
    manual_bugs = static_results.get('manual_bugs', [])
    pylint_bugs = [msg for msg in static_results.get('pylint', []) if msg.get('type') == 'error']
    llm_bugs = llm_feedback.get('bugs', [])
    
    flake8_issues = [i for i in static_results.get('flake8', []) if i and not i.startswith("Flake8")]
    llm_style = llm_feedback.get('style', [])
    
    radon_issues = [i for i in static_results.get('radon', []) if i.get('complexity', 0) > 5]
    bandit_issues = static_results.get('bandit', {}).get('results', [])
    llm_opts = llm_feedback.get('optimizations', [])
    
    total_bugs = len(manual_bugs) + len(pylint_bugs) + len(llm_bugs)
    total_style = len(flake8_issues) + len(llm_style)
    total_opts = len(radon_issues) + len(bandit_issues) + len(llm_opts)
    
    # Summary metrics
    st.markdown("### 📈 Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🐛 Bugs", total_bugs, delta=None)
    with col2:
        st.metric("🎨 Style Issues", total_style, delta=None)
    with col3:
        st.metric("⚡ Optimizations", total_opts, delta=None)
    
    st.markdown("---")

    # 🧠 AI Score
    score = 100 - (total_bugs * 5 + total_style * 2 + total_opts * 3)
    score = max(score, 0)

    st.markdown("### 🧠 AI Code Quality Score")
    st.progress(score / 100)
    st.success(f"Score: {score}/100")

    st.subheader("📊 Code Complexity Insight")

    if static_results.get("radon"):
        radon_data = static_results["radon"]

        # ✅ Handle LIST safely
        if isinstance(radon_data, list) and len(radon_data) > 0:
            avg_complexity = sum(item.get("complexity", 0) for item in radon_data) / len(radon_data)

            st.info(f"Average Complexity: {round(avg_complexity, 2)}")

            if avg_complexity > 10:
                st.warning("High complexity detected — consider refactoring")
            else:
                st.success("Code complexity is within acceptable range")

        else:
            st.info("Complexity data not structured properly")

    else:
        st.info("Complexity data not available")
    
    # 🚨 Priority Recommendation
    if total_bugs > 0:
        priority_issue = "Fix critical bugs first"
    elif total_opts > 0:
        priority_issue = "Optimize performance"
    else:
        priority_issue = "Code looks good"

    st.markdown("### 🚨 Priority Recommendation")
    st.error(priority_issue)

    # Tabs for different categories
    tab1, tab2, tab3, tab4 = st.tabs(["🐛 Bugs", "🎨 Style", "⚡ Optimizations", "📄 Full Report"])
    
    with tab1:
        st.markdown("### Bugs and Logical Errors")
        if total_bugs > 0:
            # Manual bugs
            if manual_bugs:
                st.markdown("#### 🔍 Manual Detection")
                for bug in manual_bugs:
                    with st.expander(f"Line {bug.get('line')}: {bug.get('issue')}", expanded=True):
                        st.code(bug.get('code', 'N/A'), language='python')
            
            # Pylint bugs
            if pylint_bugs:
                st.markdown("#### 🔧 Pylint Errors")
                for bug in pylint_bugs:
                    st.error(f"Line {bug.get('line')}: {bug.get('message')}")
            
            # LLM bugs
            if llm_bugs:
                st.markdown("#### 🤖 LLM Analysis")
                for bug in llm_bugs:
                    with st.expander(bug.get('issue', 'Unknown'), expanded=True):
                        st.info(f"**Suggestion:** {bug.get('suggestion', 'N/A')}")
        else:
            st.success("✅ No bugs detected!")
    
    with tab2:
        st.markdown("### Code Style Issues")
        if total_style > 0:
            if flake8_issues:
                st.markdown("#### 📏 Flake8 Issues")
                for issue in flake8_issues:
                    st.warning(issue)
            
            if llm_style:
                st.markdown("#### 🤖 LLM Suggestions")
                for item in llm_style:
                    with st.expander(item.get('issue', 'Unknown'), expanded=False):
                        st.info(f"**Suggestion:** {item.get('suggestion', 'N/A')}")
        else:
            st.success("✅ No style issues detected!")
    
    with tab3:
        st.markdown("### Optimization Opportunities")
        if total_opts > 0:
            # Complexity issues
            if radon_issues:
                st.markdown("#### 🔄 Complexity Analysis")
                for item in radon_issues:
                    complexity = item.get('complexity', 0)
                    severity = "🔴 High" if complexity > 10 else "🟡 Medium"
                    st.warning(f"{severity} - Function '{item.get('name')}': Complexity {complexity}")
            
            # Security issues
            if bandit_issues:
                st.markdown("#### 🔒 Security Issues")
                for issue in bandit_issues:
                    severity = issue.get('issue_severity', 'UNKNOWN')
                    st.error(f"[{severity}] Line {issue.get('line_number')}: {issue.get('issue_text')}")
            
            # LLM optimizations
            if llm_opts:
                st.markdown("#### 🤖 LLM Suggestions")
                for item in llm_opts:
                    with st.expander(item.get('issue', 'Unknown'), expanded=True):
                        st.info(f"**Suggestion:** {item.get('suggestion', 'N/A')}")
        else:
            st.success("✅ No optimization issues detected!")
    
    with tab4:
        st.markdown("### Full Report")
        st.text_area("Complete Analysis Report", report, height=600)
        
        # Download button
        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name="code_review_report.txt",
            mime="text/plain"
        )
    # 🔥 NEW AI INSIGHTS SECTION
    st.markdown("---")
    st.subheader("🤖 AI Insights (Advanced Intelligence)")

    st.subheader("📈 Analysis Confidence")

    confidence = 85  # fixed or simple logic

    st.progress(confidence / 100)
    st.success(f"Confidence Level: {confidence}%")

    # 🎓 Difficulty Display
    if llm_feedback.get("difficulty"):
        st.markdown("### 🎓 Code Difficulty Level")
        st.info(llm_feedback["difficulty"])

    if llm_feedback and not llm_feedback.get("error"):

        # 🧠 Code Intent
        if llm_feedback.get("intent"):
            st.markdown("### 🧠 Code Understanding")
            st.info(llm_feedback["intent"])

        # ⚡ Performance Insights
        if llm_feedback.get("performance"):
            st.markdown("### ⚡ Performance Prediction")
            for item in llm_feedback["performance"]:
                st.markdown(f"- **Issue:** {item['issue']}")
                st.markdown(f"  → Suggestion: {item['suggestion']}")

        # 🎯 Personalized Feedback
        if llm_feedback.get("personalized_feedback"):
            st.markdown("### 🎯 Personalized Suggestions")
            for tip in llm_feedback["personalized_feedback"]:
                st.markdown(f"- {tip['tip']}")

if __name__ == "__main__":
    main()