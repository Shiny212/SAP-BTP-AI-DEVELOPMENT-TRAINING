# Resume Job Match Agent using LangGraph

## Overview

Resume Job Match Agent is an AI-powered application built using LangGraph and Google's Gemini model. It analyzes a candidate's resume against a job description, calculates a job fit score, identifies missing skills, recommends improvements, generates a learning roadmap, and creates a personalized cover letter for highly matched candidates.

---

## Features

- Resume Parsing
- Job Description Parsing
- Skill Matching
- Gap Analysis
- AI-based Fit Score Calculation
- Resume Improvement Suggestions
- Personalized Learning Roadmap
- AI-generated Cover Letter
- Human Review Step
- Memory of Previous Job Descriptions
- LangGraph Workflow
- Gemini 3.1 Flash Lite Integration

---

## Project Structure

```
Resume_Job_Match_Agent/
│
├── app.py
├── graph.py
├── state.py
├── config.py
├── prompts.py
├── logger.py
├── memory.py
├── requirements.txt
├── .env
├── README.md
│
├── data/
│   ├── sample_resume.txt
│   ├── sap_btp_ai_consultant.txt
│   ├── data_engineer.txt
│   └── sap_abap_developer.txt
│
├── nodes/
│
└── tools/
```

---

## Workflow

```
START
   │
   ▼
Input Validator
   │
   ▼
Resume Parser
   │
   ▼
Job Description Parser
   │
   ▼
Skill Matcher
   │
   ▼
Gap Analysis
   │
   ▼
Fit Score
   │
   ├───────────────┐
   │               │
   ▼               ▼
Human Review   Resume Improvement
   │               │
   ▼               │
Cover Letter       │
   │               │
   └──────┬────────┘
          ▼
Learning Roadmap (Low Fit)
          │
          ▼
Final Recommendation
          │
          ▼
END
```

---

## Technologies Used

- Python
- LangGraph
- LangChain
- Google Gemini 3.1 Flash Lite
- SQLite
- Git
- VS Code

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Configure API Key

Create a `.env` file.

```text
GOOGLE_API_KEY=YOUR_API_KEY
```

---

## Run the Project

```bash
python app.py
```

---

## Expected Output

The application generates:

- Parsed Resume
- Parsed Job Description
- Matched Skills
- Missing Skills
- Gap Analysis
- Fit Score
- Resume Suggestions
- Learning Roadmap
- Cover Letter (if applicable)
- Final Recommendation

---

## Future Enhancements

- PDF Resume Upload
- Streamlit Web Interface
- FAISS Vector Database
- Multiple LLM Support
- ATS Score
- Job Recommendation System

---

## Author

Shiny Belsiya
