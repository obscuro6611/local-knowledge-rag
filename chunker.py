def create_chunks(
    documents,
    chunk_size=500,
    overlap=100
):

    chunks = []

    for document in documents:

        text = document.get("text", "")

        if not text.strip():
            continue

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append(
                {
                    "filename": document["filename"],
                    "text": chunk_text
                }
            )

            start += (chunk_size - overlap)

    return chunks