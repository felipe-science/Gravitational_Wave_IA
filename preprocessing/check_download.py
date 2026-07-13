import pandas as pd
import numpy as np
from pathlib import Path

path_data = Path('../data/')

data_parameters = pd.read_csv('gw_filtered_events.csv')
folders = [p.name for p in path_data.iterdir() if p.is_dir()]

Nfolder = len(folders)
Nparame = len(data_parameters)


empty = 0
list_shortName_empty = []
for i in range(Nfolder):
    # 1. Cria a string do caminho
    path_str = f'{path_data}/{folders[i]}'
    
    # 2. Transforma essa string em um objeto Path do pathlib
    path_objeto = Path(path_str)

    tem_hdf5 = next(path_objeto.glob('*.hdf5'), None) is not None
    is_empty = not tem_hdf5

    if is_empty:
        empty+=1
        list_shortName_empty.append(folders[i])


print(f'N parame = {Nparame}\n')
print(f'N folder = {len(folders)}')
print(f'Empty folder = {empty}')
print(f'Full folder = {Nfolder-empty}\n')

print(list_shortName_empty)
