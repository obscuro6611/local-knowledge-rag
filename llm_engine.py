import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "llama3:latest"


def generate_answer(
    question,
    retrieved_chunks
):

    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    prompt = f"""
Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:

"I could not find that information in the knowledge base."

CONTEXT:

{context}

QUESTION:

{question}

ANSWER:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]