import pandas as pd
import os, fileinput, sys

a=pd.read_excel("Candidateprimer_220118.xlsx",sheet_name="Gene information")

for i in range(len(a)):
	sn=a.loc[i,"Gene Symbol"]
	os.system(f"cp example config_{sn}")
	for l in fileinput.input(f'config_{sn}',inplace = True):
		if "SEQUENCE_ID=" in l:
			l=f"SEQUENCE_ID={sn}\n"	
		if "SEQUENCE_TEMPLATE=" in l:
			l=f"SEQUENCE_TEMPLATE={a.loc[i,'Specific Sequence(SS)']}\n"
		sys.stdout.write(l)
	os.system(f"/home/Programs/primer3/src/primer3_core config_{sn} > result_{sn}")
