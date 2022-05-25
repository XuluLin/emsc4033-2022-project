# EMSC4033 project plan template

## Implementing frequency-time normalisation for ambient noise cross-correlation

## Executive summary

In one to two sentences, explain the background, the broad goals of the project and what the specific outcomes will be.

- Normalisation is a key step to satisfy the condition of a diffuse wavefield in order to extract Green's function in ambient noise tomography. Shen et al. (2012) proposed an improved method to do such -- frequency-time normalisation. This proposed method is claimed to have a better signal-to-noise ratio in the cross-correlation function, which will be highly regarded in long-period ambient noise cross-correlation. However, the code of this method is not publicly available. The goal of this project is to develop the code in python and implement it for ambient noise cross-correlation. 



## Goals and Timeline 

- frequency-time normalisation: 

    - **Goal 1**: read through the theory and research the documentation or manual of possible Python libraries needed (e.g. Hilbert transofrm in Scipy). 
    
    *Timeline: completed by 21/05*
    
    - **Goal 2**: write up the normalisation code for one 24-hr windowed raw seismic signal from the vertical component of a single station. This will include   preprocessing of data (demean, detrend, removing earthquake signals if any, check for gaps). 
    
    *Timeline: completed by 24/05*
    
    - **Goal 3**: modify and implement the normalisation code for a longer time (try downloading 1-month of data) for the vertical component of a single station. Not sure if downloading and computation time will be a problem. Adjust the length of period accordingly. 
    
    *Timeline: completed by 27/05*

    - **Goal 3**: Modify and implement the normalisation code for a few more stations for their veritcal-component raw signals for the suitable length of time worked out from Goal 3 and compute cross correlation functions. Adjust the number of stations according to computational time. 

    *TimeLine: completed by 29/05*
   
    - **Goal 4**: Write tests for frquency-time normalisation. They may include testing the exsistence of intermediate products, testing the type of input parameters and outputs, testing the values of intermediate and final products. 
    
    *Timeline: completed by 31/05*
    
    
## Background and Innovation  

Ambient noise cross-correlation is an imaging technique that uses the ambient noise wavefield of the Earth (i.e. noise generated from non-earthquake sources such as ocean tides, traffic, human activities etc.) to sample the shallow part of the Earth. This is achieved under the assumption that the ambient noise wavefield of the Earth is contributed by each source equally (i.e. the wavefield is diffuse). This is rarely the case in practice, therefore, we need to normalise the raw signal so that each frequency-dependent content is comparable within a pre-defined range to satisfy this assumption. 

One-bit and running-mean-average normalisations have been widely used to pre-process the ambient noise raw data. One-bit normalisation is the most aggressive normalisation by only retaining the sign of the raw waveform (i.e. positive signals are all normalised to 1 and negative signals are all normalised to -1). Running-mean-average normalisation is more sophisticated than one-bit. It weights each windowed raw signal at the centre by the inverse of the average absolute value of this central signal, and the window will slide past the whole waveform which will be summed up to a complete normalised series. These conventional methods have been proven to extract cross-correlation for shorter period range. However, Shen et al. (2012)'s frequency-time normalisation has claimed to boost the signal-to-noise ratio of the cross-correlation function as well as to reach a targeted period range of more than 100s. The concept behind frequency-time normalisation is using Hilbert transform for each frequency-windowed raw signal, from which the envelope function is computed. The corresponding frequency-windowed raw signal is normalised by the inverse of the envelope in time domian, then each window is summed up to produce a final frequency-time normalised series. 


The innovation of this projects comes from the issues embedded in this paper. 1) They did not make the source code publicly available. 2) they did a test between stations in north-eastern China and the Tibetan plateau (sampling continental lithosphere). I want to code it and test it on Zealanida which is a submerged continent including noise souced from oceanic environement. This will help my own research on Zealandia because I am using ambient noise cross-correlation at long period range. So far, the conventional methods do give promising signals but how to do better quality control is potentially what frequency-time normalisation can help. 

## Resources 

The resources available for this project are two-folds: 

- The theory of requency-time normalisation. Shen et al. (2012)'s paper provide details on the mathematics of this method, which is everything needed for its implementation. 

- The NoisePy package (https://github.com/mdenolle/NoisePy). This is a package I used in my Honours project which covers the whole process of ambient noise cross-correlation. There are functions available to do pre-processing and cross-correlation. I can take advantage of those for implementing frequency-time normalisation. 

## Testing, validation, documentation



