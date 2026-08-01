import os
import sys
from typing import List

# Ensure the Server directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
import re
from vectordb.chroma_client import ChromaClient

def ingest_pdf():
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'pdf', "Lord's Pathology Centre Information Final.pdf")
    print(f"Loading PDF file: {pdf_path}")
    
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    full_text = "\n".join([doc.page_content for doc in docs])
    
    # We will split the text perfectly by 'Centre ID:' or 'Centre  ID:'
    # The text contains lots of extra spaces due to PDF extraction
    # We use a regex to split exactly at the start of each centre
    chunks = []
    
    # Clean up double spaces for easier parsing, but keep newlines
    clean_text = re.sub(r' +', ' ', full_text)
    
    centre_splits = re.split(r'(Centre ID:.*?)(?=Centre ID:|$)', clean_text, flags=re.IGNORECASE | re.DOTALL)
    
    for split in centre_splits:
        split = split.strip()
        if not split.lower().startswith('centre id:'):
            continue
            
        # Extract state for metadata if possible
        state = "Unknown"
        state_match = re.search(r'State:\s*(.*?)\n', split, re.IGNORECASE)
        if state_match:
            state = state_match.group(1).strip()
            
        centre_match = re.search(r'Centre Name:\s*(.*?)\n', split, re.IGNORECASE)
        centre_name = centre_match.group(1).strip() if centre_match else "Unknown Centre"
        
        doc = Document(
            page_content=split,
            metadata={
                "source": "centre_info",
                "state": state,
                "centre": centre_name
            }
        )
        chunks.append(doc)
        
    print(f"Chunked PDF into {len(chunks)} distinct centres.")

    print("Adding chunks to Vector DB...")
    chroma_client = ChromaClient()
    chroma_client.ingest_documents(chunks)
    print("Successfully ingested PDF with Custom Heading Chunking!")

if __name__ == "__main__":
    ingest_pdf()
