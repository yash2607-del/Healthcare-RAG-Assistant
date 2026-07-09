from langchain_community.embeddings import HuggingFaceEmbeddings

class EmbeddingModel:
    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5"):
        self.model_name = model_name
        print(f"Initializing embedding model: {self.model_name}")
        
        # We use LangChain's HuggingFaceEmbeddings which wraps the SentenceTransformer library.
        # This makes it natively compatible with LangChain documents and ChromaDB!
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            # BGE models require normalized embeddings for cosine similarity to work optimally
            encode_kwargs={'normalize_embeddings': True} 
        )
        
    def get_embeddings(self) -> HuggingFaceEmbeddings:
        """
        Returns the LangChain-compatible embeddings object, 
        ready to be passed to a VectorStore like Chroma.
        """
        return self.embeddings

if __name__ == "__main__":
    # Test the embedding model as shown in the screenshot
    embedder = EmbeddingModel()
    
    test_text = "CBC"
    print(f"\nTest encode(\"{test_text}\")")
    
    # embed_query is LangChain's wrapper around the model's encode() function
    vector = embedder.embeddings.embed_query(test_text)
    
    print(f"Returns vector? {'Yes' if vector else 'No'}")
    print(f"Vector dimensions: {len(vector)}")
    print(f"First 5 dimensions: {vector[:5]}")
    print("Done.")
