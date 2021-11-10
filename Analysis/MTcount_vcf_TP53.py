import glob, os
import pandas as pd
vctools=['freebayes','mutect2','vardict','varscan']
for vctool in vctools:
	vd=pd.read_excel(f"{vctool}_cntMT.xlsx")
	TP=pd.read_excel(f"OV-SMC_TP53list.xlsx")
	mg=pd.merge(left=TP, right=vd,how="left", on=["Chromosome","Position","REF","ALT"])
	mg.to_excel(f"{vctool}_TP53_cnt.xlsx",index=0)
	

