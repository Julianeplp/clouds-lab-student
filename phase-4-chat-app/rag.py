"""Retrieval-Augmented Generation helpers — the two functions you implement.

Where they sit
--------------
Every ``POST /chat`` runs this chain (all in this folder):

    server.chat()                                   the request handler
      -> retrieval.retrieve(bq, table, message, k=3)
           -> retrieval.tokenize(message)           same tokenizer as Phase 3 -> terms match the table
           -> retrieval.query_tfidf(...)            SELECT term, doc_id, tfidf FROM <Phase-3 table>
                                                    WHERE term IN (the query's terms)
           -> rag.rank_topk(rows, k)                YOU: which k documents match best?
           -> retrieval.load_corpus()               doc_id -> text (Phase 3's deterministic split)
      -> rag.build_rag_prompt(message, texts)       YOU: put those texts in front of the question
      -> infer.generate(weights, prompt)            the Phase-2 model answers
      -> store.store_turn(...)                      record both turns

Worked example
--------------
Message: "the king and his crown". ``tokenize`` drops stop-words -> terms ``{king, his, crown}``.
BigQuery returns every row of the TF-IDF table for those three terms — say::

    ("king",  12, 4.1)   ("king",  7, 2.9)   ("crown", 12, 3.3)
    ("crown", 31, 3.0)   ("his",   7, 0.4)   ("his",   12, 0.4)

``rank_topk`` sums per document — doc 12: 7.8, doc 7: 3.3, doc 31: 3.0 — and returns
``[12, 7, 31]``. ``retrieve`` maps those ids to their text; ``build_rag_prompt`` produces::

    Context:
    <text of doc 12>

    <text of doc 7>

    <text of doc 31>

    User: the king and his crown
    Assistant:

Both functions are pure — lists in, lists/strings out, no I/O — which is why the offline unit
tests can grade them with hand-written rows and no BigQuery:

    python -m pytest phase-4-chat-app/tests/test_units.py -p autograder.points -q
"""

from __future__ import annotations


def rank_topk(tfidf_rows: list[tuple[str, int, float]], k: int = 3) -> list[int]:
    scores = {}

    for term, doc_id, tfidf in tfidf_rows:
        scores[doc_id] = scores.get(doc_id, 0.0) + tfidf

    ranked = sorted(
        scores,
        key=lambda doc_id: (-scores[doc_id], doc_id)
    )

    return ranked[:k]


def build_rag_prompt(query: str, context_texts: list[str]) -> str:
    context = "\n\n".join(context_texts)

    return f"Context:\n{context}\n\nUser: {query}\nAssistant:"
