import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

mpl.use('TkAgg')
data=pd.read_csv("Panel_AFPmin211111.csv",index_col=0)
sns.set(font_scale=0.6)
plt.figure(figsize=(20,6))
np.ma.array(data,mask=np.isnan(data))
cmap=mpl.cm.get_cmap("bwr_r").copy()
#cmap=matplotlib.cm.bwr_r
cmap.set_bad('black')
sns.heatmap(data, cmap=cmap)#bwr seismic
#hm =sb.heatmap(data, cmap=bwr_r)#bwr seismic
plt.xlabel("Gene:Mutation", fontsize=13)
plt.ylabel("HLA type", fontsize=13)
plt.title("Affinity Percentiles of Neoantigen Peptides",fontsize=15)
plt.savefig("Panel_Heatmap2.pdf", bbox_inches ='tight')
plt.show()
