import os
import sys
import json
from langchain_core.documents import Document

# Ensure the Server/ directory is in the path so sibling packages resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from vectordb.chroma_client import ChromaClient

def run_json_ingestion(
    json_path: str = None,
    batch_size: int = 500,
    collection_name: str = "lord_diagnostics",
):
    """
    Ingests the pre-chunked JSON centres data into ChromaDB.
    """
    if json_path is None:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, "data", "centres_chunks.json")

    print("=" * 60)
    print("  Lord Diagnostics AI — JSON Ingestion Pipeline")
    print("=" * 60)

    print(f"\n[Step 1/2] Loading JSON chunks from {json_path}...")
    if not os.path.exists(json_path):
        print("ERROR: JSON file not found!")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        chunks_data = json.load(f)

    documents = []
    for item in chunks_data:
        # Build page content to be rich for both embedding (search_text) and generation
        # We include the search_text at the top for vector similarity, and the full structured data for the LLM
        
        search_text = item.get('search_text', '')
        content_dict = item.get('content', {})
        
        page_content_lines = [
            f"Search Summary: {search_text}",
            "--- Detailed Information ---"
        ]
        
        for k, v in content_dict.items():
            if isinstance(v, list):
                v = ", ".join(str(i) for i in v)
            page_content_lines.append(f"{k.replace('_', ' ').title()}: {v}")
            
        page_content = "\n".join(page_content_lines)
        metadata = item.get('metadata', {})
        
        # Ensure metadata values are strings, ints, floats, or bools (ChromaDB requirement)
        clean_metadata = {}
        for k, v in metadata.items():
            if isinstance(v, (str, int, float, bool)):
                clean_metadata[k] = v
            else:
                clean_metadata[k] = str(v)
                
        doc = Document(page_content=page_content, metadata=clean_metadata)
        documents.append(doc)

    print(f"Loaded {len(documents)} pre-processed chunks.")

    print(f"\n[Step 2/2] Embedding and ingesting {len(documents)} chunks into ChromaDB...")
    client = ChromaClient(collection_name=collection_name)
    
    # We will reset the collection if it exists to avoid duplicates when testing
    try:
        # Some versions of Chroma allow resetting or deleting
        # If not, we just add to it.
        pass
    except Exception:
        pass
        
    client.ingest_documents(documents, batch_size=batch_size)

    print("\n" + "=" * 60)
    print("  JSON Ingestion complete!")
    print(f"  {len(documents)} chunks stored in collection '{collection_name}'.")
    print("=" * 60)

if __name__ == "__main__":
    run_json_ingestion()
