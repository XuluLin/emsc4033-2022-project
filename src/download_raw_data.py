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


'''
    This script contains two functions: get_event_list and download.
    
    This script retrieves datetime information as requested and download seismic data and corresponding inventories that contains 
    information on network --> station --> channel. 
'''


def get_event_list(str1,str2,inc_hours):
    '''
    This function calculates the event list between time1 and time2 by increment of inc_hours
    in the format of %Y_%m_%d_%H_%M_%S' (str1 and str2)
    PARAMETERS:
    ----------------
    str1: string of the starting time e.g. 2010_01_01_0_0
    str2: string of the ending time e.g. 2010_10_11_0_0
    inc_hours: integer of incremental hours
    RETURNS:
    ----------------
    event: a list of event datetime
    '''
    #extract datetime information from strings
    date1=str1.split('_') 
    date2=str2.split('_')
    y1=int(date1[0]);m1=int(date1[1]);d1=int(date1[2])
    h1=int(date1[3]);mm1=int(date1[4]);mn1=int(date1[5])
    y2=int(date2[0]);m2=int(date2[1]);d2=int(date2[2])
    h2=int(date2[3]);mm2=int(date2[4]);mn2=int(date2[5])

    d1=datetime.datetime(y1,m1,d1,h1,mm1,mn1)
    d2=datetime.datetime(y2,m2,d2,h2,mm2,mn2)
    dt=datetime.timedelta(hours=inc_hours)

    event = []
    while(d1<d2):
        event.append(d1.strftime('%Y_%m_%d_%H_%M_%S'))
        d1+=dt
    event.append(d2.strftime('%Y_%m_%d_%H_%M_%S'))
    if len(event) < 1:
        raise ValueError('output event datetime list is empty.')
    
    return event


def download(all_chunk,nsta,net,sta,location,direc,chan,client,ncomp):
    '''
    This function downloads the raw waveform for requested stations and times. 
    PARAMETERS:
    ----------------
    all_chunk: a numpy character list that contains events from get_event_list
    nsta: an integer of number of stations 
    net: a list of string that specifies the networks of stations
    sta: a list of string that specifies the station names 
    location: a list of string that specifies the locations of stations
    direc: a string of path to store the data
    chan: a list of string that specifies the channels of stations
    client: data centre of obspy.Client
    ncomp: an interger of the number of cross-correlation component
    
    RETURNS:
    ----------------
    tr_list: a list of obspy Stream traces that contain the raw waveform 
    inv_list: a list of metedata of the donwloaded waveform
    date_info: a dictionary of start and end time of downloaded waveform
    '''
    
    #create empty list to store obspy trace of waveform data and inventory information
    inv_list = []
    tr_list = []
    
    #loop through each event
    for ick in range(len(all_chunk)-1):

        s1=obspy.UTCDateTime(all_chunk[ick]) #start time
        s2=obspy.UTCDateTime(all_chunk[ick+1]) #end time 
        date_info = {'starttime':s1,'endtime':s2} 
    
        # keep a track of the channels already exists
        num_records = np.zeros(nsta,dtype=np.int16) #number of stations
    # loop through each channel
        for ista in range(nsta):
            # continue when there are alreay data for sta A at day X
            if num_records[ista] == ncomp:
                continue

            # get inventory for specific station
            inv = client.get_stations(network=net[ista],
                                            station=sta[ista],
                                            location=location[ista],
                                            starttime=s1,
                                            endtime=s2,
                                            level="response")
            inv_list.append(inv)
            
            if len(inv_list)<1: 
                raise ValueError("The inventory of stations cannot be empty.")
            


 
            # get data
            tr = client.get_waveforms(network=net[ista],
                                        station=sta[ista],
                                        channel=chan[ista],
                                        location=location[ista],
                                        starttime=s1,
                                        endtime=s2)
            # filename of the saved file
            ff=os.path.join(direc,all_chunk[ick]+'T'+all_chunk[ick+1]+'.'+sta[ista]+'.'+chan[ista]+'.sac')
            tr.write(ff, format="SAC") 
            tr_list.append(tr)
            
            if len(tr_list) < 1: 
                raise ValueError("The raw waveform list cannot be empty.")
     
    return tr_list, inv_list, date_info
                


