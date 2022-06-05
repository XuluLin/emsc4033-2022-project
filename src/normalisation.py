import os
import glob
import copy
import obspy
import scipy
import time
import pycwt
import pyasdf
import datetime
import numpy as np
import pandas as pd
import sys
from numba import jit
from scipy.signal import hilbert
from obspy.signal.util import _npts2nfft
from obspy.signal.invsim import cosine_taper
from scipy.fftpack import fft,ifft,next_fast_len
from obspy.signal.filter import bandpass,lowpass
from obspy.signal.regression import linear_regression
from obspy.core.util.base import _get_function_from_entry_point
from obspy.core.inventory import Inventory, Network, Station, Channel, Site
from obspy.clients.fdsn import Client
from scipy.signal import butter, lfilter


'''
    This script implements the frequency-time normalisation to pre-proccessed data: 
    1) compute the target frequency range according to their instrument type 
    2) slice this frequency range into small frequency windows with a fixed interval 
    3) construct butterworth bandpass filter at requested frequencies
    4) calculate the Hilbert transformed data and returns normalised arrays 
    
    Functions: target_frequency, target_frequency_window, butter_bandpass, butter_bandpass_filter, normalisation. 
'''


def target_frequency (chan, freqmin, freqmax):
    '''This function returns the target frequency range for FTN dependent on the type of instrument.
       
       Parameters: 
       chan (string): the type of instrument. 'HHZ' 'BHZ' or 'LHZ'. (Only vertical component is considered in this project)
       freqmin (float): the minimum frequency used to DOWNLOAD raw data.
       freqmax (float): the maximum frequency used to DOWNLOAD raw data.
       
       Returns: 
       (freq_low, freq_high): a tuple of targeted frequency range to do FTN. 
    '''
    
    #expected frequency range for different types of instrument
    
    target_hh_low = 0.00167 #very broad band
    target_hh_high = 0.07   #very borad band 
    target_bh_low = 0.0033  #all other band width
    target_bh_high = 0.07   #all other band width

    
    if chan == 'HHZ':
        
        #if the lowest DOWNLOAD frequency is less than the EXPECTED lowest frequency
        #the FILTERING lowest frequency should be the EXPECTED lowest frequency
        #otherwise, FILTERING frequency will be the lowest DOWNLOAD frequency
        
        if freqmin < target_hh_low:
            freq_low = target_hh_low
        else: 
            freq_low = freqmin
        
        if freqmax > target_hh_high:
            
        #if the highest DOWNLOAD frequency is more than the EXPECTED highest frequency
        #the FILTERING highest frequency should be the EXPECTED highest frequency
        #otherwise, FILTERING frequency will be the highest DOWNLOAD frequency
        
            freq_high = target_hh_high
        else: 
            freq_high = freqmax
        
    elif chan == 'BHZ' or 'LHZ':
        
        if freqmin < target_bh_low:
            freq_low = target_bh_low
        else: 
            freq_low = freqmin
        
        if freqmax > target_bh_high:
            freq_high = target_bh_high
        else: 
            freq_high = freqmax  
    


    
    return freq_low, freq_high
    

def target_frequency_window(chan, freqmin, freqmax):
    '''This function slices the target frequency range for each frequency window.
       
       Parameters: 
       chan (list): the type of instrument. 'HHZ' 'BHZ' or 'LHZ'. (Only vertical component is considered in this project)
       freqmin: the minimum frequency used to DOWNLOAD raw data.
       freqmax: the maximum frequency used to DOWNLOAD raw data.
       
       Returns: 
       frange (list of tuples): a list of lowest & highest frequencies for each frequency window. 
    '''
    
    target_freq = target_frequency (chan, freqmin, freqmax) #call the previous function to return the targeted FILTERING range
    freq_low = target_freq[0] 
    freq_high = target_freq[1]
    
    df = freq_low/4
    fstart = freq_low #start from the lowest frequency 

    frange = [] 

    while fstart <= freq_high-df:
        frange_tuple = (fstart, fstart+df)
        frange.append(frange_tuple)
        fstart = fstart + df 
    
    if len(frange) < 1:
        raise ValueError("The output list should not be empty.")

    return frange


def butter_bandpass(lowcut, highcut, fs, order=2):
    '''This function returns the parameters for a butterworth filter. 
    
       Parameters: 
       lowcut (float): the lowest frequency of a butterworth filter
       highcut (float): the highest frequency of a butterworth filter
       fs (float): sample frequency 
       order (float): the order of a butterworth filter. Default is 2 which gives the best normalisation results. 
       
       Returns: 
       b (numpy ndarray): the numerator of a butterworth filter
       a (numpy ndarrya): the denominator of a butterworth filter
    
    '''
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band') #bandpass filter
    return b, a #numerator and denominator polynomials of IIR filter 


def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
    '''This function returns the butterworth-filtered data. 
    
       Parameters: 
       data (obspy trace): the unfiltered obspy trace data 
       lowcut (float): the lowest frequency of a butterworth filter
       highcut (float): the highest frequency of a butterworth filter
       fs (float/int): sample frequency 
       order (float/int): the order of a butterworth filter. Default is 2 which gives the best normalisation results. 
       
       Returns: 
       y (numpy ndarray): the butterworth-filtered data
    
    '''
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data) #filter data along one dimension
    
    if len(y)<1:
        raise ValueError("The output cannot be empty.")
    
    return y



def normalisation_filtering(target_frequency_window, samp_freq, ntr):
    '''This function performs filtering for normalisation. 
    
       Parameters: 
       target_frequency_window (list): all the possiible frequency windows for filtering within the desired range
       samp_freq (float): sampling frequency
       ntr (numpy ndarray): the pre-proccessed data
       
       Returns:
       filtered_list (list): filtered waveform for each frequency window. 
       
    '''
    
    filtered_list = []
    for freq_range in target_frequency_window: 
        #the lowest and highest frequencies in each frquency window
        lowcut = freq_range[0]
        highcut = freq_range[1]    
        #filtering 
        butter_bandpass(lowcut, highcut, samp_freq)
        filtered_ntr = butter_bandpass_filter(ntr, lowcut, highcut, samp_freq)
        filtered_list.append(filtered_ntr)
    
    if len(filtered_list)<1:
        raise ValueError ("The output of this function should not be empty.")
        
    return filtered_list
    

def freq_time_normalisation(target_frequency_window, samp_freq, ntr):
    '''This function returns the frequency-time normalised data using Hilbert transform. The filtered data is divided by its
       envelope function after Hilbert transform for each target_frequency_window. The formula can be referred to 
       https://pubs.geoscienceworld.org/ssa/bssa/article/102/4/1872/325525/an-improved-method-to-extract-very-broadband.
       
       Parameters: 
       target_frequency_window (list): all the possiible frequency windows for filtering within the desired range
       samp_freq (float): sampling frequency
       ntr (numpy ndarray): the pre-proccessed data
       
       Returns: 
       ntr_list (list): contains all the normalised segments for each frequency window. 
    '''
    #call the previous function to obtain filtered waveform
    filtered_list = normalisation_filtering(target_frequency_window, samp_freq, ntr)
    
    #create an empty list to store FT normalised waveform
    ntr_list = []
    
    #Hilbert transform
    for filt in filtered_list:
        analytical_qrz = hilbert(filt)
    #the absolute value of hilbert transform
        amplitude_envelope = np.abs(analytical_qrz)
    #normalisation
        FTN = filt/amplitude_envelope
        ntr_list.append(FTN)
        
    if len(ntr_list)<1:
        raise ValueError ("The output of this function should not be empty.")
        
    return ntr_list
        