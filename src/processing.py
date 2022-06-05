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
    This script pre-process the downloaded seismic data for normalisation: 
    1) check and remove gaps in data
    2) construct butterworth filter with user-input min/max frequencies
    3) remove nan/inf, mean and trend of each trace
    4) remove instrument response
    
    Functions: portion_gaps, check_sample_gaps, segment_interpolate, preprocess_raw. 
'''

def portion_gaps(stream,date_info):
    '''
    this function tracks the gaps (npts) from the accumulated difference between starttime and endtime
    of each stream trace. it removes trace with gap length > 30% of trace size.
    PARAMETERS:
    -------------------
    stream: obspy stream object
    date_info: dict of starting and ending time of the stream
    RETURNS:
    -----------------
    pgaps: proportion of gaps/all_pts in stream
    '''
    # ideal duration of data
    starttime = date_info['starttime']
    endtime   = date_info['endtime']
    npts      = (endtime-starttime)*stream[0].stats.sampling_rate

    pgaps=0
    #loop through all trace to accumulate gaps
    for ii in range(len(stream)-1):
        pgaps += (stream[ii+1].stats.starttime-stream[ii].stats.endtime)*stream[ii].stats.sampling_rate
    if npts!=0:pgaps=pgaps/npts
    if npts==0:pgaps=1
    return pgaps



def check_sample_gaps(stream,date_info):
    """
    this function checks sampling rate and find gaps of all traces in stream.
    PARAMETERS:
    -----------------
    stream: obspy stream object.
    date_info: dict of starting and ending time of the stream
    RETURENS:
    -----------------
    stream: List of good traces in the stream
    """
    # remove empty/big traces
    if len(stream)==0 or len(stream)>100:
        stream = []
        raise ValueError("The output stream should not be empty.")

    # remove traces with big gaps
    if portion_gaps(stream,date_info)>0.3:
        stream = []
        raise ValueError("The output stream should not be empty.")

    freqs = []
    for tr in stream:
        freqs.append(int(tr.stats.sampling_rate))
    freq = max(freqs)
    for tr in stream:
        if int(tr.stats.sampling_rate) != freq:
            stream.remove(tr)
        if tr.stats.npts < 10:
            stream.remove(tr)

    return stream




#def segment_interpolate(sig1,nfric):
    #'''
    #this function interpolates the data to ensure all points located on interger times of the
    #sampling rate (e.g., starttime = 00:00:00.015, delta = 0.05.)
    #PARAMETERS:
    #----------------------
    #sig1:  seismic recordings in a 1D array
    #nfric: the amount of time difference between the point and the adjacent assumed samples
    #RETURNS:
    #----------------------
    #sig2:  interpolated seismic recordings on the sampling points
    #'''
    #npts = len(sig1)
    #sig2 = np.zeros(npts,dtype=np.float32)

    #----instead of shifting, do a interpolation------
    #for ii in range(npts):

        #----deal with edges-----
        #if ii==0 or ii==npts-1:
            #sig2[ii]=sig1[ii]
        #else:
            #------interpolate using a hat function------
            #sig2[ii]=(1-nfric)*sig1[ii+1]+nfric*sig1[ii]

    #return sig2




def preprocess_raw(st,inv,prepro_para,date_info):
    '''
    this function pre-processes the raw data stream by:
        1) remove sigularity, trend and mean of each trace
        2) filter and correct the time if integer time are between sampling points
        3) remove instrument responses with selected methods including:
            "inv"   -> using inventory information to remove_response;
            "RESP_files" -> use the raw download RESP files;
            "polezeros"  -> use pole/zero info for a crude correction of response
        4) trim data to a day-long sequence and interpolate it to ensure starting at 00:00:00.000
    
    PARAMETERS:
    -----------------------
    st:  obspy stream object, containing noise data to be processed
    inv: obspy inventory object, containing stations info
    prepro_para: dict containing fft parameters, such as frequency bands and selection for instrument response removal etc.
    date_info:   dict of start and end time of the stream data
    RETURNS:
    -----------------------
    ntr: obspy trace object of cleaned, merged and filtered noise data
    '''
    # load paramters from fft dict
    rm_resp       = prepro_para['rm_resp']
    if 'rm_resp_out' in prepro_para.keys():
        rm_resp_out   = prepro_para['rm_resp_out']
    else:
        rm_resp_out   = 'VEL'
    respdir       = prepro_para['respdir']
    freqmin       = prepro_para['freqmin']
    freqmax       = prepro_para['freqmax']
    samp_freq     = prepro_para['samp_freq']

    # parameters for butterworth filter
    f1 = 0.9*freqmin;f2=freqmin
    if 1.1*freqmax > 0.45*samp_freq:
        f3 = 0.4*samp_freq
        f4 = 0.45*samp_freq
    else:
        f3 = freqmax
        f4= 1.1*freqmax
    pre_filt  = [f1,f2,f3,f4]


    sps = int(st[0].stats.sampling_rate)
    station = st[0].stats.station

    # remove nan/inf, mean and trend of each trace before merging
    for ii in range(len(st)):

        #-----set nan/inf values to zeros (it does happens!)-----
        tttindx = np.where(np.isnan(st[ii].data))
        if len(tttindx) >0:st[ii].data[tttindx]=0
        tttindx = np.where(np.isinf(st[ii].data))
        if len(tttindx) >0:st[ii].data[tttindx]=0
        
        #remove trend in data
        st[ii].data = np.float32(st[ii].data)
        st[ii].data = scipy.signal.detrend(st[ii].data,type='constant') 
        st[ii].data = scipy.signal.detrend(st[ii].data,type='linear')

    # merge, taper and filter the data
    if len(st)>1:st.merge(method=1,fill_value=0)
    st[0].taper(max_percentage=0.05,max_length=50)	# taper window
    st[0].data = np.float32(bandpass(st[0].data,pre_filt[0],pre_filt[-1],df=sps,corners=4,zerophase=True)) #filtered with butterworth filter

    
    
    # options to remove instrument response
    if rm_resp != 'no':
        if rm_resp != 'inv':
            if (respdir is None) or (not os.path.isdir(respdir)):
                raise ValueError('response file folder not found! abort!')

        if rm_resp == 'inv':
            #----check whether inventory is attached----
            if not inv[0][0][0].response:
                raise ValueError('no response found in the inventory! abort!')
            else:
                try:
                    print('removing response for %s using inv'%st[0])
                    st[0].attach_response(inv)
                    st[0].remove_response(output=rm_resp_out,pre_filt=pre_filt,water_level=60)
                except Exception:
                    st = []
                    return st

        elif rm_resp == 'RESP':
            print('remove response using RESP files')
            resp = glob.glob(os.path.join(respdir,'RESP.'+station+'*'))
            if len(resp)==0:
                raise ValueError('no RESP files found for %s' % station)
            seedresp = {'filename':resp[0],'date':date_info['starttime'],'units':'DIS'}
            st.simulate(paz_remove=None,pre_filt=pre_filt,seedresp=seedresp[0])

        elif rm_resp == 'polozeros':
            print('remove response using polos and zeros')
            paz_sts = glob.glob(os.path.join(respdir,'*'+station+'*'))
            if len(paz_sts)==0:
                raise ValueError('no polozeros found for %s' % station)
            st.simulate(paz_remove=paz_sts[0],pre_filt=pre_filt)

        else:
            raise ValueError('no such option for rm_resp! please double check!')

    
    # trim a continous segment into user-defined sequences
    ntr = st[0].trim(starttime=date_info['starttime'],endtime=date_info['endtime'],pad=True,fill_value=0)
    

    return ntr
