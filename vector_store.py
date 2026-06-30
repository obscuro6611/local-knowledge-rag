import json
from pathlib import Path
from datetime import datetime

import faiss
import numpy as np


KNOWLEDGE_BASE_DIR = Path("knowledge_base")

INDEX_PATH = KNOWLEDGE_BASE_DIR / "index.faiss"
METADATA_PATH = KNOWLEDGE_BASE_DIR / "metadata.json"
INFO_PATH = KNOWLEDGE_BASE_DIR / "kb_info.json"


def save_vector_store(
    embeddings,
    chunks,
    model_name
):

    KNOWLEDGE_BASE_DIR.mkdir(
        exist_ok=True
    )

    vectors = np.array(
        embeddings,
        dtype="float32"
    )

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(vectors)

    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            indent=2,
            ensure_ascii=False
        )

    info = {
        "documents": len(
            set(
                chunk["filename"]
                for chunk in chunks
            )
        ),
        "chunks": len(chunks),
        "embedding_model": model_name,
        "last_build_time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    with open(
        INFO_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            info,
            file,
            indent=2
        )


def vector_store_exists():

    return (
        INDEX_PATH.exists()
        and METADATA_PATH.exists()
        and INFO_PATH.exists()
    )