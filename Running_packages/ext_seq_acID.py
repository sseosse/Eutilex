from Bio import Entrez
import pandas as pd

acs=pd.read_excel("accessionID.xlsx",sheet_name="B2M")
#acs_cm=pd.read_excel("TRAC_acID_cm.xlsx")

Entrez.email = "shheo430@gmail.com"
l=[]
for i in acs["accession id"]:
#for i in acs_cm["accession id"]:
	handle = Entrez.efetch(db="nucleotide", id=i, rettype="fasta")
	print(handle.read())
	
