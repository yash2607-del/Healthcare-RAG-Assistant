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
            if sheet_name.strip().lower() != 'external':
                print(f"  Skipping sheet: '{sheet_name}'")
                continue
                
            print(f"  Processing sheet: '{sheet_name}'")
            df = xl.parse(sheet_name)

            # Drop fully empty rows
            df.dropna(how="all", inplace=True)

            # Normalize column names (strip whitespace)
            df.columns = [str(c).strip() for c in df.columns]

            # Analyze row 0 for sub-headers and exclude B2B/P&L to avoid confusing the LLM with wrong prices
            sub_headers = df.iloc[0] if not df.empty else None
            
            col_definitions = []
            last_main_col = ""
            
            for col in df.columns:
                col_name = str(col).strip()
                sub = str(sub_headers.get(col, '')).strip() if sub_headers is not None else ''
                
                if not col_name.startswith('Unnamed:') and not col_name.startswith('Base Rate'):
                    if col_name not in ['Feb', 'Mar', 'Apr', 'Total']:
                        last_main_col = col_name
                
                include = True
                final_name = col_name
                
                if 'B2B' in sub.upper() or 'P&L' in sub.upper() or 'COUNT' in sub.upper() or 'NET MRP' in sub.upper():
                    include = False
                elif 'MRP' in sub.upper():
                    final_name = f"{last_main_col} MRP Price".strip()
                elif sub and sub != 'nan':
                    final_name = sub.title()
                elif col_name.startswith('Unnamed:'):
                    include = False
                    
                col_definitions.append({
                    'original': col,
                    'clean_name': final_name,
                    'include': include
                })

            # Skip the first row since it contains sub-headers
            df_data = df.iloc[1:]

            for idx, row in df_data.iterrows():
                # Build a natural-language text block from all columns
                parts = []
                for col_def in col_definitions:
                    if not col_def['include']:
                        continue
                        
                    val = row.get(col_def['original'])
                    # Ignore empty values and dashes
                    if pd.notna(val) and str(val).strip() and str(val).strip() != '-':
                        parts.append(f"{col_def['clean_name']}: {str(val).strip()}")

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
