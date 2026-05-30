import os
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE, DB_NAME, EMBEDDING_MODEL, KNOWLEDGE_BASE_PATH


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=os.environ.get("EMBEDDING_MODEL", EMBEDDING_MODEL)
    )


def load_documents():
    loader = DirectoryLoader(
        str(KNOWLEDGE_BASE_PATH),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    return loader.load()


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def embed_and_store(chunks):
    embeddings = get_embeddings()
    db_path = Path(DB_NAME)
    if db_path.exists():
        existing = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)
        try:
            existing.delete_collection()
        except Exception:
            pass
    return Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=DB_NAME)


def run_ingest():
    documents = load_documents()
    chunks = chunk_documents(documents)
    embed_and_store(chunks)
    return len(documents), len(chunks)


def ensure_vector_db():
    marker = Path(DB_NAME) / ".ready"
    if marker.is_file():
        return
    run_ingest()
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("ok", encoding="utf-8")
