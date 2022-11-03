# -*- coding: utf-8 -*-
"""BioPython: Search, Read, Fetch, & Write Sequences

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tuXQPquqU1Ew3PpRmIonIrF0OLa0Mh0V

Retrieving sequences from NCBI using the Entrez module in the BioPython package

Overview:

1. The Entrez Module

> Variables : email and api_key

> Functions: einfo(), read(), esearch(), efetch(),...

2. The SeqIO Module


> Functions: parse(), read(), write(), ...
"""

pip install biopython

"""Part 1: The Entrez Module"""

from Bio import Entrez
Entrez.email = "nsangani@iu.edu" 
#Entrez.api_key = " " 

# https://www.ncbi.nlm.nih.gov/

handle = Entrez.einfo()  # hold the information
record = Entrez.read(handle) 
handle.close()

handle = Entrez.einfo(db="nucleotide") 
record = Entrez.read(handle)
handle.close()

handle = Entrez.esearch(db="nucleotide", term="Human[Orgn] AND BRCA1[Gene]", 
                        usehistory="y", idtype="acc", 
                        retmax = "10") 
record = Entrez.read(handle)
handle.close()

idlist = record['IdList']
handle = Entrez.efetch(db="nucleotide", id=idlist, rettype="gb", retmode="text")
record = handle.read()
handle.close()

# https://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.T._valid_values_of__retmode_and/?report=objectonly

"""
Part 2: The SeqIO Module"""

from Bio import SeqIO 

handle = Entrez.efetch(db="nucleotide", id=idlist, rettype="gb", retmode="text")
record_iterator = SeqIO.parse(handle, "gb")
for record in record_iterator:
  print(record)
  
handle.close()

# Searching for only one record 

handle = Entrez.efetch(db="nucleotide", rettype="fasta", retmode="text", id="23747889")
record = SeqIO.read(handle, "fasta")
handle.close()

# To download records in batch and save them for later analysis

handle = Entrez.esearch(db="nucleotide", term="Human[Orgn] AND BRCA1[Gene]", 
                        usehistory="y", idtype="acc", 
                        retmax = "3")
record = Entrez.read(handle)
handle.close()

acc_list = record['IdList']
count = int(record["RetMax"])

webenv = record["WebEnv"] 
query_key = record["QueryKey"]

# Download records in batch

batch_size = 3
out_handle = open("BRCA1_Query1.faa", "w")
for start in range(0, count, batch_size):
    end = min(count, start + batch_size)
    print("Going to download record %i to %i" % (start + 1, end))
    handle = Entrez.efetch(db="nucleotide", rettype="fasta", retmode="text",
                           retstart=start, retmax=batch_size, webenv=webenv,
                           query_key=query_key, idtype="acc")
    record = handle.read()
    handle.close()
    out_handle.write(record)
out_handle.close()

# Later look up, how to write using SeqIO.write()

# List Comprehension - one line code to get all the ids

print([seq_record.id for seq_record in SeqIO.parse("BRCA1_Query1.faa", "fasta")])

fastaFile = "BRCA1_Query1.faa"
handle = open(fastaFile,"r")

for record in SeqIO.parse(handle,"fasta"):
    #print (record.id)
    #print(record.seq)
    #print(repr(record.seq)) # Learn the difference: repr() vs str()
    print(record)
    print('\n')
handle.close()

# Indexing

record_iterator = list(SeqIO.parse("BRCA1_Query1.faa", "fasta"))
print(record_iterator[1].seq) 
#print(record_iterator[-1].id)

# Accessing one record at a time 

record_iterator = SeqIO.parse("BRCA1_Query1.faa", "fasta")

first_record = next(record_iterator)
#print(first_record.id)
#print(first_record.description)

second_record = next(record_iterator)
#print(second_record.id)
#print(second_record.description)

# Filtering by sequence length

sequences = []  
for record in SeqIO.parse("BRCA1_Query1.faa", "fasta"):
    if len(record.seq) < 10000:
        sequences.append(record)

print("Found", len(sequences), "sequences less than 10kbp")

SeqIO.write(sequences, "short_seqs.fasta", "fasta") # SeqIO.write() !!

"""## Review

Recall: Entrez.einfo(), read(), esearch(), efetch()

Recall: record.id; record.seq; record.description; record.features


> Associated with SeqIO.parse() and .read()





Learn: SeqIO.convert() & SeqIO.write()
"""

# Fun Activity for Home

# Make this code work and generate fragments of sequences 

"""
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from random import randint

# There should be one and only one record, the entire genome:
mito_record = SeqIO.read("NC_006581.gbk", "genbank")

mito_frags = []
limit = len(mito_record.seq)
for i in range(0, 500):
    start = randint(0, limit - 200)
    end = start + 200
    mito_frag = mito_record.seq[start:end]
    record = SeqRecord(mito_frag, "fragment_%i" % (i + 1), "", "")
    mito_frags.append(record)

SeqIO.write(mito_frags, "mitofrags.fasta", "fasta")

"""

# Output:
"""
>fragment_1
TGGGCCTCATATTTATCCTATATACCATGTTCGTATGGTGGCGCGATGTTCTACGTGAAT
CCACGTTCGAAGGACATCATACCAAAGTCGTACAATTAGGACCTCGATATGGTTTTATTC
TGTTTATCGTATCGGAGGTTATGTTCTTTTTTGCTCTTTTTCGGGCTTCTTCTCATTCTT
CTTTGGCACCTACGGTAGAG
...
>fragment_500
ACCCAGTGCCGCTACCCACTTCTACTAAGGCTGAGCTTAATAGGAGCAAGAGACTTGGAG
GCAACAACCAGAATGAAATATTATTTAATCGTGGAAATGCCATGTCAGGCGCACCTATCA
GAATCGGAACAGACCAATTACCAGATCCACCTATCATCGCCGGCATAACCATAAAAAAGA
TCATTAAAAAAGCGTGAGCC
"""

# Hint: Use the entrez module to fetch data from NCBI

"""
handle = Entrez.efetch(db="nucleotide", rettype="fasta", retmode="text", id="23747889")
record = SeqIO.read(handle, "fasta")
handle.close()
"""

"""Next Topic: Alignment Tools (ClustalW, Muscle, & Emboss) and its generated files extrapolation

To Be Continued ...

The Entrez module Resource:
https://biopython.org/docs/1.75/api/Bio.Entrez.html

The SeQIO module Resource: https://biopython.org/wiki/SeqIO
# Additional Resources

1.   https://github.com/appbrewery/100-days-of-python
2.   http://biopython.org/DIST/docs/tutorial/Tutorial.html
3.   https://github.com/crazyhottommy/getting-started-with-genomics-tools-and-resources
"""