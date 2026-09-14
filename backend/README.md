# AI-Based Bug Analysis System

## Project Overview

The AI-Based Bug Analysis System is a software defect analysis system that analyzes bug reports, stack traces, and error logs using multiple analysis agents and a historical defect knowledge base.

The system helps identify:

- Bug severity
- Bug priority
- Affected component
- Exception type
- Failure point
- Possible root cause
- Similar historical bugs
- Recommended remediation steps

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Sentence Transformers
- FAISS
- NumPy
- Pytest
- HTML
- CSS
- JavaScript

## AI Agents

### 1. Triage Agent

Classifies the submitted bug based on:

- Severity
- Priority
- Affected component
- Confidence score
- Reasoning

### 2. Log Analysis Agent

Analyzes stack traces and error logs to identify:

- Exception type
- Error message
- Failure point
- Code path
- Confidence score

### 3. Root Cause Agent

Uses semantic retrieval from the historical defect knowledge base to generate:

- Root cause hypothesis
- Confidence score
- Supporting historical evidence
- Reasoning

### 4. Duplicate Detection Agent

Uses semantic similarity to find similar historical defects.

It classifies results as:

- Duplicate
- Related
- New/Unmatched

### 5. Remediation Agent

Generates actionable recommendations based on:

- Triage results
- Log analysis
- Root cause analysis
- Historical similarity
- General software engineering best practices

## RAG / Knowledge Base

The project uses:

- Sentence Transformer embeddings
- `all-MiniLM-L6-v2`
- FAISS vector search
- Historical Mozilla bug data

The current development seed contains cleaned and embedded historical bug records.

## Project Structure

```text
AI-Bug-Analysis-System/
│
├── docs/
│   ├── research.md
│   └── architecture.md
│
├── backend/
│   ├── main.py
│   ├── process_dataset.py
│   ├── create_embeddings.py
│   ├── search_bugs.py
│   ├── triage_agent.py
│   ├── log_analysis_agent.py
│   ├── root_cause_agent.py
│   ├── duplicate_detection_agent.py
│   ├── remediation_agent.py
│   ├── orchestrator.py
│   ├── test_triage.py
│   ├── test_log_analysis.py
│   ├── test_orchestrator.py
│   ├── test_root_cause.py
│   ├── test_duplicate_detection.py
│   ├── test_remediation.py
│   ├── requirements.txt
│   └── README.md
│
├── datasets/
│   └── mozilla/
│
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js