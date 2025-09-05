import os
import sys
import json
from rank_bm25 import BM25Okapi
from typing import List, Dict

# Adiciona o diretório 'src' ao PATH para que o import funcione
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.vector_store_service import LocalVectorStoreService
from services.data_persistence_service import DataPersistenceService

class ChatService:
    def __init__(self):
        """
        Initializes the ChatService, preparing the semantic and lexical search services.
        """
        self.rag_service = LocalVectorStoreService()
        self.persistence_service = DataPersistenceService()

        self.bm25_index = self._create_bm25_index()

    def _create_bm25_index(self):
        """
        Loads pre-processed documents from the local file and creates a BM25 index.
        """
        print("Creating BM25 index from processed documents...")
        processed_documents = self.persistence_service.load_processed_documents()

        if not processed_documents:
            print("No processed documents found. BM25 index will not be created.")
            return None

        tokenized_corpus = [doc['page_content'].split(" ") for doc in processed_documents]
        bm25 = BM25Okapi(tokenized_corpus)

        print("BM25 index created successfully.")
        return {"index": bm25, "documents": processed_documents}

    def load_chat(self, user_input: str) -> str:
        """
        Searches for relevant information using Hybrid RAG and builds a prompt.
        """
        if not self.bm25_index:
            return "Error: The knowledge base was not loaded correctly."

        relevant_docs_sem = self.rag_service.similarity_search(user_input, k=3)

        tokenized_query = user_input.split(" ")
        bm25_docs_scores = self.bm25_index['index'].get_scores(tokenized_query)
        bm25_docs = [self.bm25_index['documents'][i] for i in bm25_docs_scores.argsort()[-3:][::-1]]

        combined_docs = relevant_docs_sem + bm25_docs

        unique_docs = []
        seen_page_content = set()
        for doc in combined_docs:
            if isinstance(doc, dict):
                page_content = doc.get('page_content', '')
            else:
                page_content = doc.page_content

            if page_content not in seen_page_content:
                unique_docs.append(doc)
                seen_page_content.add(page_content)

        relevant_info = ""
        for doc in unique_docs:
            if isinstance(doc, dict):
                relevant_info += doc.get('page_content', '') + "\n\n"
            else:
                relevant_info += doc.page_content + "\n\n"

        prompt = f"""
        Você é um assistente de IA focado em ajudar Mestres de RPG. Seu objetivo é ser um co-piloto
        útil e bem-humorado, fornecendo informações precisas e insights criativos para o
        Mestre.

        Sua resposta deve ser baseada **exclusivamente** nos DOCUMENTOS DE REFERÊNCIA
        fornecidos abaixo. Não invente informações.

        Instruções:
        - Responda diretamente à pergunta.
        - Se a informação estiver incompleta ou não for encontrada nos documentos, diga "Desculpe, a informação não está na minha base de conhecimento."
        - Mantenha a resposta clara e concisa.
        - Use a sua criatividade de IA para sugerir ganchos de história ou curiosidades, se relevante e suportado pelos documentos.

        ---

        DOCUMENTOS DE REFERÊNCIA:
        {relevant_info}

        ---

        Pergunta do Mestre: {user_input}
        """

        return prompt
