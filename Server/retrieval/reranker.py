from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

class BGEReranker:
    """
    Reranker using BAAI/bge-reranker-base cross-encoder.
    Cross-encoders score pairs of (query, document) and provide much better
    relevance scores than standard vector similarity.
    """
    def __init__(self, model_name="BAAI/bge-reranker-base", top_n=3):
        print(f"Initializing BGE Reranker with model: {model_name}")
        self.model = HuggingFaceCrossEncoder(model_name=model_name)
        self.compressor = CrossEncoderReranker(model=self.model, top_n=top_n)

    def get_compressor(self):
        """
        Returns the LangChain BaseDocumentCompressor to be used in a
        ContextualCompressionRetriever.
        """
        return self.compressor
