"""Multilingual exit-interview RAG.

Builds a FAISS index over synthetic exit-interview text in three
languages (English, Spanish, Hindi). Uses OpenAI embeddings when the
key is set AND the API is reachable; otherwise transparently falls
back to a deterministic in-process hashing model so the dashboard tab
keeps working in offline / firewalled environments.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
from langchain_core.embeddings import Embeddings

from attrisense.config import MULTILINGUAL_INDEX_DIR

logger = logging.getLogger(__name__)


SYNTHETIC_NOTES: tuple[tuple[str, str, str], ...] = (
    ("en", "training",
     "I was not fully trained on the optical assembly workflow."),
    ("es", "training",
     "No recib\u00ed suficiente capacitaci\u00f3n en el flujo de ensamblaje \u00f3ptico."),
    ("hi", "training",
     "Mujhe optical assembly workflow ke liye sahi training nahin mili thi."),
    ("en", "shifts",
     "Manufacturing shifts are difficult to sustain over months."),
    ("es", "shifts",
     "Los turnos de manufactura son dif\u00edciles de mantener durante meses."),
    ("hi", "shifts",
     "Manufacturing shifts long-term sustain karna mushkil ho gaya."),
    ("en", "manager",
     "My manager kept changing priorities every week."),
    ("es", "manager",
     "Mi gerente cambiaba las prioridades cada semana."),
    ("hi", "manager",
     "Manager har hafte priorities badal dete the."),
    ("en", "compensation",
     "Compensation lagged the rest of the engineering market."),
    ("es", "compensation",
     "La compensaci\u00f3n estaba por debajo del resto del mercado de ingenier\u00eda."),
    ("hi", "compensation",
     "Compensation industry standards se kaafi peeche thi."),
)


@dataclass
class HashingEmbeddings(Embeddings):
    """Deterministic, dependency-free fallback embeddings."""

    dimensions: int = 256

    def _vector(self, text: str) -> np.ndarray:
        text = text.lower()
        vector = np.zeros(self.dimensions, dtype=np.float32)
        for index in range(len(text) - 2):
            trigram = text[index:index + 3]
            slot = hash(trigram) % self.dimensions
            vector[slot] += 1.0
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm
        return vector

    def embed_documents(self, texts: Iterable[str]) -> list[list[float]]:
        return [self._vector(text).tolist() for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._vector(text).tolist()


def _try_openai_embeddings():
    """Return an OpenAIEmbeddings instance only if the API is reachable."""
    if not os.getenv("OPENAI_API_KEY"):
        return None
    try:
        from langchain_openai import OpenAIEmbeddings

        emb = OpenAIEmbeddings(
            model="text-embedding-3-small",
            timeout=5.0,
            max_retries=0,
        )
        emb.embed_query("ping")
        return emb
    except Exception as exc:  # noqa: BLE001 — degrade on any failure
        logger.warning("OpenAI embeddings unavailable, falling back to hashing: %s", exc)
        return None


def _build_embeddings() -> tuple[object, str]:
    openai_emb = _try_openai_embeddings()
    if openai_emb is not None:
        return openai_emb, "openai"
    return HashingEmbeddings(), "hashing"


def _index_dir_for(provider: str) -> Path:
    return MULTILINGUAL_INDEX_DIR / provider


def build_index(provider: str | None = None) -> str:
    from langchain_community.vectorstores import FAISS

    if provider is None:
        embeddings, provider = _build_embeddings()
    elif provider == "openai":
        emb = _try_openai_embeddings()
        if emb is None:
            raise RuntimeError("OpenAI embeddings requested but unreachable.")
        embeddings = emb
    else:
        embeddings = HashingEmbeddings()

    out_dir = _index_dir_for(provider)
    out_dir.mkdir(parents=True, exist_ok=True)

    texts = [text for _, _, text in SYNTHETIC_NOTES]
    metadatas = [
        {"language": language, "theme": theme}
        for language, theme, _ in SYNTHETIC_NOTES
    ]

    store = FAISS.from_texts(texts, embedding=embeddings, metadatas=metadatas)
    store.save_local(str(out_dir))
    return str(out_dir)


def search(query: str, top_k: int = 4) -> list[dict]:
    """Search the multilingual index. Falls back gracefully on connection errors."""
    from langchain_community.vectorstores import FAISS

    embeddings, provider = _build_embeddings()
    out_dir = _index_dir_for(provider)
    if not (out_dir / "index.faiss").exists():
        build_index(provider)

    store = FAISS.load_local(
        str(out_dir),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    try:
        results = store.similarity_search_with_score(query, k=top_k)
    except Exception as exc:  # noqa: BLE001
        if provider == "openai":
            logger.warning("OpenAI query failed, retrying with hashing: %s", exc)
            embeddings = HashingEmbeddings()
            provider = "hashing"
            out_dir = _index_dir_for(provider)
            if not (out_dir / "index.faiss").exists():
                build_index(provider)
            store = FAISS.load_local(
                str(out_dir),
                embeddings,
                allow_dangerous_deserialization=True,
            )
            results = store.similarity_search_with_score(query, k=top_k)
        else:
            raise

    return [
        {
            "text": doc.page_content,
            "language": doc.metadata.get("language", "?"),
            "theme": doc.metadata.get("theme", "?"),
            "score": float(score),
            "provider": provider,
        }
        for doc, score in results
    ]


if __name__ == "__main__":
    build_index()
    for hit in search("compensation issues", top_k=3):
        print(hit)
"""Multilingual exit-interview RAG.

Builds a FAISS index over synthetic exit-interview text in three
languages (English, Spanish, Hindi). Uses OpenAI embeddings when the
key is set AND the API is reachable; otherwise transparently falls
back to a deterministic in-process hashing model so the dashboard tab
keeps working in offline / firewalled environments.
"""

