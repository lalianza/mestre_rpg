import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from services.vector_store_service import LocalVectorStoreService

def update_vector_store():
    """
    Updates the ChromaDB vector store, recreating it
    from the PDF documents in the 'data/documents/' folder.
    """
    service = LocalVectorStoreService()
    service.create_and_persist_vector_store()
    print("Updated with success")

if __name__ == "__main__":
    update_vector_store()
