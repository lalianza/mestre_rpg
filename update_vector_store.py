import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from services.data_persistence_service import DataPersistenceService
from services.vector_store_service import LocalVectorStoreService

def update_data_stores():
    """
    Orchestrates the data processing and persistence for the project.
    It processes raw PDFs, saves them locally, and then creates the vector store.
    """
    print("--- Starting data store update process ---")

    persistence_service = DataPersistenceService()
    persistence_service.process_and_save_documents()

    vector_store_service = LocalVectorStoreService()
    vector_store_service.create_and_persist_vector_store()

    print("--- Data store update process completed successfully! ---")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Erro: A variável de ambiente OPENAI_API_KEY não está configurada.")
        print("Certifique-se de que sua chave está no arquivo .env na raiz do projeto.")
    else:
        update_data_stores()
