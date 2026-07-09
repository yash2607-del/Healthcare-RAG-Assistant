from typing import Optional
import sys
import os

# Ensure the Server directory is in the path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_core.language_models.chat_models import BaseChatModel

from vectordb.chroma_client import ChromaClient
from retrieval.reranker import BGEReranker

class AdvancedRetriever:
    """
    Advanced Retriever that utilizes:
    1. Base retrieval from ChromaDB (fetching more candidates than needed).
    2. Optional Multi-Query generation to improve recall by querying from different angles.
    3. Cross-Encoder Reranking to sort candidates by actual relevance and cut down to top_k.
    """
    def __init__(self, chroma_client: Optional[ChromaClient] = None, llm: Optional[BaseChatModel] = None, initial_k: int = 5, final_k: int = 3):
        self.chroma_client = chroma_client or ChromaClient()
        
        # 1. Base Retriever: We retrieve a small pool of documents (initial_k) for fast processing
        self.base_retriever = self.chroma_client.as_retriever(search_kwargs={"k": initial_k})
            
        # 2. Reranker Setup
        self.reranker = BGEReranker(top_n=final_k)
        
        # Combine into a Contextual Compression Retriever
        self.retriever = ContextualCompressionRetriever(
            base_compressor=self.reranker.get_compressor(), 
            base_retriever=self.base_retriever
        )
        
    def get_retriever(self):
        return self.retriever
        
    def invoke(self, query: str):
        print(f"Executing advanced retrieval pipeline for: '{query}'")
        return self.retriever.invoke(query)
