# chatbot_web.py
import streamlit as st
from src.rag_system import RagSystem

# Initialize RAG system once
rag_system = RagSystem()

def get_response(query):
    """Get response from the RAG system based on the user query."""
    return rag_system.query(query)

# Streamlit user interface
st.title("Fish Knowledge Chatbot")
st.write("Ask me anything about fish!")

user_query = st.text_input("Your question:")

if user_query:
    st.subheader("Your question:")
    st.write(user_query)
    
    st.subheader("Answer:")
    response = get_response(user_query)
    
    # Check if response is empty or "No information found"
    if "No information" in response:
        st.warning(response)
    else:
        # Use markdown to better format the response
        st.markdown(response.replace("\n", "  \n"))  # Ensure line breaks render correctly in markdown