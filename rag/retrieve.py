from langchain_chroma import Chroma

from config import DB_NAME, RETRIEVAL_K
from rag.ingest import get_embeddings


def build_retrieval_query(question: str, history: list) -> str:
    if not history or len(question.split()) > 4:
        return question
    last = history[-1]
    if isinstance(last, (list, tuple)):
        prev_user = last[0] or ""
    else:
        prev_user = last.get("content", "") if last.get("role") == "user" else ""
    if not prev_user:
        return question
    return f"{prev_user} {question}".strip()


def retrieve(question: str, history: list | None = None):
    if history is None:
        history = []
    vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=get_embeddings())
    query = build_retrieval_query(question, history)
    results = vectorstore.similarity_search_with_relevance_scores(query, k=RETRIEVAL_K)
    docs = []
    for doc, score in results:
        doc.metadata["_score"] = float(score)
        docs.append(doc)
    return docs
