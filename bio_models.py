from Bio import Entrez, SeqIO
import os
import pickle

'''
A surprise tool that will help us later (Pickle methods to save the data to disk)

Stored in the same folder as the program
'''
# Get the absolute path to the directory where this script is saved and join it with the filename
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PICKLE_PATH = os.path.join(BASE_DIR, "species_data.pkl")

# saves the data to the specified path (NOTE THAT THIS IS HARDCODED by name and current directory)
def save_data(data):
    with open(PICKLE_PATH, "wb") as f:
        pickle.dump(data, f)
        
    print(f"Data successfully pickled to: {PICKLE_PATH}. Good Stuff!")

# Loads the data from the specified path (NOTE THAT THIS IS HARDCODED by name and program directory)
def load_data():
    if os.path.exists(PICKLE_PATH):
        with open(PICKLE_PATH, "rb") as f:
            return pickle.load(f)
        
    return None



'''
TaxaData Class: Used to keep track of accession numbers and SeqRecord objects for the four genes in each species

To Intitialize:
- name (scientific)
- common name
- list of cd28 ids format: (gene accession ID, protein accession ID)
- list of ctla4 ids format: (gene accession ID, protein accession ID)
- list of icos ids format: (gene accession ID, protein accession ID)
- list of pd1 ids format: (gene accession ID, protein accession ID)
'''
class TaxaData:
    def __init__(self, name, common_name, cd28_ids, ctla4_ids, icos_ids, pd1_ids):
        self.name = name
        self.common_name = common_name
        
        # Structure: {id_type: access_num, seq_record: BioPythonObj}
        # Uses Tuples to declare each one (saves doing it manually)
        self.cd28 = {"gene_id": cd28_ids[0], "protein_id": cd28_ids[1], "gene_seq": None, "protein_seq": None}
        self.ctla4 = {"gene_id": ctla4_ids[0], "protein_id": ctla4_ids[1], "gene_seq": None, "protein_seq": None}
        self.icos = {"gene_id": icos_ids[0], "protein_id": icos_ids[1], "gene_seq": None, "protein_seq": None}
        self.pd1 = {"gene_id": pd1_ids[0], "protein_id": pd1_ids[1], "gene_seq": None, "protein_seq": None}

    def fetch_sequences(self):
        data = [self.cd28, self.ctla4, self.icos, self.pd1]
        for item in data:
            # Fetch Nucleotide Sequence from NCBI
            handle_g = Entrez.efetch(db="nucleotide", id=item["gene_id"], rettype="fasta", retmode="text")
            item["gene_seq"] = SeqIO.read(handle_g, "fasta") #Convert to SeqRecord and add to gene dict in self
            handle_g.close()

            # Fetch Protein Sequence from NCBI
            handle_p = Entrez.efetch(db="protein", id=item["protein_id"], rettype="fasta", retmode="text")
            item["protein_seq"] = SeqIO.read(handle_p, "fasta") #Convert to SeqRecord and add to protein dict in self
            handle_p.close()

    def __repr__(self):
        # Count how many protein sequences have been successfully loaded
        genes = [self.cd28, self.ctla4, self.icos, self.pd1]
        loaded_count = sum(1 for g in genes if g['protein_seq'] is not None) #cound how many aren't None.
        
        # Return a formatted string with the scientific name and data status
        return (f"TaxaData(species='{self.name}', "
                f"common='{self.common_name}', "
                f"status='{loaded_count}/4 genes loaded')")
    


