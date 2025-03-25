import sys
from src.rag_system import RagSystem
from src.ontology_builder import OntologyBuilder

class FishChatbot:
    def __init__(self):
        # Initialize the RAG system and ontology builder
        self.rag_system = RagSystem()
        self.ontology_builder = OntologyBuilder()
        print("Hello! I'm your Fish Knowledge Bot. Ask me about any fish species or their details.")

    def get_response(self, user_query):
        """ Process user query and return response """
        response = self.rag_system.get_answer(user_query)  # Query the RAG system
        return response

    def start_chat(self):
        """ Start interactive chat loop """
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Goodbye! Have a great day!")
                break
            else:
                response = self.get_response(user_input)
                print(f"Bot: {response}")

# Initialize the chatbot
if __name__ == "__main__":
    chatbot = FishChatbot()
    chatbot.start_chat()
