import pandas as pd
import numpy as np
from pathlib import Path

path_data = Path('../data/')

data_parameters = pd.read_csv('gw_filtered_events.csv')
folder = [p.name for p in path_data.iterdir() if p.is_dir()]

Nfolder = len(folder)
Nparame = len(data_parameters)

print(f'N folder = {len(folder)}')
print(f'N parame = {Nparame}')


for i in range(Nfolder):
    path = f'{path_data}/{folder[i]}'

    esta_vazio = not any(path.iterdir())