import os
import firebase_admin
from firebase_admin import credentials, firestore

try:
    if os.getenv("FIRESTORE_EMULATOR_HOST"):
        print("Conectando ao emulador do Firestore...")
        os.environ["FIRESTORE_EMULATOR_HOST"] = os.getenv("FIRESTORE_EMULATOR_HOST")
        cred = credentials.ApplicationDefault()
    else:
        print("Conectando ao Firestore em produção...")
        cred = credentials.ApplicationDefault()

    firebase_admin.initialize_app(cred)

except ValueError as e:
    if "The default Firebase app already exists" not in str(e):
        raise e

db = firestore.client()

class FirestoreService:
    """
    Serviço para interagir com o Cloud Firestore.
    """

    def get_player_data(self, player_id: str) -> dict | None:
        """
        Busca os dados de um jogador no Firestore.

        Args:
            player_id (str): O ID único do jogador.

        Returns:
            dict | None: Um dicionário com os dados do jogador, ou None se não for encontrado.
        """
        doc_ref = db.collection("players").document(player_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None

    def save_player_data(self, player_id: str, data: dict):
        """
        Salva ou atualiza os dados de um jogador no Firestore.

        Args:
            player_id (str): O ID único do jogador.
            data (dict): O dicionário de dados do jogador a ser salvo.
        """
        doc_ref = db.collection("players").document(player_id)
        doc_ref.set(data)
        print(f"Dados do jogador {player_id} salvos com sucesso.")
