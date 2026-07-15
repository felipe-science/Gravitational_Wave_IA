import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pycbc.waveform import get_td_waveform
from pycbc.filter import resample_to_delta_t, highpass
import matplotlib.pyplot as plt


data_parameters = pd.read_csv('gw_filtered_events.csv')
shortName = data_parameters['shortName']




# The output of this function are the "plus" and "cross" polarizations of the gravitational-wave signal 
# as viewed from the line of sight at a given source inclination (assumed face-on if not provided)
hp, hc = get_td_waveform(approximant="SEOBNRv4_opt",
                         mass1=10,
                         mass2=10,
                         delta_t=1.0/4096,
                         f_lower=30,
                         distance=10)
plt.plot(hp.sample_times, hp, label='100 Mpc')


'''
hp, hc = get_td_waveform(approximant="SEOBNRv4_opt",
                         mass1=10,
                         mass2=10,
                         delta_t=1.0/4096,
                         f_lower=30,
                         distance=100)
plt.plot(hp.sample_times, hp, label='Plus Polarization')
'''




plt.xlabel('Time (s)')
plt.ylabel('Strain')
plt.legend(loc='best')
plt.show()