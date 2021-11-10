import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


tt=pd.read_excel("OV-YUHS_expression_tsp.xlsx")
sns.boxplot(data=tt)
plt.title("Gene expression on OV-YUHS tumor samples")
plt.xlabel("Gene")
plt.ylabel("FPKM") 
plt.yticks([0,20,40,60,80])
plt.axhline(8.9,color='r',label='FPKM Average')
plt.legend()
plt.savefig("OV-YUHS_exp_boxplot.pdf", bbox_inches ='tight')
plt.show()

