import pickle

import numpy as np
from gefest.tools.utils.count_files import count_files
import os
from pathlib import Path
root_path = Path(__file__).parent.parent.parent.parent
def upload_file(path: str):
    with open(path, "rb") as f:
        file = pickle.load(f)
        f.close()
    return file


path_to_data = f'{root_path}/cases/sound_waves/sound_surr/Data_04_09/History/Data'
data_cnt = count_files(path =f'{path_to_data}', like ='spl_mask_')
data =[]
for i in range(data_cnt):
    data.append(upload_file(path_to_data+f'/spl_mask_{2}.pickle'))
print(data)
