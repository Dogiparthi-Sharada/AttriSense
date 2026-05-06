"""Build the FAISS index used for semantic exit-interview search."""

from __future__ import annotations

import os

import pandas as pd
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

from config import DATASET_PATH, FAISS_INDEX_DIR


def load_exit_interviews() -> list[str]:
    """Read only the exit interview text for employees who actually left.

    Returns:
        A list of text snippets that can be embedded into FAISS.
    """
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Missing {DATASET_PATH.name}. Run `python generate_demo_workforce_data.py` first."
        )

    df = pd.read_csv(DATASET_PATH)
    return (
        df.loc[df["Voluntary_Turnover"] == "Yes", "Exit_Interview"]
        .dropna()
        .astype(str)
        .tolist()
    )


def build_index(exit_interviews: list[str]) -> None:
    """Create and save a local FAISS vector index from exit interview text.

    Args:
        exit_interviews: Text records to split, embed, and store.
    """
    if not exit_interviews:
        raise ValueError("No exit interviews found to vectorize.")

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required to build the FAISS index.")

    # Small chunks work well here because synthetic exit interviews are short.
    # The overlap preserves a little context when a sentence crosses boundaries.
    splitter = CharacterTextSplitter(chunk_size=150, chunk_overlap=20)
    documents = splitter.create_documents(exit_interviews)

    # FAISS stores vectors locally. This keeps the demo easy to run without a
    # separate vector database service.
    vector_store = FAISS.from_documents(documents, OpenAIEmbeddings())
    vector_store.save_local(str(FAISS_INDEX_DIR))


def main() -> None:
    """Build the optional RAG index used for semantic exit-interview search."""
    load_dotenv(override=True)
    exit_interviews = load_exit_interviews()
    build_index(exit_interviews)
    print(
        f"Saved FAISS index with {len(exit_interviews):,} source interviews to "
        f"{FAISS_INDEX_DIR.name}/."
    )


if __name__ == "__main__":
    main()
