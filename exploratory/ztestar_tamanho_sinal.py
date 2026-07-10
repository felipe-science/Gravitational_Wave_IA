import h5py
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

caminho = Path('../data')
diretorios = [item.name for item in caminho.iterdir() if item.is_dir()]

for dir_nome in diretorios:
    
    # CORREÇÃO: Mantemos como objeto Path usando a barra '/'
    path = caminho / dir_nome / 'strain_H1.hdf5'
    
    # Agora o .exists() vai funcionar perfeitamente!
    if path.exists():
        # Ajustado o print para mostrar o nome da pasta mãe (parent) e do arquivo
        print(f"Lendo: {path.name} em {path.parent.name}")
        
        with h5py.File(path, 'r') as f:
            print("Chaves no topo:", list(f.keys()))
            
            try:
                dados_strain = f['strain']['Strain'][:]
                
                print(f"Formato dos dados: {dados_strain.shape}")
                print(f"Primeiros 5 pontos: {dados_strain[:5]}\n")
                print(f"numero de pontos = {len(dados_strain)}")
                

                N = len(dados_strain)
                duracao = 4096
                tempo = np.linspace(0, duracao, N)
                plt.plot(tempo, dados_strain)
                plt.xlabel("tempo (s)")
                plt.ylabel("strain")
                plt.show()
                
            except KeyError:
                print("A estrutura das chaves é diferente neste arquivo.")