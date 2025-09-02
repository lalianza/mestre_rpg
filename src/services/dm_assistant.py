import sys
import os
import openai
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from services.load_chat import ChatService


if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("The OPENAI_API_KEY not found.")

openai.api_key = os.environ.get("OPENAI_API_KEY")

def dm_assistant_chat(user_input: str) -> str:
    """
    Uses the chat service to generate the prompt and the OpenAI API for the response.
    """
    try:
        chat_service = ChatService()
        full_prompt = chat_service.load_chat(user_input)

        print("--- PROMPT SENT TO OPENAI ---")
        print(full_prompt)
        print("--- END OF PROMPT ---")


        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )


        ai_response = completion.choices[0].message.content

        return ai_response

    except Exception as e:
        print(f"An orchestration error occurred: {e}")
        return "Sorry, I couldn't process your request at the moment."

if __name__ == "__main__":
    print("Starting the chat with the Narrator's assistant. Type 'exit' to end.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        response = dm_assistant_chat(user_input)
        print(f"Assistant: {response}")
