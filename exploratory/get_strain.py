import h5py
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gwosc.locate import get_event_urls
from pathlib import Path
import shutil
from tqdm import tqdm

df = pd.read_csv("gw_filtered_events.csv")
shortName = df['shortName']

print(f"Baixando {len(shortName)} sinais")

print("Currently downloading...")
N = len(shortName)
for i in tqdm(range(N)):

    name = shortName[i]
    folder = Path(f'../data/{name}')
    folder.mkdir(parents=True, exist_ok=True)

    urls = get_event_urls(name)
    for url in urls:
        name_file = url.split("/")[-1]
        detector = name_file.split("_")[0]
        sigla = detector.split("-")[-1]
        
    
        name_file_strain = f'strain_{sigla}.hdf5'
        response = requests.get(url)
        with open(name_file_strain, "wb") as f:
            f.write(response.content)
        shutil.move(f'strain_{sigla}.hdf5',f'../data/{name}/strain_{sigla}.hdf5')
        

