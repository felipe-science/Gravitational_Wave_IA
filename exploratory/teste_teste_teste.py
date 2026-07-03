import h5py
import requests
import pandas as pd
from gwosc.locate import get_event_urls
from pathlib import Path
from tqdm import tqdm

df = pd.read_csv("gw_filtered_events.csv")
shortName = df['shortName']

print("Currently downloading...")
N = len(shortName)

for i in tqdm(range(N)):
    name = shortName[i]
    folder = Path(f'../data/{name}')
    folder.mkdir(parents=True, exist_ok=True)

    base_name = name.split('-')[0]
    
    try:
        urls = get_event_urls(base_name)
        
        # FILTRO CORRIGIDO: 
        # Pega arquivos de 32 segundos, mas ignora os de 16 kHz (seja '16KHZ' ou 'LOSC_16')
        # Assim, sobram sempre as versões de 4 kHz, independente da época.
        filtered_urls = [u for u in urls if '32.hdf5' in u and '16KHZ' not in u and '_16_' not in u]
        
        if not filtered_urls:
            print(f"\nAviso: Nenhum arquivo de 32s encontrado para {base_name}.")
            continue

        for url in filtered_urls:
            name_file = url.split("/")[-1]
            detector = name_file.split("_")[0]
            sigla = detector.split("-")[-1]
            
            target_path = folder / f'strain_{sigla}.hdf5'
            
            if not target_path.exists():
                response = requests.get(url, stream=True)
                with open(target_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
    except Exception as e:
        print(f"\nErro ao processar {name}: {e}")