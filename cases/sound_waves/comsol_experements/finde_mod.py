import os
import pickledb
import numpy as np
import mph
import pickle
import argparse

db = pickledb.load('real-world/microfluidic/comsol_db.saved', False)
last=int(len(os.listdir('real-world/microfluidic/HistoryFiles'))/2)-1
print(last)
with open(f'real-world/microfluidic/HistoryFiles/population_{last}.pickle', 'rb') as f:
    pop = pickle.load(f)
indexis=[]
for i in range(last):
    with open(f'real-world/microfluidic/HistoryFiles/performance_{i}.pickle', 'rb') as f:
        perf = pickle.load(f)
        print(perf)
for i in range(3):
    print(db.get(str(pop[i])))
