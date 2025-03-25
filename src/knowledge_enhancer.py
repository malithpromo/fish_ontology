import json
from pathlib import Path

class FishKnowledgeEnhancer:
    def __init__(self):
        """Initialize the knowledge enhancer."""
        self.data_dir = Path("data/ontology")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def add_fish_knowledge(self, fish_name):
        """
        Add detailed knowledge about a specific fish species.
        
        Args:
            fish_name (str): Name of the fish species
        
        Returns:
            dict: Structured knowledge about the fish
        """
        # Predefined knowledge for Atlantic Salmon
        if fish_name.lower() == "atlantic salmon":
            salmon_data = {
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
                    "Coastal rivers in North America and Europe"
                ],
                "diet": [
                    "Smaller fish",
                    "Crustaceans", 
                    "Aquatic insects",
                    "Squid"
                ],
                "conservation_status": "Vulnerable",
                "physical_characteristics": {
                    "average_length": "70-130 cm",
                    "average_weight": "3.6-7.3 kg",
                    "color": "Blue-green back, silver sides and belly"
                }
            }
            
            # Save to JSON file
            file_path = self.data_dir / f"{fish_name.lower().replace(' ', '_')}_knowledge.json"
            with open(file_path, 'w') as f:
                json.dump(salmon_data, f, indent=2)
            
            return salmon_data
        
        else:
            # For other fish species, you could add more complex knowledge gathering logic
            return {
                "error": f"No detailed information available for {fish_name}"
            }

    def get_fish_knowledge(self, fish_name):
        """
        Retrieve existing knowledge about a fish species.
        
        Args:
            fish_name (str): Name of the fish species
        
        Returns:
            dict: Structured knowledge about the fish
        """
        file_path = self.data_dir / f"{fish_name.lower().replace(' ', '_')}_knowledge.json"
        
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        
        return {"error": f"No knowledge found for {fish_name}"}