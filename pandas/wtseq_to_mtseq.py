import pandas as pd

#a=pd.read_excel("All-OV_MT100_ExtSeq.xlsx")
a=pd.read_excel("OV_MT100_ExtSeq.xlsx")
a.insert(0,"sequence_name","")
for i in range(len(a)):
    a.loc[i,"sequence_name"]=f"seqeunce_{i}"

a.insert(10,"MT Sequence AA 27","")
a.insert(6,"Mutation position","")
a.insert(13,"MT Sequence AA","")

for z in range(len(a)):
    pos="".join(k for k in a.loc[z,"Mutation"].split("fs")[0] if k.isdigit())
    if a.loc[z,"Mutation"][0] == a.loc[z,"Sequence AA"][int(pos)-1]:
        mut=a.loc[z,"Mutation"].split("fs")[0][-1]
        a.loc[z,"MT Sequence AA"] = a.loc[z,"Sequence AA"][:int(pos)-1]+mut+a.loc[z,"Sequence AA"][int(pos):]
    
        if int(pos)<14:
            aa=a.iloc[z]['MT Sequence AA'][:int(pos)+13]
        elif int(pos)+13 > a.iloc[z]["Sequence length"]:
            aa=a.iloc[z]['MT Sequence AA'][int(pos)-14:]
        else:
            aa=a.iloc[z]['MT Sequence AA'][int(pos)-14:int(pos)+13]
        a.loc[z,'MT Sequence AA 27']=aa
        a.loc[z,'MT Sequence AA 27']=a.loc[z,'MT Sequence AA 27'].split("*")[0]
a.to_excel("WTtoMT2.xlsx",index=0)
