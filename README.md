# 🎓 Peer-to-Peer Cohort Builder

A Streamlit and Ollama-powered application that matches learners into study cohorts based on their complementary skills, learning goals, and career objectives. It features a hybrid matching pipeline that combines a fast heuristic pre-filter with deep AI synergy analysis.

---

## 🚀 Key Features

*   **Hybrid Matching Pipeline:**
    1.  **Fast Heuristic Pre-filter:** Compares skill-need overlaps in pure Python to rank candidates and select top matches instantly.
    2.  **AI Synergy Engine:** Leverages a local LLM via Ollama to evaluate matches, compute synergy scores, and generate detailed cohort plans.
*   **Custom Learning Plans:** Outlines what each member can teach the other and suggests tailored capstone projects.
*   **Personalized Icebreakers:** Dynamically writes custom technical conversation starters to kickstart the cohort collaboration.
*   **Interactive Dashboard:** Interactive UI built with Streamlit featuring real-time statistics, progress indicators, and collapsible cohort plans.

---

## 🛠️ Tech Stack

*   **Frontend / UI:** Streamlit
*   **AI Engine:** Ollama (`gemma4:e2b` or similar)
*   **Language:** Python 3.8+

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/avinash1216/Study-Cohort.git
cd Study-Cohort
```

### 2. Install Dependencies
Make sure you have python and pip installed, then install the required libraries:
```bash
pip install streamlit requests
```

### 3. Set Up Ollama
1.  Download and install [Ollama](https://ollama.com/).
2.  Start the Ollama server.
3.  Pull the required model (defaults to `gemma4:e2b` in the codebase):
    ```bash
    ollama pull gemma4:e2b
    ```
    *(Note: If you use a different model tag, update the model field in [ai_engine.py](file:///d:/Avinash/Buildathon/ai_engine.py).)*

---

## 🏃 How to Run the Application

### Running the App
Start the Streamlit application:
```bash
streamlit run app.py
```
Open the provided local URL (typically `http://localhost:8501`) in your web browser.

### Running the CLI Test
To test the AI engine integration directly from the console, run:
```bash
python test_engine.py
```

---

## 📁 Project Structure

*   [app.py](file:///d:/Avinash/Buildathon/app.py): The main Streamlit dashboard application.
*   [ai_engine.py](file:///d:/Avinash/Buildathon/ai_engine.py): Integration with Ollama for candidate compatibility analysis.
*   [mock_data.py](file:///d:/Avinash/Buildathon/mock_data.py): Representative profiles used for testing matching logic.
*   [test_engine.py](file:///d:/Avinash/Buildathon/test_engine.py): Direct CLI runner for validating Ollama response parsing.
