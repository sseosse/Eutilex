#!/bin/python

import os
# 1.Running WES, WTS, HLA typing at the same time.
# 2.Running pVACseq when step 1 is finished. 
os.system("(python WES/WES_v1.4.py & python WTS/WTS_v1.4.py & python WTS/HLAtyping_v1.1.py) && (conda run -n Neoang python pVACseq/pVACseq_v1.7_lenient.py & conda run -n Neoang python pVACseq/pVACseq_v1.7_strict.py)")
