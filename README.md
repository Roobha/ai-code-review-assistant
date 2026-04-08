# 🧠 Adaptive AI Code Review System

An advanced AI-powered system for analyzing Python code with **code understanding, performance prediction, and personalized feedback** — designed to go beyond traditional static analysis tools.

---

## 🚀 Overview

This project transforms conventional code review into an **intelligent, adaptive, and insight-driven process** by combining:

* 🔍 Static Analysis
* 🧠 AI-powered Code Understanding
* ⚡ Performance Prediction
* 🎯 Personalized Feedback Engine

Unlike traditional analyzers, this system delivers **context-aware insights** and simulates **adaptive intelligence**, aligning with modern AI-assisted development tools.

---

## ✨ Key Features

### 🧠 Code Understanding Engine

* Interprets what the code is doing
* Generates high-level intent explanations

> Example: *“This code defines functions and performs logical operations.”*

---

### ⚡ Performance Prediction

* Detects inefficient patterns (e.g., nested loops)
* Predicts time complexity issues (e.g., O(n²))

---

### 🎯 Personalized Feedback System

* Adapts suggestions based on user level (Beginner / Advanced)
* Provides actionable, targeted improvements

---

### 📊 AI Code Quality Score

* Scores code quality (0–100)
* Based on bugs, style, complexity, and performance

---

### 📈 Code Complexity Insight

* Uses Radon metrics
* Classifies code as optimal or high complexity

---

### 🚨 Priority Recommendation Engine

* Highlights the most critical action:

  * Fix bugs
  * Optimize performance
  * Improve maintainability

---

### 🔍 Hybrid Analysis System

Combines multiple industry-standard tools:

* **Pylint** → Code correctness
* **Flake8** → Style enforcement
* **Radon** → Complexity analysis
* **Bandit** → Security scanning

---

### 🤖 AI-Powered Review (Gemini Integration)

* Provides intelligent, context-aware insights
* Detects nuanced bugs and optimization opportunities
* Generates human-like explanations

> Enhances static analysis with deeper reasoning and contextual intelligence

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** (Web UI)
* **Pylint, Flake8, Radon, Bandit**
* **Google Gemini API (LLM Integration)**

---

## ⚙️ System Architecture

```
User Code Input
      ↓
Static Analysis Layer (Pylint, Flake8, Radon, Bandit)
      ↓
AI Understanding Layer (Gemini / Logic Engine)
      ↓
Adaptive Feedback Engine
      ↓
Final Report (Score + Insights + Recommendations)
```

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧪 Usage Options

### 💻 CLI Mode

```bash
python main.py sample_bad_code.py
```

* Generates console output
* Saves report in `/reports`

---

### 🌐 Web Interface (Streamlit)

```bash
streamlit run app.py
```

Features:

* Upload or paste code
* Interactive analysis dashboard
* Downloadable reports

---

## 📊 Example Output

* 🧠 Code Intent Explanation
* ⚡ Performance Warnings
* 🎯 Personalized Suggestions
* 📊 Code Quality Score
* 📈 Complexity Analysis

---

## 💡 Innovation

This system introduces a **lightweight adaptive AI layer** that:

* Understands code behavior
* Predicts future issues
* Provides contextual recommendations
* Simulates intelligent code review systems

> Designed as a foundation for next-generation AI developer tools

---

## 📁 Project Structure

```
code-review-analyzer/
├── main.py
├── app.py
├── config.py
├── static_analyzer.py
├── llm_integrator.py
├── report_generator.py
├── requirements.txt
├── sample_bad_code.py
└── reports/
```

---

## ⚠️ Setup (Optional - Gemini API)

Set API key:

```bash
# Windows
set GEMINI_API_KEY=your_api_key

# Linux/Mac
export GEMINI_API_KEY=your_api_key
```

---

## 📌 Future Enhancements

* 🔄 User behavior tracking (adaptive learning system)
* 🌐 Multi-language support
* 🤖 Advanced LLM integration
* 📊 Analytics dashboard
* ☁️ Cloud deployment

---

## 🙏 Acknowledgments

* Built with **Pylint, Flake8, Radon, and Bandit**
* AI powered by **Google Gemini**
* UI built with **Streamlit**

---

## 👩‍💻 Author

**Roobhasri S**
B.Tech Artificial Intelligence & Data Science

---

## 🎯 Project Vision

> “To transform code review from rule-based checking into an intelligent, adaptive, and insight-driven system.”

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub!

---

**Happy Coding! 🚀**
