import re
import time
import csv
import pandas as pd
from gwosc.datasets import find_datasets
from gwosc.api import fetch_event_json
from tqdm import tqdm


start_time = time.perf_counter()

# 1. We define only the most reliable and updated catalogs
target_catalogs = [
    'GWTC-1-confident',
    'GWTC-2.1-confident', 
    'GWTC-3-confident',
    'GWTC-4.1',           
    'GWTC-5.0',
    'O4_Discovery_Papers'
]

consolidated_events = {}

print("Downloading and filtering events...")

for cat in target_catalogs:
    events = find_datasets(type='event', catalog=cat)
    
    for event in events:
        # Uses Regular Expression to separate the base name from the version. E.g.: 'GW150914-v4'
        match = re.match(r"(.+)-v(\d+)$", event)
        
        if match:
            base_name = match.group(1)     # E.g.: 'GW150914'
            version = int(match.group(2))  # E.g.: 4
        else:
            # Some new events might not have a suffix yet
            base_name = event
            version = 1 
            
        # Replacement logic: if the event is already in the dictionary, check if the current version is higher
        if base_name in consolidated_events:
            if version > consolidated_events[base_name]['version']:
                consolidated_events[base_name] = {'full_name': event, 'version': version}
        else:
            # If the event is new, add it to the dictionary
            consolidated_events[base_name] = {'full_name': event, 'version': version}

# Extract only the final full names from our filtering process
final_list = [data['full_name'] for data in consolidated_events.values()]
final_list.sort() # Sort alphabetically/chronologically

print("="*50)
print(f"TOTAL UNIQUE AND UPDATED EVENTS: {len(final_list)}")
print("="*50)

# Displaying the first 10 events just to check the output
print("\nFirst 10 events of the consolidated list:")
print(final_list[:10])
print('\n')



filename = 'gw_events.csv'
    
headers = [
    'shortName', 'GPS', 'mass_1_source', 'mass_2_source', 'total_mass_source', 'final_mass_source', 'snr', 'luminosity_distance', 
    'chi_eff',  'chirp_mass_source', 'redshift' 
]

# ABRIR O ARQUIVO ANTES DO LOOP
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Escreve o cabeçalho uma única vez

N_events = len(final_list)
for i in tqdm(range(N_events)):


    name_event = final_list[i]
    data = fetch_event_json(name_event)

    # Os dados ficam organizados dentro da chave 'events' e depois no nome do evento
    parameters = data['events'][name_event]

    # Extraindo as massas (os valores vêm em Massas Solares)
    gps_time = parameters.get('GPS')
    massa_1 = parameters.get('mass_1_source')
    massa_2 = parameters.get('mass_2_source')
    network = parameters.get('network_matched_filter_snr')
    lum_dis = parameters.get('luminosity_distance')
    chi_eff = parameters.get('chi_eff')
    tot_mass = parameters.get('total_mass_source')
    chirp_mass_source = parameters.get('chirp_mass_source')
    redshift = parameters.get('redshift')
    final_mass_source = parameters.get('final_mass_source')

    row_data = [name_event, gps_time, massa_1, massa_2, tot_mass, final_mass_source, network, lum_dis, chi_eff, chirp_mass_source, redshift]

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(row_data)


    
print(f"\n\n=================== Event {name_event} ===================")
print(f"GPS time: {gps_time} s")
print(f"Massa do objeto primário (Massa 1): {massa_1} massas solares")
print(f"Massa do objeto secundário (Massa 2): {massa_2} massas solares")
print(f'network-matched-filter-snr: {network}')
print(f'Luminosity distance: {lum_dis} Mpc')
print(f'chi_eff: {chi_eff}')
print(f'total mass source: {tot_mass} massas solares')
print(f'Chirp mass: {chirp_mass_source} massas solares')
print(f'redshift: {redshift}')
print(f'Final mass source: {final_mass_source}')
print("==========================================================")


end_time = time.perf_counter()
elapsed_time = (end_time - start_time)/60.0
print(f"\nExecution time: {elapsed_time:.6f} minutes")


df = pd.read_csv("gw_events.csv")
df_filtered = df.dropna()
print("\n Filtered DataFrame")
print(df_filtered.head())

Ntotal = len(df)
Nfilte = len(df_filtered)
print(f"Number of events: {Ntotal}")
print(f"Number of filtered events: {Nfilte}")

df_filtered.to_csv("gw_filtered_events.csv", index=False)