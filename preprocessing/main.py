import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries  # <-- Adicione esta importação
from gwpy.signal import filter_design
from gwpy.plot import Plot

data_parameters = pd.read_csv('gw_filtered_events.csv')
shortName = data_parameters['shortName']


'''
N = 2
for i in range(1,2,1):

    folder = shortName[i]
    
    pathH1 = f'../data/{shortName[i]}/strain_H1.hdf5'
    pathL1 = f'../data/{shortName[i]}/strain_L1.hdf5'

    strain_data_H1 = TimeSeries.read(pathH1, format='hdf5.gwosc')
    strain_data_L1 = TimeSeries.read(pathL1, format='hdf5.gwosc')

    puro = strain_data_H1

    bp = filter_design.bandpass(50, 250, strain_data_H1.sample_rate)
    notches = [filter_design.notch(line, strain_data_H1.sample_rate) for line in (60, 120, 180)]
    zpk = filter_design.concatenate_zpks(bp, *notches)
    hfilt = strain_data_H1.filter(zpk, filtfilt=True)
    
    strain_data_H1 = strain_data_H1.crop(*strain_data_H1.span.contract(1))
    hfilt = hfilt.crop(*hfilt.span.contract(1))

    plot = Plot(strain_data_H1, hfilt, figsize=[12, 6], separate=True, sharex=True, color='gwpy:ligo-hanford')
    ax1, ax2 = plot.axes
    ax1.set_title('LIGO-Hanford strain data around GW150914')
    ax1.text(1.0, 1.01, 'Unfiltered data', transform=ax1.transAxes, ha='right')
    ax1.set_ylabel('Amplitude [strain]', y=-0.2)
    ax2.set_ylabel('')
    ax2.text(1.0, 1.01, r'50-250\,Hz bandpass, notches at 60, 120, 180 Hz', transform=ax2.transAxes, ha='right')
    plot.show()

    plt.plot(strain_data_H1)
    plt.show()
'''




N = 2
for i in range(1,2,1):

    folder = shortName[i]
    
    pathH1 = f'../data/{shortName[i]}/strain_H1.hdf5'
    pathL1 = f'../data/{shortName[i]}/strain_L1.hdf5'

    strain_data_H1 = TimeSeries.read(pathH1, format='hdf5.gwosc')
    strain_data_L1 = TimeSeries.read(pathL1, format='hdf5.gwosc')

    puro = strain_data_H1

    bp = filter_design.bandpass(50, 250, strain_data_H1.sample_rate)
    notches = [filter_design.notch(line, strain_data_H1.sample_rate) for line in (60, 120, 180)]
    zpk = filter_design.concatenate_zpks(bp, *notches)
    hfilt = strain_data_H1.filter(zpk, filtfilt=True)
    
    strain_data_H1 = strain_data_H1.crop(*strain_data_H1.span.contract(1))
    hfilt = hfilt.crop(*hfilt.span.contract(1))

    plot = Plot(strain_data_H1, hfilt, figsize=[12, 6], separate=True, sharex=True, color='gwpy:ligo-hanford')
    ax1, ax2 = plot.axes
    ax1.set_title('LIGO-Hanford strain data around GW150914')
    ax1.text(1.0, 1.01, 'Unfiltered data', transform=ax1.transAxes, ha='right')
    ax1.set_ylabel('Amplitude [strain]', y=-0.2)
    ax2.set_ylabel('')
    ax2.text(1.0, 1.01, r'50-250\,Hz bandpass, notches at 60, 120, 180 Hz', transform=ax2.transAxes, ha='right')
    plot.show()

    plt.plot(strain_data_H1)
    plt.show()
