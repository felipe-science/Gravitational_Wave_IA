import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries  # <-- Adicione esta importação

data_parameters = pd.read_csv('gw_filtered_events.csv')

shortName = data_parameters['shortName']

N = 1
for i in range(N):

    folder = shortName[i]
    
    pathH1 = f'../data/{shortName[i]}/strain_H1.hdf5'
    pathL1 = f'../data/{shortName[i]}/strain_L1.hdf5'

    strain_data_H1 = TimeSeries.read(pathH1, format='hdf5.gwosc')
    strain_data_L1 = TimeSeries.read(pathL1, format='hdf5.gwosc')



    high_passed_H1 = strain_data_H1.highpass(15)
    white_strain_H1 = high_passed_H1.whiten(4, 2)
    filtered_strain_H1 = white_strain_H1.bandpass(30, 400)
    fig = filtered_strain_H1.plot(title=f'Strain Filtrado - H1 ({folder})')
    plt.show()
