# ontology_builder.py
from owlready2 import *

# Create new ontology
onto = get_ontology("http://fish-ontology.org/onto.owl")

with onto:
    # Define main classes
    class Fish(Thing):
        pass
    
    # Properties for fish
    class has_habitat(Fish >> str):
        pass
    
    class has_diet(Fish >> str):
        pass
    
    class has_average_size(Fish >> float):
        pass
    
    class has_lifespan(Fish >> float):
        pass
    
    class is_related_to(Fish >> Fish):
        pass
    
    # Add 7 example fish species (you'll replace these with your specific ones)
    class Salmon(Fish):
        pass
    
    class Tuna(Fish):
        pass
    
    class Bass(Fish):
        pass
    
    # Create individuals
    atlantic_salmon = Salmon("AtlanticSalmon")
    atlantic_salmon.has_habitat = ["Ocean", "River"]
    atlantic_salmon.has_diet = ["Small fish", "Insects"]
    atlantic_salmon.has_average_size = 76.0  # in cm
    atlantic_salmon.has_lifespan = 7.0  # in years
    
    bluefin_tuna = Tuna("BluefinTuna")
    bluefin_tuna.has_habitat = ["Ocean"]
    bluefin_tuna.has_diet = ["Small fish", "Squid"]
    bluefin_tuna.has_average_size = 200.0  # in cm
    bluefin_tuna.has_lifespan = 15.0  # in years

# Save ontology
onto.save(file="fish_ontology.owl", format="rdfxml")