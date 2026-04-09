'''
This program pulls the SeqRecord objects using the NCBI entrez API (WIP)

Stored in a 
Access the data via: taxa_registry['Common Name'].gene_symbol['type']
Example: taxa_registry['Human'].cd28['protein_seq'] returns a BioPython SeqRecord for the prtein sequence for cd28.
Keys for gene_symbol: .cd28, .ctla4, .icos, .pd1
Keys for type: 'gene_seq', 'protein_seq', 'gene_id', 'protein_id' (last two are the accession numbers)

The SeqRecod object that has the property .seq to access the full sequence. Full example to get the first 50 characters of hte protein sequence for cd28
taxa_registry['Human'].cd28['protein_seq'].seq[:50]

'''
from Bio import Entrez, SeqIO
from bio_models import TaxaData, load_data, save_data, write_to_fasta # Get the custom TaxaData Class and pickle methods
import time


#Entrez.api_key = # May be needed for faster requests, currently don't know how to get
'''
Initial declaration of TaxaData Objects
See bio_models.py for more info on how this is structured, but basically each object has a dictionary for each protein type
These dictionary items have the fields gene_id, protein_id, gene_seq and protein_seq.
The tuples are just used to instatiate this

Format: TaxaData(Scientific Name, Common Name, cd28_id, ctla4_id, icos_id, pd1_id)
gene_id = (gene id, protein id)
N/A = Accession number not found
'''
species_list = [
    TaxaData("Alligator mississippiensis", "American alligator", 
        ("XM_019491998.2", "XP_019347543.2"), ("XM_006267243.4", "XP_006267305.1"), 
        ("XM_019491999.2", "XP_019347544.1"), ("XM_019499038", "XP_019354583")),

    TaxaData("Ictalurus punctatus", "Channel catfish", 
        ("XM_017469194.3", "XP_017324683.1"), ("XM_017469194", "XP_017324683"), 
        ("N/A", "N/A"), ("N/A", "N/A")),

    TaxaData("Latimeria chalumnae", "Coelacanth", 
        ("N/A", "N/A"), ("N/A", "N/A"), 
        ("N/A", "N/A"), ("N/A", "N/A")),

    TaxaData("Callorhinchus milii", "Elephant shark", 
        ("NM_001292542.1", "NP_001279471.1"), ("XM_007890607", "XP_007888798"), 
        ("N/A", "N/A"), ("XM_007899691", "XP_007897882")),

    TaxaData("Anguilla anguilla", "European eel", 
        ("XM_035408948", "XP_035264839"), ("XM_035410183", "XP_035266074"), 
        ("N/A", "N/A"), ("N/A", "N/A")),

    TaxaData("Polypterus senegalus", "Gray bichir", 
        ("XM_039757853.1", "XP_039613787.1"), ("XM_039755029", "XP_039610963"), 
        ("XM_039757853", "XP_039613787"), ("N/A", "N/A")),

    TaxaData("Homo sapiens", "Human", 
        ("NM_006139.4", "NP_006130.1"), ("NM_005214.5", "NP_005205.2"),  
        ("NM_012092.4", "NP_036224.1"), ("NM_005018.3", "NP_005009.2")),

    TaxaData("Petromyzon marinus", "Sea Lamprey", 
        ("N/A", "N/A"), ("N/A", "N/A"), 
        ("N/A", "N/A"), ("XM_032977898.2", "XP_032833789.1")),

    TaxaData("Leucoraja erinacea", "Little skate", 
        ("XM_055638249", "XP_055494224"), ("XM_055638252.1", "XP_055494227"), 
        ("N/A", "N/A"), ("XM_055645557", "XP_055501532")),

    TaxaData("Oncorhynchus mykiss", "Rainbow trout", 
        ("NM_001124533.1", "NP_001118005.1"), ("XM_036975349.1", "XP_036831244"), 
        ("N/A", "N/A"), ("N/A", "N/A")),

    TaxaData("Scyliorhinus canicula", "Smaller-spotted catshark", 
        ("XM_038801863", "XP_038657791"), ("XM_038790366", "XP_038646294"), 
        ("N/A", "N/A"), ("N/A", "N/A")),

    TaxaData("Terrapene triunguis", "Box Turtle", 
        ("XM_026647348.1", "XP_026503133"), ("N/A", "N/A"), 
        ("XM_026647348.1", "XP_026503133"), ("XM_014578548.3", "XP_014434034")),

    TaxaData("Acipenser ruthenus", "Sterlet", 
        ("XM_034043461", "XP_033899352"), ("XM_034044623", "XP_033900514"), 
        ("XM_059033578.1", "XP_058889561"), ("XM_034027671.3", "XP_033883562")),

    TaxaData("Anser cygnoides", "Swan goose", 
        ("XM_013171675.3", "XP_013027129.1"), ("XM_013171678.3", "XP_013027132.2"), 
        ("XM_013171676.3", "XP_013027130.1"), ("XM_013194961.3", "XP_013050415.3"))
]

# Check if the species data is already downloaded. Returns None if nothing is saved
taxa_registry = load_data()

# Else pull sequences for proteins and genes using entrez
if (taxa_registry):
    print("Sequence data loaded from disk. Good stuff!")

else:
    api_email = input("Enter your email for the NCBI Entrez API (required): ")

    Entrez.email = api_email # Needed for Entrez API call
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

print(taxa_registry['Human'])
print(taxa_registry['Elephant shark'])

# write the registry to a set of FASTA files
write_to_fasta(taxa_registry)