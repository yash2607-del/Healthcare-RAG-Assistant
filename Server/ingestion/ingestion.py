"""
ingestion.py — Main ingestion pipeline entry point.

Run this script once to populate your ChromaDB vector store from the Excel data.

Usage (from the Server/ directory):
    python -m ingestion.ingestion

Or directly:
    python ingestion/ingestion.py
"""

import os
import sys

# Ensure the Server/ directory is in the path so sibling packages resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ingestion.excel_loader import ExcelLoader
from ingestion.chunker import DocumentChunker
from vectordb.chroma_client import ChromaClient


def run_ingestion(
    excel_path: str = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    batch_size: int = 500,
    collection_name: str = "lord_diagnostics",
):
    """
    Full ingestion pipeline:
      1. Load rows from Excel as LangChain Documents
      2. Chunk each document into smaller pieces
      3. Embed and store all chunks in ChromaDB

    Args:
        excel_path:       Path to the Excel file. Defaults to Server/data/excel/<file>.
        chunk_size:       Max characters per chunk.
        chunk_overlap:    Character overlap between consecutive chunks.
        batch_size:       Number of chunks to upsert per ChromaDB call.
        collection_name:  ChromaDB collection to write into.
    """

    print("=" * 60)
    print("  Lord Diagnostics AI — Ingestion Pipeline")
    print("=" * 60)

    # ── Step 1: Load ──────────────────────────────────────────────
    print("\n[Step 1/3] Loading Excel data...")
    loader = ExcelLoader(excel_path=excel_path)
    raw_docs = loader.load_documents()

    if not raw_docs:
        print("ERROR: No documents were loaded. Check your Excel file path.")
        return

    # ── Step 2: Chunk ─────────────────────────────────────────────
    print(f"\n[Step 2/3] Chunking {len(raw_docs)} documents...")
    chunker = DocumentChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = chunker.chunk_documents(raw_docs)

    # ── Step 3: Embed & Ingest ────────────────────────────────────
    print(f"\n[Step 3/3] Embedding and ingesting {len(chunks)} chunks into ChromaDB...")
    print("  (This may take several minutes on the first run — the embedding model")
    print("   needs to download and process all chunks.)\n")

    client = ChromaClient(collection_name=collection_name)
    client.ingest_documents(chunks, batch_size=batch_size)

    print("\n" + "=" * 60)
    print("  Ingestion complete!")
    print(f"  {len(chunks)} chunks stored in collection '{collection_name}'.")
    print("=" * 60)


if __name__ == "__main__":
    run_ingestion()
