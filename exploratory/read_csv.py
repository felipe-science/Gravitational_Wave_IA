import h5py
import pandas as pd


df_events = pd.read_csv('gw_filtered_events.csv')
shotName = df_events['shotName']

caminho = '../data/GW150914-v4/strain_H1.hdf5'

# 1. Abre com h5py para extrair a série temporal bruta
with h5py.File(caminho, 'r') as f:
    # Acessa o dataset real de deformação (strain)
    dados_brutos = f['strain/Strain'][:]

# 2. Transforma esses dados brutos em um DataFrame do Pandas
df = pd.DataFrame(dados_brutos, columns=['Strain'])

# Agora você tem todo o poder do Pandas disponível!
print("--- Primeiras linhas do DataFrame ---")
print(df.head())

print("\n--- Estatísticas descritivas do sinal ---")
print(df.describe())



sdhfljdshfdjfdjlkj. adsfuejfdf,bcv,mb