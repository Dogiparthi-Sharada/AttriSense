# RAG — retrieval-augmented generation

> *"Find me the exit interviews where people complained about compensation, in any language."* — RAG turns that into a vector search + LLM combo.

## The intuition

A pure LLM can hallucinate. A pure search engine can't summarise. RAG combines them:

```
1. user query           → "compensation issues"
2. embed the query      → 1536-dim vector
3. similarity search    → top-K most-similar exit interview chunks
4. (optional) feed K    → LLM with prompt: "answer using only these chunks"
5. response             → answer + citations
```

The model can only reference what was retrieved. Hallucination shrinks dramatically.

## The math, lightly

Embeddings map text to dense vectors:

$$
\text{embed}(\text{"raise was denied"}) = [-0.21, 0.47, \dots, 0.03] \in \mathbb{R}^{1536}
$$

Similarity is **cosine**:

$$
\text{cos}(a, b) = \frac{a \cdot b}{\|a\| \, \|b\|} \in [-1, 1]
$$

Multilingual embedding models (OpenAI's `text-embedding-3-small`, multilingual SBERT) place "compensation issues" (EN) and "problemas de compensación" (ES) close together in the same vector space — even though they share zero tokens.

A **vector database** (FAISS) indexes the corpus once, then answers `top_k(query, k=6)` in milliseconds.

## In AttriSense

- **Library**: LangChain + FAISS.
- **Where**: [`production/src/attrisense/multilingual_rag.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/multilingual_rag.py).
- **Two-tier embedding**:
  - **Tier 1**: OpenAI `text-embedding-3-small` (1536-dim) — high quality, requires reachable API.
  - **Tier 2** (fallback): hashing embeddings (256-dim, MD5 + Gaussian) — works fully offline.
- **Per-provider FAISS dirs** (`data/multilingual_index/openai/` vs `hashing/`) prevent dimension collisions.
- **Reachability probe** decides which tier to use, mid-query.

## The gotcha

**Retrieval ≠ truth.** RAG only retrieves what's in the corpus. If the corpus is biased, the answers will be biased. If the corpus is sparse, you'll get bad neighbours that look superficially relevant.

Hashing embeddings (the offline fallback) are **markedly worse** than OpenAI embeddings — they don't understand semantics, only token overlap. The dashboard surfaces the `provider` field so reviewers can see which tier served their query.

## Try it

```python
from attrisense.multilingual_rag import search

results = search("compensation issues", top_k=6)
for r in results:
    print(r["language"], r["theme"], round(r["score"], 3), r["text"][:60])
```
