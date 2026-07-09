import os
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from embeddings.embedding_model import EmbeddingModel

class ChromaClient:
    def __init__(self, collection_name: str = "lord_diagnostics"):
        self.collection_name = collection_name
        
        # Determine the persist directory (Server/data/chroma)
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.persist_directory = os.path.join(base_dir, 'data', 'chroma')
        
        # Ensure directory exists
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize the embedding model
        self.embedding_model = EmbeddingModel()
        
        # Initialize the Chroma vector store
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding_model.get_embeddings(),
            persist_directory=self.persist_directory
        )

    def ingest_documents(self, documents: List[Document], batch_size: int = 500):
        """
        Ingests a list of LangChain documents into the Chroma vector store in batches.
        """
        print(f"Starting ingestion of {len(documents)} documents into ChromaDB...")
        
        # Process in batches to avoid overwhelming memory/Chroma
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            self.vector_store.add_documents(batch)
            print(f"Ingested batch {i // batch_size + 1} ({len(batch)} documents).")
            
        print(f"Successfully finished ingestion. Data is persisted to {self.persist_directory}")

    def as_retriever(self, search_kwargs=None):
        """
        Returns a LangChain retriever interface for the vector store.
        """
        if search_kwargs is None:
            search_kwargs = {"k": 5}
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)

if __name__ == "__main__":
    from ingestion.excel_loader import ExcelLoader
    from ingestion.chunker import DocumentChunker
    
    # 1. Load Documents
    base_dir = os.path.dirname(os.path.dirname(__file__))
    excel_path = os.path.join(base_dir, 'data', 'excel', 'Lord Test MRP and DOS Complete Details copy.xlsx')
    
    print("Step 1: Loading documents from Excel...")
    loader = ExcelLoader(excel_path)
    raw_docs = loader.load_documents()
    
    # 2. Chunk Documents
    print("Step 2: Chunking documents...")
    chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)
    chunked_docs = chunker.chunk_documents(raw_docs)
    
    # 3. Ingest into ChromaDB
    print("\nStep 3: Initializing ChromaDB and embedding model...")
    chroma_client = ChromaClient()
    
    print("\nStep 4: Ingesting chunks into Vector DB...")
    chroma_client.ingest_documents(chunked_docs)
    
    print("\nVector DB setup complete!")
