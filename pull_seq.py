'''
This program pulls the SeqRecord objects using the NCBI entrez API (WIP)

Access data via: taxa_registry['Common Name'].gene_symbol['type']
Example: taxa_registry['Human'].cd28['protein_seq'] returns a BioPython SeqRecord for the prtein sequence for cd28.
Keys for gene_symbol: .cd28, .ctla4, .icos, .pd1
Keys for type: 'gene_seq', 'protein_seq', 'gene_id', 'protein_id' (last two are the accession numbers)

The SeqRecod object that has the property .seq to access the full sequence. Full example to get the first 50 characters of hte protein sequence for cd28
taxa_registry['Human'].cd28['protein_seq'].seq[:50]

'''
from Bio import Entrez, SeqIO
from bio_models import TaxaData, load_data, save_data # Get the custom TaxaData Class and pickle methods
import time


Entrez.email = "evan.boonstra@mytwu.ca" # Needed for Entrez API call
#Entrez.api_key = # May be needed for faster requests, currently don't know how to get

# Initial declaration of TaxaData Objects
# See bio_models.py for more info on how this is structured, but basically each object has a dictionary for each protein type
# These dictionary items have the fields gene_id, protein_id, gene_seq and protein_seq.
# The tuples are just used to instatiate this

species_list = [
    TaxaData("Homo sapiens", "Human", 
        ("NM_006139.4", "NP_006130.1"), ("NM_005214.5", "NP_005205.2"),  
        ("NM_012092.4", "NP_036224.1"), ("NM_005018.3", "NP_005009.2")),

    TaxaData("Oncorhynchus mykiss", "Rainbow trout", 
        ("NM_001124434.1", "NP_001117906.1"), ("XM_032415309", "XP_032271200"), 
        ("XM_021612440", "XP_021468115"), ("XM_032415160", "XP_032271051")),

    TaxaData("Ictalurus punctatus", "Channel catfish", 
        ("XM_017482835", "XP_017338324"), ("XM_017482833", "XP_017338322"), 
        ("XM_017482834", "XP_017338323"), ("XM_017478086", "XP_017333575")),

    TaxaData("Alligator mississippiensis", "American alligator", 
        ("XM_019481308", "XP_019336853"), ("XM_019481313", "XP_019336858"), 
        ("XM_019481314", "XP_019336859"), ("XM_019478440", "XP_019333985")),

    TaxaData("Anser cygnoides", "Swan goose", 
        ("XM_048037628", "XP_047893583"), ("XM_048043063", "XP_047899018"), 
        ("XM_013180425", "XP_013035879"), ("XM_048040904", "XP_047896859")),

    TaxaData("Callorhinchus milii", "Elephant shark", 
        ("XM_007897274", "XP_007895465"), ("XM_007908332", "XP_007906523"), 
        ("XM_007908331", "XP_007906522"), ("XM_007905105", "XP_007903296")),

    TaxaData("Scyliorhinus canicula", "Small-spotted catshark", 
        ("XM_038786278", "XP_038642206"), ("XM_038786280", "XP_038642208"), 
        ("XM_038786281", "XP_038642209"), ("XM_038783416", "XP_038639344")),

    TaxaData("Leucoraja erinacea", "Little skate", 
        ("XM_061595159", "XP_061451042"), ("XM_061595160", "XP_061451043"), 
        ("XM_061595162", "XP_061451045"), ("XM_061580172", "XP_061436055"))
]

# Check if the species data is already downloaded. Returns None if nothing is saved
taxa_registry = load_data()

# Else pull sequences for proteins and genes using entrez
if (taxa_registry):
    print("Sequence data loaded from disk. Good stuff!")

else:
    taxa_registry = {} # Stores references to the TaxaData items in the list, but makes it searchable by common name
    for species in species_list:
        try:
            
            species.fetch_sequences()
            print(f"Successfully pulled data for: {species.common_name} ({species.name})")
            
            # Add to the searchable dictionary
            taxa_registry[species.common_name] = species

            time.sleep(0.4) # avoids being rate-limited by the entrez api since there is no api key (I think it is free so could sign up if this is an issue)
            
        except Exception as e:
            print(f"Failed to pull {species.common_name}: {e}")
        
    # Dump data for next time
    save_data(taxa_registry)

# Print the keys and a few test cases
print(taxa_registry.keys())
print(taxa_registry['Human'].cd28['protein_seq'].seq[:50])
print(taxa_registry['Human'].cd28['gene_seq'].seq[:50])

