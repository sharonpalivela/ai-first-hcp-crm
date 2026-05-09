# AI First HCP CRM

An AI-powered CRM interaction logging system for pharmaceutical sales representatives.

This project enables users to log HCP (Healthcare Professional) interactions using conversational AI. The system extracts structured CRM fields, provides AI-powered suggestions, performs compliance checks, and stores interactions in a SQLite database.

---

# Features

## AI Interaction Logging
Users can describe interactions in natural language and the system automatically extracts:

- HCP Name
- Interaction Type
- Products Discussed
- Materials Shared
- Samples Distributed
- Sentiment
- Follow-Up Actions
- Summary

---

## AI Tools Implemented

### 1. Log Interaction Tool
Converts conversational notes into structured CRM fields.

### 2. Edit Interaction Tool
Updates only modified fields while preserving existing draft data.

### 3. HCP Profile Lookup Tool
Displays mock historical HCP profile information.

### 4. Suggest Next Action Tool
Generates AI-recommended next best actions for the sales rep.

### 5. Compliance Checker Tool
Detects potentially risky pharmaceutical claims such as:
- "guaranteed cure"
- "100% effective"
- "no side effects"

---

## Database Persistence

Interactions can be saved into a SQLite database using the "Save Interaction" feature.

---

# Tech Stack

## Frontend
- React
- Redux Toolkit
- Axios
- Vite

## Backend
- FastAPI
- SQLite
- SQLAlchemy

## AI / Orchestration
## AI / Orchestration
- LangGraph StateGraph
- Groq API
- Llama 3.3 70B Versatile

---

# Project Structure

```bash
ai-first-hcp-crm/
│
├── backend/
│   ├── app/
│   ├── crm.db
│   └── main.py
│
├── frontend/
│   ├── src/
│   └── package.json
│
└── README.md
```

---

# Setup Instructions

## Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend runs on:

```txt
http://127.0.0.1:8000
```

Swagger Docs:

```txt
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```txt
http://localhost:5173
```

---

# Example Interaction

User Input:

```txt
Met Dr. Rao today and discussed CardioX. Shared brochure and 2 samples. Doctor seemed positive. Follow up next Tuesday.
```

System Output:
- Extracted CRM fields
- Sentiment analysis
- Follow-up action
- Compliance evaluation

---

# AI Workflow

1. User enters interaction in conversational format.
2. Backend detects which tool should be triggered.
3. Structured draft is generated.
4. Redux updates frontend state.
5. User reviews interaction.
6. Interaction is saved into SQLite database.

---

# Notes

# Notes

The assignment originally referenced the `gemma2-9b-it` Groq model. Since the model has been deprecated and is no longer supported by Groq, the application uses `llama-3.3-70b-versatile` as the active fallback model.

LangGraph StateGraph is used to orchestrate tool routing and AI workflow execution. Groq LLM is used for interaction summarization and AI-assisted CRM processing.

---

# Future Improvements

- Real LLM-based extraction
- Authentication
- Persistent HCP profiles
- Interaction history dashboard
- Production deployment

---

# Author
Built as part of the AI First HCP CRM Assignment.