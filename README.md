# Local Knowledge RAG

## Overview

Local Knowledge RAG is a Python application that indexes local documents and allows users to ask questions against their personal knowledge base.

The system uses vector embeddings and similarity search to retrieve relevant document chunks before generating an answer.

Responses include supporting source references from the indexed documents.

---

## Features

- Local document indexing
- Vector database search
- Retrieval-Augmented Generation (RAG)
- Source-aware answers
- Knowledge base persistence
- Export generated answers
- Support for PDF and DOCX documents

---

## Project Structure

```text
app.py
chunker.py
document_loader.py
embedding_engine.py
export_engine.py
llm_engine.py
retrieval_engine.py
vector_store.py

Knowledge_base/
sample_docs/
```

---

## Technologies

- Python
- FAISS
- Vector Embeddings
- Retrieval-Augmented Generation (RAG)
- Local Knowledge Base Storage

---

## How It Works

1. Load documents into the system.
2. Split documents into chunks.
3. Generate embeddings.
4. Store embeddings in a FAISS index.
5. Ask questions.
6. Retrieve relevant chunks.
7. Generate a response using retrieved context.
8. Display supporting sources.

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python app.py
```

---

## Example Workflow

1. Select a document folder.
2. Build the knowledge base index.
3. Enter a question.
4. Receive an answer.
5. Review retrieved source references.

---

## Future Improvements

Version 1 intentionally focuses on:

- Local indexing
- Question answering
- Source retrieval

Additional features such as OCR, memory, agents, and advanced workflows are planned for future versions.

---

## Author

Remé Marshall
