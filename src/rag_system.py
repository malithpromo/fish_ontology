import os
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RagSystem:
    def __init__(self):
        """Initialize the RAG system."""
        # Initialize sentence transformer model for embeddings
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        
        # Predefined knowledge about Atlantic Salmon
        self.atlantic_salmon_data = {
            "taxonomy": {
                "kingdom": "Animalia",
                "phylum": "Chordata",
                "class": "Actinopterygii",
                "order": "Salmoniformes",
                "family": "Salmonidae",
                "genus": "Salmo",
                "species": "Salmo salar"
            },
            "habitat": [
                "North Atlantic Ocean",
                "Rivers and streams in North America and Europe"
            ],
            "diet": [
                "Smaller fish",
                "Crustaceans",
                "Insects",
                "Squid"
            ],
            "conservation_status": "Vulnerable"
        }
        
        # Initialize vector store
        self.vectorstore = self.load_vectorstore()
    
    def load_vectorstore(self):
        """
        Load or create a vector store for fish knowledge.
        
        Returns:
            faiss.IndexFlatL2: A FAISS vector index
        """
        # Ensure data directory exists
        vector_store_dir = Path("data/processed")
        vector_store_dir.mkdir(parents=True, exist_ok=True)
        
        vector_store_path = vector_store_dir / "fish_vectorstore.faiss"
        
        if vector_store_path.exists():
            # Load existing vector store
            return faiss.read_index(str(vector_store_path))
        else:
            # Create an empty vector store
            dimension = self.model.get_sentence_embedding_dimension()
            return faiss.IndexFlatL2(dimension)
    
    def query(self, user_query):
        """
        Process user query and return relevant information
        
        Args:
            user_query (str): User's input query about fish
        
        Returns:
            str: Relevant information about the query
        """
        # Convert query to lowercase for consistent matching
        user_query = user_query.lower()
        
        # Check for taxonomy-related queries
        if any(tax_term in user_query for tax_term in ["taxonomy", "classification", "species", "scientific name"]):
            taxonomy_response = "Atlantic Salmon (Salmo salar) Taxonomy:\n"
            for rank, name in self.atlantic_salmon_data['taxonomy'].items():
                taxonomy_response += f"- {rank.capitalize()}: {name}\n"
            return taxonomy_response
        
        # Check for habitat-related queries
        if any(hab_term in user_query for hab_term in ["habitat", "live", "environment"]):
            habitat_response = "Atlantic Salmon Habitats:\n"
            for habitat in self.atlantic_salmon_data['habitat']:
                habitat_response += f"- {habitat}\n"
            return habitat_response
        
        # Check for diet-related queries
        if any(diet_term in user_query for diet_term in ["diet", "eat", "food"]):
            diet_response = "Atlantic Salmon Diet:\n"
            for food in self.atlantic_salmon_data['diet']:
                diet_response += f"- {food}\n"
            return diet_response
        
        # Check for conservation status queries
        if any(cons_term in user_query for cons_term in ["conservation", "status", "endangered"]):
            return f"Conservation Status: {self.atlantic_salmon_data['conservation_status']}"
        
        # Default response if no specific information is found
        return "I apologize, but I couldn't find specific information matching your query about Atlantic Salmon."