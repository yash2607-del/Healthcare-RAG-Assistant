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
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'pdf', "Lord's Pathology Centre Information.pdf")
    print(f"Loading PDF file: {pdf_path}")
    
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    full_text = "\n".join([doc.page_content for doc in docs])
    
    states = ["Andhra Pradesh", "Goa", "Gujarat", "Karnataka", "Maharashtra"]
    
    # We will manually split the text by finding where each state section starts
    chunks = []
    
    for i, state in enumerate(states):
        # Allow multiple spaces within the state name (e.g. "Andhra  Pradesh")
        state_regex = state.replace(' ', r'\s+')
        # Find start index of this state
        pattern = re.compile(rf"{state_regex}\s*\(\d+\s*Centres\)", re.IGNORECASE)
        match = pattern.search(full_text)
        
        if not match:
            print(f"Could not find section for {state}")
            continue
            
        start_idx = match.start()
        
        # Find end index (start of next state, or end of text)
        end_idx = len(full_text)
        if i + 1 < len(states):
            next_state = states[i + 1]
            next_state_regex = next_state.replace(' ', r'\s+')
            next_pattern = re.compile(rf"{next_state_regex}\s*\(\d+\s*Centres\)", re.IGNORECASE)
            next_match = next_pattern.search(full_text[start_idx+1:])
            if next_match:
                end_idx = start_idx + 1 + next_match.start()
        else:
            # Last state, ends at "Overall  Network  Summary"
            summary_pattern = re.compile(r"Overall\s*Network\s*Summary", re.IGNORECASE)
            summary_match = summary_pattern.search(full_text[start_idx:])
            if summary_match:
                end_idx = start_idx + summary_match.start()
                
        state_text = full_text[start_idx:end_idx].strip()
        
        # Split the state text exactly by 'Centre \d+', 'Center \d+', or '\d+. Lord's Pathology'
        # This ensures one chunk = one centre, with all contact details perfectly preserved
        centre_splits = re.split(r'(Cent(?:re|er)\s+\d+|\d+\.\s*Lord\'s\s+Pathology)', state_text, flags=re.IGNORECASE)
        
        # re.split keeps the delimiters if captured in groups, so centre_splits will look like:
        # [ "intro text...", "Centre 1", " \nCentre Name...", "Centre 2", " \nCentre Name..." ]
        
        # If there's intro text before the first centre, we can optionally store it or skip it
        # We'll iterate through the splits and combine the "Centre X" with its subsequent details
        
        centre_chunks = []
        for j in range(1, len(centre_splits), 2):
            centre_title = centre_splits[j].strip()
            centre_details = centre_splits[j+1].strip()
            
            # Create a perfect, self-contained chunk for this specific centre
            chunk_text = f"State: {state}\n{centre_title}\n{centre_details}"
            
            doc = Document(
                page_content=chunk_text,
                metadata={
                    "source": "centre_info",
                    "state": state,
                    "centre": centre_title
                }
            )
            chunks.append(doc)
            centre_chunks.append(chunk_text)
            
        print(f"Chunked {state} into {len(centre_chunks)} distinct centres.")

    print("Adding chunks to Vector DB...")
    chroma_client = ChromaClient()
    chroma_client.ingest_documents(chunks)
    print("Successfully ingested PDF with Custom Heading Chunking!")

if __name__ == "__main__":
    ingest_pdf()
