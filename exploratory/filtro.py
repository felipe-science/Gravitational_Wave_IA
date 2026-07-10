import h5py
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import butter, filtfilt

# --- FUNÇÕES DE PROCESSAMENTO ---

def filtro_bandpass(dados, lowcut, highcut, fs, order=4):
    """Aplica um filtro passa-banda para remover frequências fora do alvo."""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, dados)
    return y

def branquear_sinal(dados, fs):
    """Iguala o peso das frequências (Whitening) para destacar o sinal sobre o ruído."""
    # Passa o sinal para o domínio da frequência
    dados_freq = np.fft.rfft(dados)
    
    # Calcula a densidade espectral de potência (PSD) simplificada
    psd = np.abs(dados_freq) ** 2
    
    # Suaviza a PSD para não apagar o sinal real
    psd_suave = np.convolve(psd, np.ones(100)/100, mode='same')
    psd_suave[psd_suave == 0] = 1e-25 # Evita divisão por zero matemática
    
    # Divide pelo ruído e volta para o domínio do tempo
    dados_brancos_freq = dados_freq / np.sqrt(psd_suave)
    dados_brancos = np.fft.irfft(dados_brancos_freq, n=len(dados))
    
    return dados_brancos


# --- LOOP PRINCIPAL ---

# 1. Configuração dos caminhos
caminho = Path('../data')
diretorios = [item.name for item in caminho.iterdir() if item.is_dir()]

# 2. Iterando sobre cada pasta de evento
for dir_nome in diretorios:
    path = caminho / dir_nome / 'strain_H1.hdf5'
    
    if path.exists():
        print(f"Processando evento: {dir_nome} ...")
        
        with h5py.File(path, 'r') as f:
            try:
                # Extração e limpeza básica
                dados_strain = f['strain']['Strain'][:]
                dados_strain = np.nan_to_num(dados_strain, nan=0.0)
                
                # Configurações de tempo e amostragem (LIGO = 4096 Hz)
                fs = 4096  
                duracao = 4096
                tempo = np.linspace(0, duracao, len(dados_strain))
                
                # --- A MÁGICA ACONTECE AQUI ---
                # 3. Branqueia o sinal primeiro (Whitening)
                dados_brancos = branquear_sinal(dados_strain, fs)
                
                # 4. Aplica o filtro passa-banda (30 a 300 Hz)
                dados_filtrados = filtro_bandpass(dados_brancos, 30, 300, fs)
                
                # 5. Define a janela de Zoom (Meio segundo ao redor da colisão)
                janela = (tempo >= 2048.0) & (tempo <= 2048.5)
                
                # --- PLOTAGEM ---
                plt.figure(figsize=(10, 4))
                plt.plot(tempo[janela], dados_filtrados[janela], color='crimson', label='Sinal de GW Limpo')
                
                plt.title(f"Assinatura da Colisão - Evento {dir_nome}")
                plt.xlabel("Tempo de Gravação (s)")
                plt.ylabel("Amplitude Normalizada (Whitened)")
                plt.grid(True, alpha=0.5)
                plt.legend()
                
                plt.tight_layout()
                plt.show()
                
            except KeyError:
                print(f"-> Estrutura não reconhecida no arquivo do evento {dir_nome}.")