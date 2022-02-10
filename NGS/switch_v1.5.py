#!/bin/python
import os

os.system("(python WES/WES_v1.5.py & \
python WTS/WTS_v1.5.py & \
python WTS/HLAtyping_v1.2.py) && \
(conda run -n Neoang python pVACseq/pVACseq_v1.8.py)")
