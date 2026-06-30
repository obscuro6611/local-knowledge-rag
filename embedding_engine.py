from sentence_transformers import SentenceTransformer
import numpy as np


MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


def get_model():

    global _model

    if _model is None:

        _model = SentenceTransformer(
            MODEL_NAME
        )

    return _model


def create_embeddings(
    chunks,
    progress_callback=None,
    batch_size=10
):

    model = get_model()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = []

    total = len(texts)

    for start in range(
        0,
        total,
        batch_size
    ):

        end = min(
            start + batch_size,
            total
        )

        batch = texts[start:end]

        batch_embeddings = model.encode(
            batch,
            show_progress_bar=False
        )

        embeddings.extend(
            batch_embeddings
        )

        if progress_callback:

            progress = (
                end / total
            ) * 100

            progress_callback(
                progress
            )

    return np.array(
        embeddings
    )