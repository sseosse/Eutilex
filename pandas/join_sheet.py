import pandas as pd

mall=pd.read_excel('MF_all100.xlsx')
mov=pd.read_excel('MF_Ovary100.xlsx')


a=pd.merge(left=mall, right=mov, how="left", on=["DNA Change"])
b=a.iloc[:,[0,12,2,3,4,7,18]]
b.columns = ['All_MT','OV_MT','Variant type','Gene','Mutation','Rate_All','Rate_OV']


c=b.index[b['OV_MT']=='Substitution'].tolist()

for i in c:
    b['OV_MT'][i]=b['All_MT'][i]


a.to_csv('a.tsv',index=False,sep='\t')
b.to_csv('All-OV_MT100info.tsv',index=False,sep='\t')
