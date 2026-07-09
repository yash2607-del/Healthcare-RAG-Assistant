import os
import sys
import pandas as pd
from langchain_core.documents import Document

# Ensure the Server directory is in the path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vectordb.chroma_client import ChromaClient

def ingest_excel(file_path):
    print(f"Loading data from {file_path}...")
    df = pd.read_excel(file_path)
    
    documents = []
    
    # Process each row into a text document
    for index, row in df.iterrows():
        if row.dropna().empty:
            continue
            
        content_lines = []
        for col_name, val in row.items():
            # Skip empty cells
            if pd.notna(val) and str(val).strip():
                content_lines.append(f"{col_name}: {val}")
                
        # Join the row data into a single text block
        page_content = "\n".join(content_lines)
        
        # Create a Langchain Document
        doc = Document(
            page_content=page_content,
            metadata={"source": os.path.basename(file_path), "row": index}
        )
        documents.append(doc)

    print(f"Created {len(documents)} document rows from Excel.")
    
    # Normally we'd chunk large documents, but Excel rows are already small chunks.
    # We will pass them directly to the database.
    
    print("Initializing ChromaDB connection...")
    chroma_client = ChromaClient()
    
    print("Adding documents to ChromaDB... (this might take a few minutes)")
    chroma_client.ingest_documents(documents)
    
    print("✅ Ingestion complete! The AI can now search this data.")

if __name__ == "__main__":
    # Define path to the Excel file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_path = os.path.join(base_dir, "data", "excel", "Lord Test MRP and DOS Complete Details copy.xlsx")
    
    if os.path.exists(excel_path):
        ingest_excel(excel_path)
    else:
        print(f"Error: Could not find excel file at {excel_path}")
