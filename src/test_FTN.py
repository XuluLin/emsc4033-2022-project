import pytest
from dependencies import *
import download_raw_data
import processing
import normalisation

def test_event_list(): 
    
    '''
       This function tests
       1) the existence of the function
       2) the input and output types of the function
       3) if the output is an empty list, will the error be raised
       
       ASSERTION: 
       If 1) false: raise exception that the function does not exist.
       If 2) false: Type error: the first two input parameters should be a string and the last input should be an int or a float. 
                                the output should be a list. 
       If 3) false: Value error is not succesfully raised. 
       
    '''
    #test case: inputs
    str1 = "2021_11_01_11_0_0"
    str2 = "2021_11_01_12_0_0"
    inc_hours = 1
    
    #existence of function
    assert download_raw_data.get_event_list, "get_event_list function does not exist." 
    
    #Type of inputs
    assert type(str1) == str, "TypeError, input datetime value should be a string."
    assert type(str1) == str, "TypeError, input datetime value should be a string."
    assert type(inc_hours) == float or int, "TypeError, input inc_hour value should be a float or an integer."
    
    #test case: output
    output1 = download_raw_data.get_event_list (str1, str2, inc_hours)
    
    #type of output
    assert type(output1) == list, "TypeError, output value should be a list of event datetime."
    
    # test if the ValueError for empty output will be raised or not 
    str3 = ''
    str4 = ''
    with pytest.raises(ValueError):
        download_raw_data.get_event_list(str3, str4, inc_hours)


def test_download (): 
    
    '''This function tests
       1) the existence of the function
       2) the input and output types of the function
       
       ASSERTION: 
       If 1) false: raise exception that the function does not exist.
       If 2) false: Type error: the input parameters should be corresponding types described in the error message.
                                the output should be corresponding types described in the error message. 

       
    '''

    #test case: inputs
    all_chunk = ['2021_11_01_11_00_00', '2021_11_01_12_00_00']
    nsta = 2
    net = ['NZ', 'AU']
    sta = ['QRZ', 'LHI']
    location = ['*', '*']
    direc =  '/Users/xulul/Downloads/honours/NoisePy-master/NoisePy-master/FTN/DATA_NZ'
    chan = ['HHZ', 'BHZ']
    client = Client ('IRIS')
    ncomp = 1
    
    #existence of function
    assert download_raw_data.download, "download function does not exist."
    
    #Type of inputs
    assert type(all_chunk) == list, "TypeError, input event datetime should be a list."
    assert type(nsta) == int, "TypeError, input number of stations should be an integer."
    assert type(net) == list, "TypeError, input net should be a lIST of network."
    assert type(sta) == list, "TypeError, input sta should be a lIST of stations."
    assert type(location) == list, "TypeError, input location should be a lIST of locations."
    assert type(direc) == str, "TypeError, input direc should be a string of a directory path."  
    assert type(chan) == list, "TypeError, input chan should be a lIST of channels."
    assert type(client) == obspy.clients.fdsn.client.Client, "TypeError, input client should be an obspy client object of a data centre."
    assert type(ncomp) == int, "TypeError, input ncomp should be an integer of number of cross-correlation components."
    
    #test case: output
    tr_list, inv_list, date_info = download_raw_data.download(all_chunk,nsta,net,sta,location,direc,chan,client,ncomp)
    
    #type of output
    assert type(tr_list) == list, "TypeError"
    for i in range(len(tr_list)): 
        assert type(tr_list[i]) == obspy.core.stream.Stream, "TypeError"
        
    assert type(inv_list) == list, "TypeError"
    for i in range(len(inv_list)): 
        assert type(inv_list[i]) == obspy.core.inventory.inventory.Inventory, "TypeError"
    
    assert type(date_info) == dict, "TypeError, output date_info should be a dictionary."
    
        
def test_portion_gaps():
    
    '''This function tests
    
       1) the existence of the function
       2) the output types of the function
       
       ASSERTION: 
       If 1) false: raise exception that the function does not exist.
       If 2) false: Type error: the outputs should be the corresponding types described in the error message. 
       
       Note: 
       Tests for inputs: portion_gaps take input from the output of download_raw_data.download.
       Hence test for output of download_raw_data.download also tests inputs for portion_gaps.
    '''
    
    #test cases
    all_chunk = ['2021_11_01_11_00_00', '2021_11_01_12_00_00']
    nsta = 2
    net = ['NZ', 'AU']
    sta = ['QRZ', 'LHI']
    location = ['*', '*']
    direc =  '/Users/xulul/Downloads/honours/NoisePy-master/NoisePy-master/FTN/DATA_NZ'
    chan = ['HHZ', 'BHZ']
    client = Client ('IRIS')
    ncomp = 1
    tr_list, inv_list, date_info = download_raw_data.download(all_chunk,nsta,net,sta,location,direc,chan,client,ncomp)
    
    #existence of function
    assert processing.portion_gaps, "portion_gaps function does not exist."
    
    #type of input: portion_gaps take input from the output of download_raw_data.download.
    #Hence test for output of download_raw_data.download also tests inputs for portion_gaps.
    
    #type of output: 
    output1 = processing.portion_gaps(tr_list[0],date_info)
    assert type(output1) == float, "TypeError, output of portion_gaps should be a float number of the percentage of gaps in data."
    

def test_check_sample_gaps():

    '''This function tests
    
       1) the existence of the function
       2) the output types of the function
       3) Whether the output is empty or not
       
       ASSERTION: 
       If 1) false: raise exception that the function does not exist.
       If 2) false: Type error: the outputs should be the corresponding types described in the error message. 
       If 3) false: Value error is not raised successfully.
       
       Note: 
       Tests for inputs: check_sample_gaps take input from the output of download_raw_data.download.
       Hence test for output of download_raw_data.download also tests inputs for portion_gaps.
    '''

    #test cases
    all_chunk = ['2021_11_01_11_00_00', '2021_11_01_12_00_00']
    nsta = 2
    net = ['NZ', 'AU']
    sta = ['QRZ', 'LHI']
    location = ['*', '*']
    direc =  '/Users/xulul/Downloads/honours/NoisePy-master/NoisePy-master/FTN/DATA_NZ'
    chan = ['HHZ', 'BHZ']
    client = Client ('IRIS')
    ncomp = 1
    tr_list, inv_list, date_info = download_raw_data.download(all_chunk,nsta,net,sta,location,direc,chan,client,ncomp)
    
    #existence of function
    assert processing.check_sample_gaps, "check_sample_gaps function does not exist."
    
    #type of output: 
    output1 = processing.check_sample_gaps(tr_list[0],date_info)
    assert type(output1) == obspy.core.stream.Stream, "TypeError, output of check_sample_gaps should be an Obspy stream object."

    # test if the ValueError for empty output will be raised or not 
    stream_except = obspy.Stream()
    with pytest.raises(ValueError):
        processing.check_sample_gaps(stream_except, date_info)
    
    

def test_preprocess_raw():
    
    '''This function tests
    
       1) the existence of the function
       2) the input and output types of the function
       3) when removing instrument response, whether appropriate exceptions will be raised
          --test if the removing option is not one of 'inv', 'RSEP_files', 'polezeros', will the exception be raised?
          --In the processing main script, 'inv' option is preferred. So we test if inv.response is false, will exception be raised?
       
       ASSERTION: 
       If 1) false: raise exception that the function does not exist.
       If 2) false: Type error: the input parameters should be corresponding types described in the error message.
                                the output should be corresponding types described in the error message.  
       If 3) false: Value error is not successfully raised. 
       
       Note:    
       The inputs of preprocess_raw are the outputs of downlaod_raw_data.downlaod.
       Hence the test for downlaod_raw_data.downlaod also tests for the inputs of preprocess_raw except prepro_para. 
       
    '''
    
    #test existence of function 
    assert processing.preprocess_raw, "preprocess_raw function does not exist."
    
    #test case 
    rootpath = '/Users/xulul/Downloads/honours/NoisePy-master/NoisePy-master/FTN'
    samp_freq = 1                               # targeted sampling rate at X samples per seconds 
    rm_resp   = 'inv'                    # select 'no' to not remove response and use 'inv','spectrum','RESP', or 'polozeros' 
    respdir   = os.path.join(rootpath,'resp')    # directory where instrument response files are located 
    freqmin   = 0.005                            # pre filtering minimum frequency bandwidth
    freqmax   = 0.1                              # pre filtering maximum frequency bandwidth
                                             #note this cannot exceed Nquist freq (<= 0.5 samp_freq)                        
    start_date = ["2021_11_01_11_0_0"]           # start date of download, ["year_month_date_hour_minute_second"]
    end_date   = ["2021_11_01_12_0_0"]           # end date of download, ["year_month_date_hour_minute_second"]
    inc_hours  = 1                               # length of data for each request (in hour)
    # assemble parameters used for pre-processing
    prepro_para = {'rm_resp':rm_resp,
               'respdir':respdir,
               'freqmin':freqmin,
               'freqmax':freqmax,
               'samp_freq':samp_freq,
               'start_date':start_date,
               'end_date':end_date,
               'inc_hours':inc_hours}
    
    all_chunk = ['2021_11_01_11_00_00', '2021_11_01_12_00_00']
    nsta = 2
    net = ['NZ', 'AU']
    sta = ['QRZ', 'LHI']
    location = ['*', '*']
    direc =  '/Users/xulul/Downloads/honours/NoisePy-master/NoisePy-master/FTN/DATA_NZ'
    chan = ['HHZ', 'BHZ']
    client = Client ('IRIS')
    ncomp = 1
    tr_list, inv_list, date_info = download_raw_data.download(all_chunk,nsta,net,sta,location,direc,chan,client,ncomp)    
    
    #The inputs of preprocess_raw are the outputs of downlaod_raw_data.downlaod
    #Hence the test for downlaod_raw_data.downlaod also tests for the inputs of preprocess_raw
    #except prepro_para
    assert type(prepro_para) == dict, "TypeError, prepro_para input of pre_process_raw should be a dictionary."
    
    
    #test output type 
    output1 = processing.preprocess_raw(tr_list[0], inv_list[0], prepro_para, date_info)
    assert type(output1) == obspy.core.trace.Trace, "TypeError, output of preprocess_raw should be an Obspy trace object."
    
    #test if exceptions are raised 
    #test option for removing instrument response
    prepro_para_except = {'rm_resp':'spectrum',
               'respdir':respdir,
               'freqmin':freqmin,
               'freqmax':freqmax,
               'samp_freq':samp_freq,
               'start_date':start_date,
               'end_date':end_date,
               'inc_hours':inc_hours}
    
    with pytest.raises(ValueError):
        processing.preprocess_raw(tr_list[0], inv_list[0], prepro_para_except, date_info)
    
    #removing method is by inventory
    #test if the inv.response exception will be raised
    inv_list[0][0][0][0].response = False
    with pytest.raises(ValueError):
        processing.preprocess_raw(tr_list[0], inv_list[0], prepro_para_except, date_info)

        
        
def test_target_frequency():
    
    '''This function tests
    
       1) the existence of the function
       2) the input and output types of the function
       3) the accuracy of the output
       
       ASSERTION: 
       If 1) false: raise exception that the function does not exist.
       If 2) false: Type error: the outputs should be the corresponding types described in the error message. 
       If 3) false: the function does not return the correct result.
       
    '''   
    
    #existence of function 
    assert normalisation.target_frequency, "target_frequency function does not exist."
    
    #test case 
    chan = 'HHZ'
    freqmin   = 0.005
    freqmax   = 0.1
    
    #input type 
    assert type(chan) == str, "TypeError, the input channel should be a string."
    assert type(freqmin) == float or int, "TypeError, the input minimum frequency should be a float or int number."
    assert type(freqmax) == float or int, "TypeError, the input maximum frequency should be a float or int number."
    
    output1 = normalisation.target_frequency(chan, freqmin, freqmax)
    
    #output type 
    assert type(output1) == tuple, "TypeError, the output should be a tuple of min&max targeted filtering frequency range."
    
    #test if exception is raised
    #chan_except = 'NHZ'
    #with pytest.raises(NameError):
        #normalisation.target_frequency(chan_except, freqmin, freqmax)
    
    #test the accuracy of the output frequency range
    freqmin1 = 0.00150
    freqmax1 = 0.05
    output2 = normalisation.target_frequency(chan, freqmin1, freqmax1)
    assert output2 == (0.00167, 0.05), "ValueError, the function does not return the right frequency range. "
    
    
    
def test_target_frequency_window():
    '''This function tests
    
       1) the existence of the function
       2) the output types of the function
       3) the accuracy of the output
       4) if exception is raised successfully
       
       ASSERTION: 
       If 1) false: raise exception that the function does not exist.
       If 2) false: Type error: the outputs should be the corresponding types described in the error message. 
       If 3) false: the function does not return the correct result.
       If 4) false: the output should not be empty.
       
       Note: 
       The inputs of this function are the same as the inputs of target_frequency_range.
       Hence, test for target_frequency_range inputs also tests for the inputs here. 
    '''   
    
    #existence of function 
    assert normalisation.target_frequency_window, "target_frequency_window function does not exist."
    
    #The inputs of this function are the same as the inputs of target_frequency_range.
    #Hence, test for target_frequency_range inputs also tests for the inputs here. 
        
    #the output type of the function
    #test case 
    chan = 'HHZ'
    freqmin   = 0.00150
    freqmax   = 0.0020875
    
    output1 = normalisation.target_frequency_window(chan, freqmin, freqmax)
    assert type(output1) == list, "TypeError, the output should be a list of frequency windows."
    
    #test the accuracy of output
    assert output1 == [(0.00167, 0.0020875)], "ValueError, the output value is not correct."
    
    
    #test if exception is raised
    freqmin1 = 0.01
    freqmax1 = 0.01
    with pytest.raises(ValueError):
        normalisation.target_frequency_window(chan, freqmin1, freqmax1)
    
    
def test_butter_bandpass_filter():
    '''This function tests
    
       1) the existence of the function
       2) if the exception is raised for empty output 
       
       ASSERTION: 
       If 1) false: raise exception that the function does not exist.
       If 2) false: the function does not raise exception successfully.
       
       Note: 
       The butter bandpass_filter uses outputs from previous functions. To avoid triviality, this test function will not test the type of 
       inputs and outputs. But will test if the exception will be successfully raised for undesired output. 
       
       
    '''   
    
    #existence of function 
    assert normalisation.butter_bandpass_filter, "target_frequency_window function does not exist."
    
    #test case
    fs = 1
    highcut = 0.05
    lowcut = 0.01
    
    #test if exception is raised 
    data_except = []
    with pytest.raises(ValueError):
        normalisation.butter_bandpass_filter(data_except, fs, highcut, lowcut, order=2)

        
        
def test_normalisation_filtering():
    '''This function tests
    
       1) the existence of the function
       2) if the exception is raised for empty output 
       
       ASSERTION: 
       If 1) false: raise exception that the function does not exist.
       If 2) false: the function does not raise exception successfully.
       
       Note: 
       The butter normalisation_filtering uses outputs from previous functions. 
       To avoid triviality, this test function will not test the type of 
       inputs and outputs. But will test if the exception will be successfully raised for undesired output. 
       
       
    '''   
    #existence of function 
    assert normalisation.normalisation_filtering, "normalisation_filtering function does not exist."
    
    #test if exception will be raised
    target_frequency_window = [(0.01, 0.05)]
    samp_freq = 1
    ntr = []
    with pytest.raises(ValueError):
        normalisation.normalisation_filtering(target_frequency_window, samp_freq, ntr)
        

def test_normalisation ():
    '''This function tests
    
       1) the existence of the function
       2) if the exception is raised for empty output 
       
       ASSERTION: 
       If 1) false: raise exception that the function does not exist.
       If 2) false: the function does not raise exception successfully.
       
       Note: 
       The butter normalisation_filtering uses outputs from previous functions. 
       To avoid triviality, this test function will not test the type of 
       inputs and outputs. But will test if the exception will be successfully raised for undesired output.       
    '''   

    #existence of function 
    assert normalisation.freq_time_normalisation, "normalisation function does not exist."
    
    #test if exception will be raised
    target_frequency_window = [(0.01, 0.05)]
    samp_freq = 1
    ntr = []
    with pytest.raises(ValueError):
        normalisation.freq_time_normalisation(target_frequency_window, samp_freq, ntr)    
    

    



    
        
        
    
        