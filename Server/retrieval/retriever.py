from typing import Optional
import sys
import os

# Ensure the Server directory is in the path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.language_models.chat_models import BaseChatModel
from vectordb.chroma_client import ChromaClient

class AdvancedRetriever:
    """
    Fast Retriever that utilizes:
    1. Base retrieval from ChromaDB (fetching candidates).
    """
    def __init__(self, chroma_client: Optional[ChromaClient] = None, llm: Optional[BaseChatModel] = None, initial_k: int = 5, final_k: int = 15):
        self.chroma_client = chroma_client or ChromaClient()
        
        # 1. Base Retriever
        self.retriever = self.chroma_client.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        
    def get_retriever(self):
        return self.retriever
        
    def invoke(self, query: str):
        print(f"Executing fast retrieval pipeline for: '{query}'")
        return self.retriever.invoke(query)
