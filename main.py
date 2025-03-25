import os
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st

# Import necessary modules
from src.knowledge_enhancer import FishKnowledgeEnhancer
from src.rag_system import RagSystem
from src.llm_integrator import DeepSeekLLM

def initialize_project_structure():
    """Create necessary project directories."""
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    Path("data/ontology").mkdir(parents=True, exist_ok=True)

def validate_api_key():
    """Validate DeepSeek API key."""
    load_dotenv()
    if not os.environ.get("DEEPSEEK_API_KEY"):
        st.error("DeepSeek API key not found in environment variables")
        st.info("Please add your DeepSeek API key to the .env file")
        st.stop()

def prepare_fish_knowledge():
    """Prepare initial fish knowledge base."""
    # Initialize knowledge enhancer
    enhancer = FishKnowledgeEnhancer()
    
    # Add detailed knowledge about Atlantic Salmon
    st.write("### Adding detailed knowledge about Atlantic Salmon...")
    salmon_data = enhancer.add_fish_knowledge("Atlantic Salmon")
    
    # Display extracted structured data
    st.write("\n#### Structured data extracted:")
    st.write(f"**Taxonomy:** {salmon_data['taxonomy']}")
    st.write(f"**Habitats:** {salmon_data['habitat']}")
    st.write(f"**Diet:** {salmon_data['diet']}")
    st.write(f"**Conservation status:** {salmon_data['conservation_status']}")
    
    return salmon_data

def create_streamlit_chatbot():
    """Create a Streamlit-based chatbot interface."""
    st.title("🐟 Fish Knowledge Chatbot 🌊")
    
    # Initialize RAG system
    rag_system = RagSystem()
    
    # Streamlit chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm a fish knowledge expert. Ask me anything about fish!"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    if prompt := st.chat_input("What would you like to know about fish?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Searching fish knowledge base..."):
                # Query the RAG system with LLM enhancement
                response = rag_system.query(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def run_test_queries(rag_system):
    """Run test queries to demonstrate LLM chatbot capabilities."""
    st.write("### Test Queries Demonstration")
    
    # Test queries
    test_queries = [
        "What does the Atlantic Salmon eat?",
        "What is the conservation status of Atlantic Salmon?",
        "How does Atlantic Salmon reproduce?",
        "Tell me about the habitat of Atlantic Salmon",
        "What are the physical characteristics of Atlantic Salmon?"
    ]
    
    for query in test_queries:
        st.write(f"\n#### Query: {query}")
        response = rag_system.query(query)
        st.write(f"**Result:** {response}")

def main():
    # Validate environment setup
    validate_api_key()
    
    # Initialize project structure
    initialize_project_structure()
    
    # Option to choose between chatbot and test queries
    mode = st.sidebar.selectbox(
        "Choose Mode", 
        ["Interactive Chatbot", "Test Queries Demonstration"]
    )
    
    # Prepare initial fish knowledge
    prepare_fish_knowledge()
    
    # Initialize RAG system
    rag_system = RagSystem()
    
    # Run selected mode
    if mode == "Interactive Chatbot":
        create_streamlit_chatbot()
    else:
        run_test_queries(rag_system)

if __name__ == "__main__":
    main()