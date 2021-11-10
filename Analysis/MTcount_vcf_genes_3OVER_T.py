import glob, os, sys
import pandas as pd
vd=pd.read_excel(f"OV-SMC_MTgene_3VC.xlsx")
allmut=pd.DataFrame()
vctool = sys.argv[1]
allfile=glob.glob(f"/home/eutilex/data/mRNA/SMC_vcf/SMC-T_{vctool}/Filtered_noheader_{vctool}/SMC_*")
for a in range(len(vd)):
	for vcf in allfile:
		sn=vcf.split("/")[8].split("-tumor-")[0]
		vcfd=pd.read_csv(vcf,sep='\t',header=None)
		vds=vcfd[(vcfd[0]==vd.loc[a,"Chromosome"]) & (vcfd[1]==vd.loc[a,"Position"]) & (vcfd[3]==vd.loc[a,"REF"]) & (vcfd[4]==vd.loc[a,"ALT"])]
		vd.loc[a,sn]=len(vds)
		print(vds)
vd["Total"]=vd.iloc[:,11:].sum(axis=1)
vd.to_excel(f"OV-SMC_{vctool}_genes_3OVER_T.xlsx",index=None)

