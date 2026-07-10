import requests
import pandas as pd
from gwosc.locate import get_event_urls
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def baixar_single_url(url, folder):
    """Função focada em baixar uma única URL de forma eficiente"""
    name_file = url.split("/")[-1]
    detector = name_file.split("_")[0]
    sigla = detector.split("-")[-1]
    file_path = folder / f'strain_{sigla}.hdf5'
    
    # Se o arquivo já existe e tem tamanho maior que zero, pula para poupar tempo
    if file_path.exists() and file_path.stat().st_size > 0:
        return
        
    try:
        # Aumentamos o chunk_size para 1MB para acelerar a escrita em disco
        with requests.get(url, stream=True, timeout=15) as response:
            response.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    f.write(chunk)
    except Exception as e:
        print(f"\n[Erro] Falha ao baixar {url}: {e}")

# --- Código Principal ---
df = pd.read_csv("gw_filtered_events.csv")
short_names = df['shortName']

print(f"Preparando o download de sinais para {len(short_names)} eventos...")

# Lista para acumular todas as tarefas de download (URL, pasta_destino)
tarefas_download = []

# Primeiro, coletamos as URLs rapidamente (isso evita travar a barra de progresso do download)
for name in tqdm(short_names, desc="Coletando URLs da API"):
    folder = Path(f'../data/{name}')
    folder.mkdir(parents=True, exist_ok=True)
    
    try:
        urls = get_event_urls(name)
        for url in urls:
            tarefas_download.append((url, folder))
    except Exception as e:
        print(f"\nErro ao localizar o evento {name}: {e}")

print(f"\nTotal de arquivos individuais encontrados: {len(tarefas_download)}")
print("Iniciando downloads paralelos com velocidade máxima...\n")

# Dispara os downloads em paralelo (max_workers=5 gerencia bem sem sobrecarregar a rede)
with ThreadPoolExecutor(max_workers=5) as executor:
    # Usamos o tqdm para envelopar a execução paralela e ver o progresso real
    list(tqdm(
        executor.map(lambda t: baixar_single_url(t[0], t[1]), tarefas_download),
        total=len(tarefas_download),
        desc="Baixando arquivos"
    ))

print("\n🎉 Todos os downloads foram concluídos com sucesso!")