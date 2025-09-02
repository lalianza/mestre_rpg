import os
import sys
from dotenv import load_dotenv

load_dotenv()


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.services.dm_assistant import dm_assistant_chat


def run_local_chat():
    """
    Runs a local chat session to test the narrator's assistant.
    """
    print("--- Assistente do mestre ---")
    print("Digite sua questão ou 'sair' para finalizar o chat.")
    print("---------------------------------------")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'sair':
            print("Fechando a sessão, obrigado!")
            break

        try:
            response = dm_assistant_chat(user_input)
            print(f"Assistant: {response}")
        except Exception as e:
            print(f"um erro ocorreu para a questão: {e}")
            print("Por favor, tente novamente.")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Erro: Chave não configurada.")
    else:
        run_local_chat()
