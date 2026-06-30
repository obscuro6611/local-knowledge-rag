import json

import faiss
import numpy as np

from embedding_engine import get_model
from vector_store import (
    INDEX_PATH,
    METADATA_PATH
)


def retrieve_chunks(
    question,
    top_k=3
):

    index = faiss.read_index(
        str(INDEX_PATH)
    )

    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        chunks = json.load(file)

    model = get_model()

    query_embedding = model.encode(
        [question]
    )

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for index_position in indices[0]:

        if index_position < len(chunks):

            results.append(
                chunks[index_position]
            )

    return results