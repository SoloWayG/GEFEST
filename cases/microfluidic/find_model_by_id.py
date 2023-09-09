import os
import pickledb
import numpy as np
import mph
import pickle
import argparse
from pathlib import Path
root_path = Path(__file__).parent.parent.parent
db = pickledb.load(f'{root_path}/cases/microfluidic/comsol_db.saved', False)
last=int(len(os.listdir(f'{root_path}/cases/microfluidic/HistoryFiles'))/2)-1
print(last)
with open(f'{root_path}/cases/microfluidic/HistoryFiles/population_{last}.pickle', 'rb') as f:
    pop = pickle.load(f)
indexis=[]
for i in range(last):
    with open(f'{root_path}/cases/microfluidic/HistoryFiles/performance_{i}.pickle', 'rb') as f:
        perf = pickle.load(f)
        print(perf)
for i in range(3):
    print(f'{i+1} model',db.get(str(pop[i])))
