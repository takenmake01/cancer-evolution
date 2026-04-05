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

# write to fasta files
def write_to_fasta(taxa_registry):
    cd28_fasta_file_g = open("fastaFiles/sequenceList_cd28_g.fasta", "w")
    ctla4_fasta_file_g = open("fastaFiles/sequenceList_ctla4_g.fasta", "w")
    icos_fasta_file_g = open("fastaFiles/sequenceList_icos_g.fasta", "w")
    pd1_fasta_file_g = open("fastaFiles/sequenceList_pd1_g.fasta", "w")
    cd28_fasta_file_p = open("fastaFiles/sequenceList_cd28_p.fasta", "w")
    ctla4_fasta_file_p = open("fastaFiles/sequenceList_ctla4_p.fasta", "w")
    icos_fasta_file_p = open("fastaFiles/sequenceList_icos_p.fasta", "w")
    pd1_fasta_file_p = open("fastaFiles/sequenceList_pd1_p.fasta", "w")

    cd28_gene_list = []
    ctla4_gene_list = []
    icos_gene_list = []
    pd1_gene_list = []
    cd28_protein_list = []
    ctla4_protein_list = []
    icos_protein_list = []
    pd1_protein_list = []

    for taxa in taxa_registry.keys():
        genes, proteins = taxa_registry[taxa].get_records()

        cd28_gene_list.append(genes[0])
        ctla4_gene_list.append(genes[1])
        icos_gene_list.append(genes[2])
        pd1_gene_list.append(genes[3])
        cd28_protein_list.append(proteins[0])
        ctla4_protein_list.append(proteins[1])
        icos_protein_list.append(proteins[2])
        pd1_protein_list.append(proteins[3])

    SeqIO.write(cd28_gene_list, cd28_fasta_file_g, "fasta")
    SeqIO.write(ctla4_gene_list, ctla4_fasta_file_g, "fasta")
    SeqIO.write(icos_gene_list, icos_fasta_file_g, "fasta")
    SeqIO.write(pd1_gene_list, pd1_fasta_file_g, "fasta")
    SeqIO.write(cd28_protein_list, cd28_fasta_file_p, "fasta")
    SeqIO.write(ctla4_protein_list, ctla4_fasta_file_p, "fasta")
    SeqIO.write(icos_protein_list, icos_fasta_file_p, "fasta")
    SeqIO.write(pd1_protein_list, pd1_fasta_file_p, "fasta")

    cd28_fasta_file_g.close()
    ctla4_fasta_file_g.close()
    icos_fasta_file_g.close()
    pd1_fasta_file_g.close()
    cd28_fasta_file_p .close()
    ctla4_fasta_file_p.close()
    icos_fasta_file_p.close()
    pd1_fasta_file_p.close()



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

    # a function to return the SeqRecords contained in the class
    def get_records(self):
        record_g = [self.cd28["gene_seq"], self.ctla4["gene_seq"], self.icos["gene_seq"], self.pd1["gene_seq"]]
        record_p = [self.cd28["protein_seq"], self.ctla4["protein_seq"], self.icos["protein_seq"], self.pd1["protein_seq"]]

        return record_g, record_p

    def __repr__(self):
        # Count how many protein sequences have been successfully loaded
        genes = [self.cd28, self.ctla4, self.icos, self.pd1]
        loaded_count = sum(1 for g in genes if g['protein_seq'] is not None) #cound how many aren't None.
        
        # Return a formatted string with the scientific name and data status
        return (f"TaxaData(species='{self.name}', "
                f"common='{self.common_name}', "
                f"status='{loaded_count}/4 genes loaded')")
    


