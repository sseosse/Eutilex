import pandas as pd

EC=pd.read_excel("join.xlsx",sheet_name="EC")
AA2=pd.read_excel("join.xlsx",sheet_name="AA2")
MC=pd.read_excel("join.xlsx",sheet_name="MC")
SAI=pd.read_excel("join.xlsx",sheet_name="SAI")
HSCA=pd.read_excel("join.xlsx",sheet_name="HSCA")
CH=pd.read_excel("join.xlsx",sheet_name="CH")

mg=pd.merge(left=EC, right=AA2, how="left", on=["Allele"])
mg2=pd.merge(left=mg, right=MC, how="left", on=["Allele"])
mg3=pd.merge(left=mg2, right=SAI, how="left", on=["Allele"])
mg4=pd.merge(left=mg3, right=HSCA, how="left", on=["Allele"])
mg5=pd.merge(left=mg4, right=CH, how="left", on=["Allele"])
fn=mg5.iloc[:,[0,1,3,5,7,9,11]]
fn.columns =['HLA type','ECfq','AA2fq','MCfq','SAIfq','HSCAfq','CHfq']
f2=fn.fillna(0)
f2.to_excel("graph.xlsx",index=0)
