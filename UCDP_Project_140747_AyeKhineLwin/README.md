# 🏢 Enterprise AI & jMetal UCDP Solver

This is a Hybrid Optimization System that solves the Uncapacitated Facility Location Problem (UCDP) using **jMetalPy (Genetic Algorithm)** for mathematical optimization and **Ollama (Qwen2.5)** for business strategic analysis, wrapped in a **Streamlit** dashboard.

## 📁 Project Structure (Modular Architecture)
- `app_frontend.py`: Streamlit Dashboard UI
- `jmetal_backend.py`: jMetal Py Optimization Logic
- `ai_analyzer.py`: Ollama AI Connector for Business JSON Analysis

## 🛠️ How to Run Locally

1. Clone the Repository
```bash
git clone <your-github-repo-link>
cd UCDP_Project


2. Install Required Python Packages
Bash
pip install streamlit jmetalpy numpy scipy ollama


3. Setup AI Model (Ollama)
Ensure you have Ollama installed locally and run:

Bash
ollama run qwen2.5:3b



4. Run the Application
Bash
python -m streamlit run app_frontend.py