import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel

class VertexService:
    """
    Serviço que se conecta ao modelo Gemini Pro do Vertex AI.
    """
    def __init__(self):

        project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "seu-projeto-id") 
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel(model_name="gemini-pro")

    def generate_narrative(self, prompt: str) -> str:
        """
        Gera uma narrativa usando o modelo Gemini Pro.

        Args:
            prompt (str): O prompt completo, incluindo contexto e ação do jogador.

        Returns:
            str: A narrativa gerada pela IA.
        """
        print("Chamando a API do Gemini...")
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Erro na chamada da API: {e}")
            return "O Mestre de RPG está ocupado no momento. Tente novamente mais tarde."