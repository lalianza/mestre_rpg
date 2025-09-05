import os
import shutil  # Importe a biblioteca shutil para deletar diretórios
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

class LocalVectorStoreService:
    def __init__(self):
        self.persist_directory = "data/vector_store/"
        self.documents_directory = "data/documents/"
        self.embedding_function = OpenAIEmbeddings()

    def load_and_split_pdfs(self):
        """
        Loads all PDF files from the 'data/documents/' folder,
        splits the content into chunks, and returns the processed documents.
        """
        raw_documents = []
        if not os.path.exists(self.documents_directory):
            print(f"Document directory not found: {self.documents_directory}. Make sure the folder exists and contains PDFs.")
            return []

        for filename in os.listdir(self.documents_directory):
            if filename.endswith(".pdf"):
                file_path = os.path.join(self.documents_directory, filename)
                print(f"Loading {file_path}...")
                loader = PyPDFLoader(file_path)
                raw_documents.extend(loader.load())

        if not raw_documents:
            print("No PDF documents found. The vector store will not be created.")
            return []

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(raw_documents)
        return docs

    def create_and_persist_vector_store(self):
        """
        Deletes the old vector store and creates a new one from the loaded documents.
        """
        if os.path.exists(self.persist_directory):
            print(f"Old vector store found. Deleting {self.persist_directory}...")
            shutil.rmtree(self.persist_directory)

        print("Creating and persisting the vector store. This may take a few minutes...")
        documents = self.load_and_split_pdfs()

        if not documents:
            return None

        db = Chroma.from_documents(documents=documents, embedding=self.embedding_function, persist_directory=self.persist_directory)
        db.persist()
        print(f"Vector store created and saved at {self.persist_directory}")
        return db

    def load_existing_vector_store(self):
        """
        Loads the existing vector store from disk.
        """
        if not os.path.exists(self.persist_directory):
            print("Vector store directory not found. Creating a new one...")
            return self.create_and_persist_vector_store()

        print(f"Loading existing vector store from {self.persist_directory}")
        db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embedding_function)
        return db

    def similarity_search(self, query, k=6):
        """
        Performs a similarity search on the vector store.
        """
        db = self.load_existing_vector_store()
        if not db:
            return []

        print(f'Searching for relevant documents for: "{query}"...')
        docs = db.similarity_search(query, k=k)
        print(f'Relevant documents found.')
        return docs
