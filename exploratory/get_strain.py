import requests
import pandas as pd
from gwosc.locate import get_event_urls
from pathlib import Path
from tqdm import tqdm

df = pd.read_csv("gw_filtered_events.csv")
short_names = df['shortName']

print(f"Baixando {len(short_names)} sinais...")

# Iterando diretamente sobre os nomes
for name in tqdm(short_names, desc="Progresso Geral dos Eventos"):
    
    # Criação do diretório com Pathlib
    folder = Path(f'../data/{name}')
    folder.mkdir(parents=True, exist_ok=True)

    try:
        urls = get_event_urls(name)
    except Exception as e:
        print(f"\nErro ao localizar o evento {name}: {e}")
        continue

    for url in urls:
        name_file = url.split("/")[-1]
        detector = name_file.split("_")[0]
        sigla = detector.split("-")[-1]
        
        # Cria o caminho do arquivo final diretamente
        file_path = folder / f'strain_{sigla}.hdf5'
        
        # Download por chunks com indicador de progresso visual em tempo real
        try:
            # Adicionado o timeout=15 para o código não travar infinitamente se o servidor da GWOSC oscilar
            with requests.get(url, stream=True, timeout=15) as response:
                response.raise_for_status() 
                
                # Descobre o tamanho total do arquivo em bytes (enviado pelo servidor)
                total_size = int(response.headers.get('content-length', 0))
                
                # Cria uma barra secundária para monitorar os megabytes deste arquivo específico
                with open(file_path, "wb") as f, tqdm(
                    desc=f" ↳ {name} ({sigla})",
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    leave=False # Limpa essa barra da tela quando o arquivo termina, mantendo o terminal limpo
                ) as bar:
                    
                    # Alterado para chunks de 1MB (mais rápido para o disco)
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        f.write(chunk)
                        bar.update(len(chunk)) # Atualiza os MBs baixados na tela
                        
        except requests.exceptions.RequestException as e:
            print(f"\nErro ao baixar {url}: {e}")