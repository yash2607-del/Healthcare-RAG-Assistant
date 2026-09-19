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
    
    # The text contains newlines between almost every word due to PDF extraction
    # We will normalize all whitespace to single spaces first
    clean_text = re.sub(r'\s+', ' ', full_text)
    
    # Now we split by "Centre ID:"
    # Note: re.split with a capture group keeps the delimiter in the list
    centre_splits = re.split(r'(Centre ID:)', clean_text, flags=re.IGNORECASE)
    
    # Combine the delimiter and the text
    chunks = []
    for i in range(1, len(centre_splits), 2):
        if i + 1 < len(centre_splits):
            split_text = centre_splits[i] + centre_splits[i+1]
        else:
            split_text = centre_splits[i]
            
        split_text = split_text.strip()
        
        # Extract state
        state = "Unknown"
        state_match = re.search(r'State:\s*(.*?)\s*(?:City:|Service Type:|Trust Indicator:)', split_text, re.IGNORECASE)
        if state_match:
            state = state_match.group(1).strip()
            
        # Extract centre name
        centre_name = "Unknown Centre"
        centre_match = re.search(r'Centre Name:\s*(.*?)\s*State:', split_text, re.IGNORECASE)
        if centre_match:
            centre_name = centre_match.group(1).strip()
            
        doc = Document(
            page_content=split_text,
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
