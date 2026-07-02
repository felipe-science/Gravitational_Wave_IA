import numpy as np
import pandas as pd

df = pd.read_csv('event-versions.csv')

selected_columns = [
    'catalog', 'shortName', 
    'mass_1_source', 'mass_1_source_lower', 'mass_1_source_upper',
    'mass_2_source', 'mass_2_source_lower', 'mass_2_source_upper',
    'total_mass_source', 'total_mass_source_lower', 'total_mass_source_upper',
    'final_mass_source', 'final_mass_source_lower', 'final_mass_source_upper',
    'luminosity_distance', 'luminosity_distance_lower', 'luminosity_distance_upper',
    'chi_eff', 'chi_eff_lower', 'chi_eff_upper',
    'chirp_mass_source', 'chirp_mass_source_lower', 'chirp_mass_source_upper',
    'redshift', 'redshift_lower', 'redshift_upper', 'p_astro'
]

filtered_df = df[df['catalog'].str.endswith('confident', na=False)][selected_columns]
filtered_df.to_csv('data_gravitational_confident.csv', sep=',', index=False)