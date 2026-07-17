import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pycbc.waveform import get_td_waveform
from pycbc.filter import resample_to_delta_t, highpass, matched_filter
from pycbc.psd import interpolate, inverse_spectrum_truncation
from gwpy.timeseries import TimeSeries  # <-- Adicione esta importação


data_parameters = pd.read_csv('gw_filtered_events.csv')
shortName = data_parameters['shortName']

'''
# The output of this function are the "plus" and "cross" polarizations of the gravitational-wave signal 
# as viewed from the line of sight at a given source inclination (assumed face-on if not provided)
hp, hc = get_td_waveform(approximant="SEOBNRv4_opt",
                         mass1=10,
                         mass2=10,
                         delta_t=1.0/4096,
                         f_lower=30,
                         distance=10)
plt.plot(hp.sample_times, hp, label='100 Mpc')
plt.xlabel('Time (s)')
plt.ylabel('Strain')
plt.legend(loc='best')
plt.show()
'''


for i in range(1):

    pathH1 = f'../data/{shortName[i]}/strain_H1.hdf5'
    pathL1 = f'../data/{shortName[i]}/strain_L1.hdf5'

    strain_H1_gwpy = TimeSeries.read(pathH1, format='hdf5.gwosc')
    strain_L1_gwpy = TimeSeries.read(pathL1, format='hdf5.gwosc')

    strain_H1_pycbc = strain_H1_gwpy.to_pycbc()
    strain_L1_pycbc = strain_L1_gwpy.to_pycbc()

    # 3. Aplica o highpass e o resample usando as funções nativas do PyCBC
    strain_H1 = resample_to_delta_t(highpass(strain_H1_pycbc, 15.0), 1.0/2048)
    strain_L1 = resample_to_delta_t(highpass(strain_L1_pycbc, 15.0), 1.0/2048)

    plt.plot(strain_H1.sample_times, strain_H1)
    plt.xlabel('Time (s)')
    plt.show()

    #Remove 2 seconds of data from both the beginning and end
    conditioned = strain_H1.crop(2,2)
    plt.plot(conditioned.sample_times, conditioned)
    plt.xlabel('Times (s)')
    plt.show()

    psd = conditioned.psd(4)
    psd = inverse_spectrum_truncation(psd, int(4*conditioned.sample_rate), low_frequency_cutoff=15)

    plt.loglog(psd.sample_frequencies, psd)
    plt.ylabel('$Strain^2$ / Hz')
    plt.xlabel('Frequency (Hz)')
    plt.xlim(30, 1024)
    plt.show()


    #In this case we "know" what the signal parameters are. In a search
    #We would grid over the parameters and calculate the SNR times series
    #for which one

    #We'll assume equal masses, which is within the posterior probability
    # of GW150914
    m = 36
    hp, hc = get_td_waveform(approximant="SEOBNRv4_opt",
                         mass1=m,
                         mass2=m,
                         delta_t=conditioned.delta_t,
                         f_lower=20)
    hp.resize(len(conditioned))

    # The waveform begins at the start of the vector, so if we want the
    # SNR times series to correspond to the approximate merger location
    # we need to shift the data so that the merger is approximately at
    # the first bin of the data.

    # This function rotates the vector by a fixed amount of times.
    # It treats the data as if were on a ring. Note that time stamps
    # are *not* in general affected, but the true position in the vector
    # is.

    # By convention waveforms returned from 'get_td_waveform' have their
    # merger stamped with zero, so we can use the start time to shift the
    # merger into position
    template = hp.cyclic_time_shift(hp.start_time)
    plt.plot(template)
    plt.show()



    # Remove time corrupted by the template filter and the psd filter
    # we remove 4 seconds at the beginning and end for the PSD filtering
    # An we remove 4 additional seconds at the beginning to account for
    # the template length (this is somewhat generous for so short a template)
    # A longer signal such as from a BNS, would require much

    #https://colab.research.google.com/github/gwastro/pycbc-tutorials/blob/master/tutorial/3_WaveformMatchedFilter.ipynb#scrollTo=W2iIdF9g3sfb