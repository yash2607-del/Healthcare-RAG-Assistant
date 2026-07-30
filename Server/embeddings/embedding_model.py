from langchain_community.embeddings import HuggingFaceEmbeddings

class EmbeddingModel:
    def __init__(self, model_name: str = "all-mpnet-base-v2"):
        self.model_name = model_name
        print(f"Initializing embedding model: {self.model_name}")
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name
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
    print(f"\nTest embed_query(\"{test_text}\")")
    
    try:
        vector = embedder.embeddings.embed_query(test_text)
        print(f"Returns vector? {'Yes' if vector else 'No'}")
        print(f"Vector dimensions: {len(vector)}")
        print(f"First 5 dimensions: {vector[:5]}")
    except Exception as e:
        print(f"Error testing embeddings: {e}")
    print("Done.")
