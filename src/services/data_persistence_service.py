import os
import json
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DataPersistenceService:
    def __init__(self):
        self.documents_directory = "data/documents/"
        self.processed_data_file = "data/processed_documents/processed_documents.json"

    def _load_and_split_pdfs(self) -> List[Dict]:
        """
        Loads all PDF files, splits the content, and returns a list of dictionaries.
        """
        raw_documents = []
        if not os.path.exists(self.documents_directory):
            print(f"Document directory not found: {self.documents_directory}. Make sure it exists and contains PDFs.")
            return []

        for filename in os.listdir(self.documents_directory):
            if filename.endswith(".pdf"):
                file_path = os.path.join(self.documents_directory, filename)
                print(f"Loading {file_path}...")
                loader = PyPDFLoader(file_path)
                raw_documents.extend(loader.load())

        if not raw_documents:
            print("No PDF documents found. No data will be saved.")
            return []

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(raw_documents)

        processed_docs = [
            {"page_content": doc.page_content, "metadata": doc.metadata}
            for doc in docs
        ]
        return processed_docs

    def process_and_save_documents(self):
        """
        Processes the documents and saves them to a local JSON file.
        Deletes the old file if it exists.
        """
        print("Processing and saving documents to local file...")

        if os.path.exists(self.processed_data_file):
            print(f"Old file found. Deleting {self.processed_data_file}...")
            os.remove(self.processed_data_file)

        documents = self._load_and_split_pdfs()

        if documents:
            os.makedirs(os.path.dirname(self.processed_data_file), exist_ok=True)
            with open(self.processed_data_file, 'w') as f:
                json.dump(documents, f, indent=2)
            print(f"Documents processed and saved to {self.processed_data_file}")
        else:
            print("No documents to save. Operation cancelled.")

    def load_processed_documents(self) -> List[Dict]:
        """
        Loads the processed documents from the local JSON file.
        """
        if not os.path.exists(self.processed_data_file):
            print(f"Processed data file not found at {self.processed_data_file}. Please run 'update_vector_store.py' first.")
            return []

        print(f"Loading processed documents from {self.processed_data_file}")
        with open(self.processed_data_file, 'r') as f:
            documents = json.load(f)

        return documents
