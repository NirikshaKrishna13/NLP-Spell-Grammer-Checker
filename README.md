# ✍️ NLP-Based Grammar and Spell Checker

An intelligent **Grammar and Spell Checking application** built using **Natural Language Processing (NLP)** techniques. The application analyzes user-provided text, identifies spelling and common grammar errors, and provides correction suggestions through an interactive Streamlit interface.

---

## 🚀 Features

- 🔤 **Spelling Error Detection**
- ✏️ **Spelling Correction Suggestions**
- 📝 **Grammar Error Detection**
- ✅ **Automatic Corrected Text Generation**
- 🔍 **Text Tokenization**
- 🏷️ **Part-of-Speech (POS) Tagging**
- 📊 **Text Statistics**
- ⚡ **Real-Time Text Analysis**
- 🖥️ **Interactive Streamlit Web Interface**
- 🔒 **Runs Locally**
- ☁️ **No Cloud LLM or API Key Required**

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| NLTK | Dictionary-based spelling analysis and NLP resources |
| spaCy | Tokenization, POS tagging and linguistic analysis |
| Streamlit | Interactive web application |
| Pandas | Displaying linguistic analysis results |
| Regular Expressions | Grammar and text pattern detection |
| Git & GitHub | Version control and project hosting |

---

## 🧠 NLP Pipeline

The application follows the following NLP pipeline:

```text
                User Input
                    │
                    ▼
            Text Preprocessing
                    │
                    ▼
               Tokenization
                    │
                    ▼
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
    Spell Checking       Grammar Checking
          │                   │
          ▼                   ▼
   Word Dictionary       Grammar Rules
          │                   │
          └─────────┬─────────┘
                    ▼
             Error Detection
                    │
                    ▼
             Suggestions
                    │
                    ▼
           Corrected Text
                    │
                    ▼
             Streamlit UI
