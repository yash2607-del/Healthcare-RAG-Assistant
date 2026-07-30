from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List


class DocumentChunker:
    """
    Splits large LangChain Documents into smaller, overlapping chunks
    so they fit within the embedding model's context window and improve
    retrieval precision.
    
    Strategy: RecursiveCharacterTextSplitter tries to split on paragraph
    breaks → newlines → spaces before falling back to hard character splits.
    This keeps semantically related content together as much as possible.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Args:
            chunk_size:    Max number of characters per chunk.
            chunk_overlap: Number of characters to overlap between consecutive
                           chunks so context is not lost at boundaries.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            # Prefer splitting on newlines since our rows use newline-separated fields
            separators=["\n\n", "\n", " ", ""],
            length_function=len,
        )

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Splits a list of Documents into chunks and carries over all metadata
        from the parent document.

        Returns:
            A flat list of chunked LangChain Documents.
        """
        print(
            f"Chunking {len(documents)} documents "
            f"(chunk_size={self.chunk_size}, overlap={self.chunk_overlap})..."
        )

        chunked_docs = self.splitter.split_documents(documents)

        print(f"Total chunks produced: {len(chunked_docs)}")
        return chunked_docs


if __name__ == "__main__":
    from ingestion.excel_loader import ExcelLoader

    loader = ExcelLoader()
    raw_docs = loader.load_documents()

    chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)
    chunks = chunker.chunk_documents(raw_docs)

    print(f"\nSample chunk:\n{chunks[0].page_content}")
    print(f"\nChunk metadata: {chunks[0].metadata}")
