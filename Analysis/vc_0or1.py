import pandas as pd

df=pd.read_excel("vc_cntMT.xlsx")
col=["vardict.xlsx","freebayes.xlsx","varscan.xlsx","mutect2.xlsx"]
for line in range(len(df)):
	for ec in col:
		if int(df.loc[line,ec])== 0:
			df.loc[line,f"{ec}_TF"]=0
		else:
			df.loc[line,f"{ec}_TF"]=1

df["Total_TF"]=df.iloc[:,16:].sum(axis=1)
df=df.sort_values(by='Total_TF',ascending=False)
df.to_excel("OV-SMC_TopMT_VCFQ_vcf.xlsx",index=False)
		



