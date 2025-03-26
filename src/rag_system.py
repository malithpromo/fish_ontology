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
        
        # Predefined knowledge about Bulath Hapaya
        self.bulath_hapaya_data = {
            "taxonomy": {
                "order": "Cypriniformes",
                "family": "Cyprinidae",
                "subfamily": "Smiliogastrinae",
                "genus": "Pethia",
                "species": "Pethia nigrofasciata"
            },
            "common_names": ["Sri Lanka Black Ruby Barb", "Black Ruby Barb"],
            "appearance": "Dorsally olive green, becoming lighter with a reddish-orange tint. Three black vertical bands. Males exhibit bright red coloration.",
            "habitat": "Clear, cool, shady streams in forested areas. Found in pools of quiet water in clear streams and rivers.",
            "diet": "Feeds mainly on filamentous algae and detritus.",
            "conservation_status": "Vulnerable (VU), assessed on 07 August 2019.",
            "distribution": "Sri Lanka - Lowland wet zone from Kelani to Nilwala basins. Population in Ginigathena (Mahaweli River Basin) is translocated.",
            "aquarium_trade": "Highly commercial. Popular aquarium fish. Among top five exported endemic species in Sri Lanka."
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
        user_query = user_query.lower()
        
        if any(term in user_query for term in ["taxonomy", "classification", "species", "scientific name"]):
            response = "Bulath Hapaya (Pethia nigrofasciata) Taxonomy:\n"
            for rank, name in self.bulath_hapaya_data['taxonomy'].items():
                response += f"- {rank.capitalize()}: {name}\n"
            return response
        
        if any(term in user_query for term in ["habitat", "live", "environment"]):
            return f"Bulath Hapaya Habitat:\n- {self.bulath_hapaya_data['habitat']}"
        
        if any(term in user_query for term in ["diet", "eat", "food"]):
            return f"Bulath Hapaya Diet:\n- {self.bulath_hapaya_data['diet']}"
        
        if any(term in user_query for term in ["conservation", "status", "endangered"]):
            return f"Conservation Status: {self.bulath_hapaya_data['conservation_status']}"
        
        if any(term in user_query for term in ["distribution", "location", "found"]):
            return f"Bulath Hapaya Distribution:\n- {self.bulath_hapaya_data['distribution']}"
        
        if any(term in user_query for term in ["aquarium", "trade", "commercial"]):
            return f"Bulath Hapaya in Aquarium Trade:\n- {self.bulath_hapaya_data['aquarium_trade']}"
        
        return "I couldn't find specific information matching your query about Bulath Hapaya."
