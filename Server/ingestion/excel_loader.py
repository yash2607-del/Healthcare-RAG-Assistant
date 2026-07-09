import os
import pandas as pd
from langchain_core.documents import Document
from typing import List


class ExcelLoader:
    """
    Loads diagnostic test data from an Excel file and converts
    each row into a LangChain Document with structured metadata.
    """

    def __init__(self, excel_path: str = None):
        if excel_path is None:
            # Default to Server/data/excel/<filename>
            base_dir = os.path.dirname(os.path.dirname(__file__))
            excel_path = os.path.join(
                base_dir,
                "data",
                "excel",
                "Lord Test MRP and DOS Complete Details copy.xlsx",
            )
        self.excel_path = excel_path

    def load_documents(self) -> List[Document]:
        """
        Reads all sheets from the Excel file, converts each row into a
        human-readable text block, and wraps it in a LangChain Document.
        """
        if not os.path.exists(self.excel_path):
            raise FileNotFoundError(
                f"Excel file not found at: {self.excel_path}"
            )

        print(f"Loading Excel file: {self.excel_path}")

        xl = pd.ExcelFile(self.excel_path)
        all_documents: List[Document] = []

        for sheet_name in xl.sheet_names:
            print(f"  Processing sheet: '{sheet_name}'")
            df = xl.parse(sheet_name)

            # Drop fully empty rows
            df.dropna(how="all", inplace=True)

            # Normalize column names (strip whitespace)
            df.columns = [str(c).strip() for c in df.columns]

            for idx, row in df.iterrows():
                # Build a natural-language text block from all columns
                parts = []
                for col in df.columns:
                    val = row.get(col)
                    if pd.notna(val) and str(val).strip():
                        parts.append(f"{col}: {str(val).strip()}")

                if not parts:
                    continue  # Skip empty rows

                page_content = "\n".join(parts)

                # Store raw row values as metadata for filtering later
                metadata = {
                    "sheet": sheet_name,
                    "row_index": int(idx),
                    "source": self.excel_path,
                }
                # Add all column values to metadata as well (useful for retrieval)
                for col in df.columns:
                    val = row.get(col)
                    if pd.notna(val):
                        metadata[col.lower().replace(" ", "_")] = str(val).strip()

                all_documents.append(
                    Document(page_content=page_content, metadata=metadata)
                )

        print(f"Total documents loaded: {len(all_documents)}")
        return all_documents


if __name__ == "__main__":
    loader = ExcelLoader()
    docs = loader.load_documents()
    print(f"\nSample document (first row):\n{docs[0].page_content}")
    print(f"\nMetadata: {docs[0].metadata}")
