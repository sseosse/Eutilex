import glob
import pandas as pd
genelist=pd.read_excel("OV-YUHS_geneexplist.xlsx")
for i in glob.glob("*genes.*"):
	sn=i.split(".genes.")[0]
	a=pd.read_csv(i,sep='\t')
	b=pd.merge(left=genelist,right=a,how='left',on='gene_id')
	b=b.loc[:,['FPKM']]
	b.rename(columns={'FPKM':f'{sn}:FPKM'},inplace=True)
	genelist[f'{sn}:FPKM']=b
genelist.rename(columns={'gene_id':'Gene symbol'},inplace=True)
genelist.to_excel("OV-YUHS_expression.xlsx",index=0)
