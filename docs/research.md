# Milestone 1 - Research & Technical Understanding

## 1. Defect Analysis Workflow

### What is Defect Analysis?

Defect analysis is the process of understanding, investigating, and resolving software bugs.

### Defect Analysis Workflow

1. Bug Submission
2. Bug Validation
3. Bug Classification
4. Log Analysis
5. Historical Bug Search
6. Root Cause Analysis
7. Remediation
8. Final Report

## 2. RAG Architecture

### What is RAG?

RAG stands for Retrieval-Augmented Generation. It is a technique that combines information retrieval with a Large Language Model (LLM). Instead of depending only on the knowledge stored in the LLM, the system first retrieves relevant information from a knowledge base and provides it to the LLM to generate a better answer.

### RAG Workflow

1. User submits a new bug report.

2. The bug information is converted into an embedding.

3. The system searches the vector database for similar historical defects.

4. The most relevant historical bugs are retrieved.

5. The retrieved information is provided as context to the LLM.

6. The LLM analyzes the current bug using the submitted bug details and retrieved historical information.

7. The system generates a structured diagnosis and recommendation.

### RAG in Our Project

In this project, RAG will be used to retrieve similar historical bug reports from the Mozilla, Apache, and Eclipse defect datasets. The retrieved historical information will provide useful context to the AI agents for bug classification, root cause analysis, duplicate detection, and remediation recommendations.

## 3. Embeddings

### What are Embeddings?

Embeddings are numerical representations of text. They convert words, sentences, or documents into vectors that capture their meaning. Texts with similar meanings have similar vector representations.

### Why Embeddings are Used?

Embeddings help the system compare the meaning of different bug reports. They allow the system to find historical bugs that are semantically similar to a newly submitted bug, even when different words are used.

### Embeddings in Our Project

In this project, bug descriptions, stack traces, comments, and resolutions from historical defect datasets will be converted into embeddings. These embeddings will be stored in a vector database and used for semantic search and RAG-based retrieval.

### Example

New Bug:
"Application crashes when the user logs in."

Historical Bug:
"System fails during user authentication."

Although the wording is different, both bugs have a similar meaning. Embeddings help the system identify this semantic similarity.

## 4. Semantic Similarity and Vector Search

### What is Semantic Similarity?

Semantic similarity measures how similar two pieces of text are based on their meaning rather than only matching exact words.

### What is Vector Search?

Vector search finds the most similar vectors from a vector database by comparing the numerical representations of the text.

### Semantic Similarity in Our Project

In this project, a newly submitted bug will be converted into an embedding. The embedding will be compared with historical bug embeddings stored in the vector database. The system will retrieve the most semantically similar historical defects.

### Example

New Bug:
"Login page crashes with a null pointer error."

Historical Bug:
"Application throws NullPointerException during user authentication."

The system can identify these bugs as similar because their meanings are closely related, even though the wording is different.

### Purpose

Semantic similarity and vector search will be used mainly for duplicate bug detection and retrieving relevant historical defects for the RAG pipeline.

## 5. Bug Report Structure

### What is a Bug Report?

A bug report is a structured description of a software defect. It contains the information required to understand, reproduce, investigate, and resolve the defect.

### Common Bug Report Fields

A typical bug report can contain the following information:

- Bug ID
- Bug Title
- Bug Description
- Steps to Reproduce
- Expected Result
- Actual Result
- Stack Trace
- Error Logs
- Affected Component
- Severity
- Priority
- Comments
- Resolution
- Status

### Bug Report Structure in Our Project

The system will accept bug descriptions, stack traces, error logs, and uploaded bug report files. The submitted information will be validated, stored, and processed by the AI agents.

The structured bug information will also be used by the RAG pipeline to retrieve similar historical defects and provide relevant context to the AI agents.

### Example

Bug Title:
Login application crashes

Description:
The application crashes when the user clicks the login button.

Stack Trace:
NullPointerException at LoginService.java:45

Expected Result:
The user should be logged in successfully.

Actual Result:
The application crashes.

Affected Component:
Authentication

## 6. Technology Choices

### Proposed Technology Stack

The project will use the following technologies:

- Frontend: React.js
- Backend: Python with FastAPI
- Programming Language: Python
- LLM: OpenAI API
- Embedding Model: OpenAI Embeddings
- Vector Database: FAISS
- RAG Framework: LangChain
- Database: PostgreSQL
- Version Control: Git and GitHub

### Reason for Technology Selection

React.js will be used to build the bug submission and results interface.

Python and FastAPI will be used to develop the backend APIs and integrate the AI components.

OpenAI models will be used for language understanding and generating bug analysis results.

Embeddings will convert bug reports and historical defect information into numerical vectors.

FAISS will be used for efficient similarity search over historical bug embeddings.

LangChain will help implement the RAG pipeline and coordinate the interaction between retrieval and the LLM.

PostgreSQL will be used to store structured bug submission and application data.

Git and GitHub will be used for source code management and team collaboration.