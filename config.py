"""Insurellm demo corpus — fictional insurance company docs from LLM engineering course."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KNOWLEDGE_BASE_PATH = ROOT / "knowledge-base"
DB_NAME = str(ROOT / "chroma_db")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVAL_K = 8

# Hugging Face router (same pattern as Trend Research Agent)
HF_CHAT_MODEL = "moonshotai/Kimi-K2-Instruct-0905"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

COMPANY_NAME = "Insurellm"
