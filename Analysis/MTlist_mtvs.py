import os, glob, sys
import pandas as pd

vctool=sys.argv[1]
allmut=pd.DataFrame()
allfile=glob.glob(f"/home/eutilex/data/mRNA/SMC_vcf/SMC_{vctool}/Filtered_noheader_{vctool}/SMC_*")
for vcf in allfile:
	sn=vcf.split("/")[8].split("-tumor-")[0]
	df = pd.read_csv(vcf, sep='\t',header=None)
	df.insert(0,"sn",sn,True)
	allmut=allmut.append(df)
allmut.columns=['Sample ID','Chromosome', 'Position', 'ID','REF','ALT','QUAL','FILTER','INFO','FORMAT','normal','tumor']
allmut.to_excel(f"allmut_{vctool}.xlsx", index=False)
#commonmutinfb=allmut[~allmut.duplicated(subset=['Chromosome', 'Position', 'ID','REF','ALT'])]
comnmutinfb=allmut.drop_duplicates(subset=['Chromosome', 'Position', 'ID','REF','ALT'])
comnmutinfb=comnmutinfb.sort_values(by='Position')
comnmutinfb=comnmutinfb.drop(['Sample ID'],axis=1)
comnmutinfb.to_excel(f"commut_{vctool}.xlsx", index=False)



