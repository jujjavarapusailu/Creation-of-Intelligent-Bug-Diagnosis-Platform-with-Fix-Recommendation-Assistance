# Milestone 1 - System Architecture

## 1. System Overview

The AI-Based Bug Analysis System is designed to automatically analyze submitted software bugs, error logs, and stack traces using multiple AI agents and historical defect information.

The system follows a multi-agent architecture where specialized AI agents perform different stages of bug analysis.

## 2. High-Level Architecture

User
↓
Bug Submission UI
↓
Backend API
↓
Bug Processing
↓
RAG Pipeline
↓
Historical Defect Knowledge Base
↓
Agent Orchestrator
↓
AI Agents
↓
Final Analysis Result
↓
User Interface

## 3. AI Agent Responsibilities

### 3.1 Triage Agent

The Triage Agent classifies the submitted bug based on:

- Severity: Critical, High, Medium, or Low
- Priority
- Affected software component
- Confidence score
- Reasoning for the classification

### 3.2 Log Analysis Agent

The Log Analysis Agent analyzes stack traces and error logs to identify:

- Exception type
- Failure point
- Affected code path
- Important error messages

### 3.3 Root Cause Agent

The Root Cause Agent analyzes the bug description, logs, and retrieved historical defects to identify the possible root cause of the problem.

### 3.4 Duplicate Detection Agent

The Duplicate Detection Agent compares the submitted bug with historical defects using semantic similarity and identifies potentially duplicate or similar bugs.

### 3.5 Remediation Agent

The Remediation Agent provides possible solutions, fixes, and recommendations based on the bug analysis and relevant historical defect information.

## 4. Agent Orchestrator

The Agent Orchestrator coordinates the execution of all AI agents.

It receives the submitted bug information, sends relevant context to each agent, and combines their outputs into a structured final analysis.

The general flow is:

Bug Submission
→ Triage Agent
→ Log Analysis Agent
→ Historical Defect Retrieval
→ Root Cause Agent
→ Duplicate Detection Agent
→ Remediation Agent
→ Final Analysis

## 5. Historical Defect Knowledge Base

The Historical Defect Knowledge Base stores previously reported software defects from public datasets such as Mozilla, Apache, and Eclipse.

The knowledge base will be used by the RAG pipeline to retrieve relevant historical defects during bug analysis.

### Knowledge Base Processing Flow

Historical Bug Datasets
→ Data Cleaning
→ Data Standardization
→ Document Chunking
→ Embedding Generation
→ Vector Database
→ Semantic Search
→ RAG Context

### Historical Defect Information

Each historical defect can contain:

- Bug ID
- Bug Title
- Bug Description
- Stack Trace
- Error Logs
- Comments
- Affected Component
- Severity
- Priority
- Resolution
- Status

## 6. Vector Database

The processed historical defect documents will be converted into embeddings and stored in a FAISS vector database.

When a new bug is submitted, its embedding will be compared with the stored historical defect embeddings.

The most similar historical defects will be retrieved and passed to the RAG pipeline as context.

## 7. Data Flow

1. User submits a bug report, stack trace, error log, or file.

2. Backend validates and processes the submitted information.

3. The bug information is converted into an embedding.

4. The vector database searches for similar historical defects.

5. Relevant historical defects are retrieved.

6. The Agent Orchestrator provides the required information to the AI agents.

7. The AI agents analyze the bug.

8. The system combines the agent outputs.

9. The final structured analysis is displayed to the user.

## 8. System Architecture Diagram

```mermaid
flowchart TD
    A[User] --> B[Bug Submission UI]

    B --> C[Backend API - FastAPI]

    C --> D[Bug Processing]

    D --> E[RAG Pipeline]

    E --> F[Embedding Model]
    F --> G[FAISS Vector Database]

    G --> H[Historical Defect Knowledge Base]

    D --> I[Agent Orchestrator]

    I --> J[Triage Agent]
    I --> K[Log Analysis Agent]
    I --> L[Root Cause Agent]
    I --> M[Duplicate Detection Agent]
    I --> N[Remediation Agent]

    H --> I

    J --> O[Final Analysis]
    K --> O
    L --> O
    M --> O
    N --> O

    O --> P[Results UI]
    P --> A

## 9. Data Model

### 9.1 Bug Report Schema

The Bug Report stores information about a newly submitted software defect.

| Field | Description |
|---|---|
| bug_id | Unique identifier for the bug |
| title | Short title of the bug |
| description | Detailed description of the problem |
| steps_to_reproduce | Steps required to reproduce the bug |
| expected_result | Expected system behavior |
| actual_result | Actual behavior observed |
| stack_trace | Stack trace related to the error |
| error_logs | Error or application logs |
| component | Affected software component |
| severity | Critical, High, Medium, or Low |
| priority | Priority of the bug |
| status | Current status of the bug |

### 9.2 Historical Defect Schema

The Historical Defect stores information about previously reported defects.

| Field | Description |
|---|---|
| defect_id | Unique identifier of the historical defect |
| title | Historical defect title |
| description | Defect description |
| stack_trace | Historical stack trace |
| comments | Developer or tester comments |
| component | Affected component |
| severity | Defect severity |
| priority | Defect priority |
| resolution | Solution or resolution applied |
| status | Final defect status |
| embedding | Vector representation of the defect |

### 9.3 Agent Output

Each AI agent produces structured information that can be passed to the Agent Orchestrator.

The final analysis can contain:

- Bug severity
- Bug priority
- Affected component
- Exception type
- Failure point
- Code path
- Possible root cause
- Similar historical defects
- Duplicate probability
- Recommended remediation
- Confidence scores
- Reasoning