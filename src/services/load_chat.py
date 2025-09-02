import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.vector_store_service import LocalVectorStoreService

class ChatService:
    def __init__(self):
        """
        Initializes the ChatService.
        """
        self.rag_service = LocalVectorStoreService()

    def load_chat(self, user_input: str) -> str:
        """
        Searches for relevant information in the vector store and builds a prompt.
        """
        relevant_docs = self.rag_service.similarity_search(user_input, k=4)

        relevant_info = "\n\n".join([doc.page_content for doc in relevant_docs])

        prompt = f"""
        Você é um assistente de IA focado em ajudar Mestres de RPG. Seu objetivo é ser um co-piloto
        útil e bem-humorado, fornecendo informações precisas e insights criativos para o
        Mestre.

        Sua resposta deve ser baseada nos DOCUMENTOS DE REFERÊNCIA
        fornecidos abaixo. Não invente informações.

        Instruções:
        - Responda diretamente à pergunta.
        - Se a informação estiver incompleta ou não for encontrada nos documentos, diga "Desculpe, a informação não está na minha base de conhecimento."
        - Mantenha a resposta clara e concisa.
        - Use a sua criatividade de IA para sugerir ganchos de história ou curiosidades, se relevante e suportado pelos documentos.

        ---

        DOCUMENTOS DE REFERÊNCIA:
        {relevant_info}
        """

        return prompt
