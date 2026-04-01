'''

Sequence information will be stored in dict with entries of the form {(Taxa, AccessionNumber) : SeqRecord object}

This program pulls the SeqRecord object using the NCBI entrez API (WIP)


'''
from Bio import Entrez, SeqIO


Entrez.email = "evan.boonstra@mytwu.ca" # Needed for Entrez API call
#Entrez.api_key = # May be needed for faster requests, currently don't know how to get

# Accession Numbers:
taxa_DNA = [("Homo Sapiens", "NMs12344"), ()]
taxa_Protein = [("Homo Sapiens", "123"), ()]

# Dictionaries for adding the SeqRecord objects
dna_dict = dict.fromkeys(taxa_DNA, None)

protein_dict = dict.fromkeys(taxa_Protein, None)


# Query GenBank for the acession numbers. (MAY NEED TO ADD A WAIT IN BETWEEN REQUESTS)
# These two loops iterate through the dictionaries above and parses the result into SeqRecord objects
# These are put in a list (for now - will determine better solution)

# Pull sequences for genes
for species in accNum_DNA:
    print(f"Getting Sequence for {species}: {accNum_DNA[species]}")

    with Entrez.efetch(db="nucleotide", id=accNum_DNA[species], rettype="fasta", retmode="text") as handle:
        DNASeqs[species] = SeqIO.read(handle, "fasta") # parse the fasta data, convert to SeqRecord

    print(f"Successfully pulled Sequence for {species}")


# Pull sequences for prspeciesoteins
for species in accNum_Protein:
    print(f"Getting Sequence for {species}: {accNum_Protein[species]}")

    with Entrez.efetch(db="nucleotide", id=accNum_Protein[species], rettype="fasta", retmode="text") as handle:
        ProteinSeqs[species] = SeqIO.read(handle, "fasta") # parse the fasta data, convert to SeqRecord

    print(f"Successfully pulled Sequence for {species}")


print(ProteinSeqs)
print(DNASeqs)