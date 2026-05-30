#!/usr/bin/env python3
"""Smoke-test ingest + retrieval + answers. Run from docs-rag-space/: python scripts/test_rag.py"""
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from config import DB_NAME
from rag.answer import answer_question
from rag.ingest import run_ingest

TESTS = [
    {
        "q": "What is Insurellm and what does the company do?",
        "check": lambda a: "insurellm" in a and "insur" in a,
    },
    {
        "q": "Who is Marcus Johnson and what is his role?",
        "check": lambda a: "marcus" in a and ("customer success" in a or "success" in a),
    },
    {
        "q": "Name two insurance products from the knowledge base.",
        "check": lambda a: sum(
            1 for p in ("carllm", "bizllm", "homellm", "healthllm", "rellm", "claimllm", "markellm", "lifellm")
            if p in a
        )
        >= 2,
    },
]


def main():
    if not os.environ.get("HF_TOKEN"):
        print("FAIL: HF_TOKEN not set")
        sys.exit(1)
    if not os.environ.get("OPENAI_API_KEY"):
        print("WARN: OPENAI_API_KEY not set — using HF embeddings (needs sentence-transformers)")

    db = Path(DB_NAME)
    if db.exists():
        shutil.rmtree(db)

    print("Running ingest…")
    n_docs, n_chunks = run_ingest()
    print(f"  {n_docs} documents → {n_chunks} chunks\n")

    failed = 0
    for i, t in enumerate(TESTS, 1):
        print(f"--- Test {i}: {t['q']}")
        try:
            answer, docs = answer_question(t["q"], [])
            print(f"Retrieved {len(docs)} chunks")
            if docs:
                print(f"Top source: {Path(docs[0].metadata.get('source', '?')).name}")
            preview = answer[:450] + ("…" if len(answer) > 450 else "")
            print(f"Answer: {preview}\n")
            if t["check"](answer.lower()):
                print("  OK")
            else:
                print("  WARN: answer may be incomplete or off-corpus")
                failed += 1
        except Exception as e:
            print(f"  FAIL: {e}\n")
            failed += 1

    if failed:
        print(f"\n{failed} test(s) need review")
        sys.exit(1)
    print("\nAll tests passed.")


if __name__ == "__main__":
    main()
