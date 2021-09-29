import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
df=pd.read_excel("FQgene.xlsx")
b=sns.barplot(data=df,y="Gene",x="Number of mutations",palette="autumn")
b.tick_params(labelsize=7)
plt.title("Frequencies of 4206 mutations in OV-YUHS by gene level",fontsize=13)
plt.savefig("bar.pdf", bbox_inches ='tight')
plt.show()
