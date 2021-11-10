import glob, os
import pandas as pd
vd=pd.read_excel(f"vc_commut.xlsx")
allmut=pd.DataFrame()
allfile=glob.glob(f"/home/eutilex/data/mRNA/SMC_vcf/SMC_mutations/allmut_*")
for a in range(len(vd)):
	for vc in allfile:
		vn=vc.split("/")[7].split("mut_")[1]
		vcfd=pd.read_excel(vc,header=None)
		vds=vcfd[(vcfd[1]==vd.loc[a,"Chromosome"]) & (vcfd[2]==vd.loc[a,"Position"]) & (vcfd[4]==vd.loc[a,"REF"]) & (vcfd[5]==vd.loc[a,"ALT"])]
		vd.loc[a,vn]=len(vds)
vd["Total"]=vd.iloc[:,11:].sum(axis=1)
vd.to_excel(f"vc_cntMT.xlsx",index=None)

