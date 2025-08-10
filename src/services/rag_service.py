import os
import json
from typing import List, Dict
from chromadb import HttpClient
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

class LocalRAGService:
    """
    Serviço para o sistema de Recuperação-Aumentada de Geração (RAG),
    otimizado para ambiente de desenvolvimento local e sem custos.
    """

    def __init__(self):
        rag_host = os.getenv("RAG_DATABASE_HOST", "http://localhost:8001")
        self.chroma_client = HttpClient(host=rag_host, port=8000)
        

        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name='paraphrase-multilingual-MiniLM-L12-v2'
        )


        self.collection = self.chroma_client.get_or_create_collection(
            name="rpg_adventures",
            embedding_function=self.embedding_function
        )

    def load_knowledge_base(self, data_file_path: str = "data/adventures.jsonl"):
        """
        Carrega dados do arquivo JSONL, gera embeddings e salva no ChromaDB.
        Isso deve ser executado apenas uma vez.
        """

        if self.collection.count() > 0:
            print("A base de conhecimento já está populada. Ignorando a carga.")
            return

        documents = []
        metadatas = []
        ids = []

        with open(data_file_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                entry = json.loads(line)
                documents.append(entry.get("text"))
                metadatas.append({"source": entry.get("source")})
                ids.append(str(i))
        

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Base de conhecimento populada com {len(documents)} documentos.")

    def search_relevant_text(self, query: str, n_results: int = 3) -> List[Dict]:
        """
        Busca os trechos mais relevantes na base de conhecimento com base na query do jogador.

        Args:
            query (str): A entrada do jogador.
            n_results (int): O número de resultados a serem retornados.

        Returns:
            List[Dict]: Uma lista de dicionários com os documentos e metadados relevantes.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        

        formatted_results = []
        if results.get("documents"):
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                formatted_results.append({"text": doc, "source": meta.get("source")})
        
        return formatted_results