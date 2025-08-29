import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

# Importa as classes dos serviços
from src.services.local_db_service import LocalDbService
from src.services.rag_service import LocalRAGService # << CORRIGIDO AQUI
from src.services.vertex_service import VertexService

app = FastAPI()

# Inicializa os serviços
local_db_service = LocalDbService()
rag_service = LocalRAGService() # << CORRIGIDO AQUI
vertex_service = VertexService()

class PlayerInput(BaseModel):
    player_id: str
    message: str
    history: List[Dict[str, str]] = []


@app.on_event("startup")
async def startup_event():
    """
    Evento que é executado na inicialização do servidor.
    Popula a base de conhecimento do RAG.
    """
    print("Inicializando e populando a base de conhecimento do RAG...")
    try:
        rag_service.load_knowledge_base()
    except Exception as e:
        print(f"Erro ao carregar a base de conhecimento: {e}")

@app.post("/game-turn")
async def handle_game_turn(data: PlayerInput):
    """
    Endpoint para processar uma ação do jogador e retornar a narrativa do Mestre de RPG.
    """
    try:

        player_data = local_db_service.get_player_data(data.player_id)
        if not player_data:
            player_data = {
                "name": f"Aventureiro_{data.player_id[:4]}",
                "hp": 100,
                "inventory": ["Espada Curta", "Poção de Cura"],
                "location": "A entrada da Floresta dos Sussurros"
            }
            local_db_service.save_player_data(data.player_id, player_data)

        # 2. Busca informações relevantes na base de conhecimento (RAG)
        relevant_info = rag_service.search_relevant_text(data.message)

        # 3. Constrói o prompt completo para o modelo de IA
        prompt_parts = [
            "Você é um Mestre de RPG em um cenário de fantasia medieval. Sua tarefa é narrar a história, simular a aleatoriedade de dados e interagir com o jogador de forma imersiva. Sua resposta deve ser criativa e envolvente.",
            "Considere as seguintes informações do jogador:",
            f"- Nome: {player_data['name']}",
            f"- HP: {player_data['hp']}",
            f"- Localização: {player_data['location']}",
            f"- Inventário: {', '.join(player_data['inventory'])}",
            "Use as seguintes informações do mundo para enriquecer sua narrativa:",
            *[f" - {info['text']}" for info in relevant_info],
            "Aqui está o histórico da conversa:",
            *[f"{entry['role']}: {entry['content']}" for entry in data.history],
            f"Ação do jogador: {data.message}",
            "Sua resposta deve ser uma continuação da história, descrevendo as consequências da ação do jogador. Se a ação for um ataque, simule a jogada de um dado (ex: 'Você rolou um 18 e acertou o goblin!')."
        ]

        full_prompt = "\n\n".join(prompt_parts)

        # 4. Chama o modelo de IA
        ai_response = vertex_service.generate_narrative(full_prompt)

        # 5. Retorna a resposta ao jogador
        return {"response": ai_response}

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno. Por favor, tente novamente.")
