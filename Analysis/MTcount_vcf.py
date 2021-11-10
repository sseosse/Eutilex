import glob, os
import pandas as pd
vctools=['freebayes','mutect2','vardict','varscan']
for vctool in vctools:
	vd=pd.read_excel(f"commut_{vctool}.xlsx")
	allmut=pd.DataFrame()
	allfile=glob.glob(f"/home/eutilex/data/mRNA/SMC_vcf/SMC_{vctool}/Filtered_noheader_{vctool}/SMC_*")
	for a in range(len(vd)):
		for vcf in allfile:
			sn=vcf.split("/")[8].split("-tumor-")[0]
			vcfd=pd.read_csv(vcf,sep='\t',header=None)
			vds=vcfd[(vcfd[0]==vd.loc[a,"Chromosome"]) & (vcfd[1]==vd.loc[a,"Position"]) & (vcfd[3]==vd.loc[a,"REF"]) & (vcfd[4]==vd.loc[a,"ALT"])]
			vd.loc[a,sn]=len(vds)
	vd["Total"]=vd.iloc[:,11:].sum(axis=1)
	vd.to_excel(f"{vctool}_cntMT.xlsx",index=None)

