import pandas as pd

flurry_result=pd.read_excel("bbbbbb.xlsx")
hla_kr=pd.read_excel("HLAlist_KR_final.xlsx")
mut=pd.read_excel("All-OV_MT100_Mutseq.xlsx")

best_af=pd.DataFrame(columns = flurry_result.columns)
for i in range(len(mut)):
    sep_sample=flurry_result[flurry_result["sequence_name"]==f"sequence_{i}"]
    for j in hla_kr["Allele"]:
        sep_hla=sep_sample[sep_sample["best_allele"]=="HLA-"+j]
        sep_hla=sep_hla.drop_duplicates("best_allele",keep="first")
        best_af=best_af.append(sep_hla)
#best_af.to_excel("MT-HLA_KR_BestAF3.xlsx",index=0)

join=pd.merge(left=best_af, right=mut, how='left', on=["sequence_name","All_MT"])
prePanel=join.loc[:,["All_MT","Rate_All","best_allele","Gene","Mutation","Transcript ID","peptide","affinity","affinity_percentile",]]
#prepanel.to_excel("prePanel.xlsx",index=0)

y_axis=hla_kr["Allele"]
x_axis=mut["Gene"]+":"+mut["Mutation"]
finPanel=pd.DataFrame(index="HLA-"+y_axis, columns=x_axis)
dic={}
for k in range(len(prePanel)):
    l=prePanel.loc[k]
    dic[l["Gene"]+":"+l["Mutation"]+"|"+l["best_allele"]]=[l["peptide"],l["Rate_All"],l["affinity_percentile"]]

for m in finPanel.columns:
    for n in finPanel.index:
        if m+"|"+n in dic:
            finPanel.loc[n,m]=str(dic[m+"|"+n][2]) # 0 : peptide, 1 : Rate, 2 : AF
        else:
            finPanel.loc[n,m]="NaN"

def Filter():
    poplist=[]
    for cnt in finPanel.columns:
        cntnon=0
        for cnt2 in finPanel.index:
            cntnon+=finPanel.loc[cnt2,cnt].count("NaN")
            if cntnon > 10:
                if cnt not in poplist:
                    poplist.append(cnt)

    for pop in poplist:
        finPanel.pop(pop)

    for pop in poplist:
        for hla in finPanel.index:
            if pop+"|"+hla in dic:
                dic.pop(pop+"|"+hla)

    

def Sum():
    for hla in finPanel.index:
        summ=0
        for cmn in dic:
            if hla in cmn.split("|")[1]:
                summ+=float(dic[cmn][1])
    finPanel.loc[hla,"Rate_sum"]=summ
    
Filter()
#Sum()
finPanel.to_csv("Panel_AFP_210907.csv")

