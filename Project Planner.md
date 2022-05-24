# EMSC4033 project plan template

## Implementing frequency-time normalisation for ambient noise cross-correlation

## Executive summary

In one to two sentences, explain the background, the broad goals of the project and what the specific outcomes will be.

- Normalisation is a key step to satisfy the condition of a diffuse wavefield in order to extract Green's function in ambient noise tomography. Shen et al. (2012) proposed an improved method to do such -- frequency-time normalisation. This proposed method is claimed to have a better signal-to-noise ratio in the cross-correlation function, which will be highly regarded in long-period ambient noise cross-correlation. However, the code of this method is not publicly available. The goal of this project is to develop the code in python and implement it for ambient noise cross-correlation. 



## Goals and Timeline 

- frequency-time normalisation: 

    - Goal 1: read through the theory and research the documentation or manual of possible Python libraries needed (e.g. Hilbert transofrm in Scipy). 
    *Timeline: completed by 22/05*
    
    - Goal 2: write up the code and test it with the station pairs in the paper and with several of my catalogue in Zealandia. 

    - Goal 3: compare the results with the one produced by one-bit and running-mean-average normalisations. 
   
    - Goal 4: write tests for frquency-time normalisation


(Write things that you can assess whether they have been accomplished. For example, a goal like “improve visualisation of ocean output” is vague... But a goal that reads “implement functionality to plot streamlines of horizontal velocities in various slices from 3D ocean output” is specific enough.)


## Background and Innovation  

One-bit and running-mean-average normalisations have been widely used to pre-process the ambient noise raw data. Shen et al. (2012)'s frequency-time normalisation has claimed to boost the signal-to-noise ratio of the correlogram by a factor of 2. The issue with this is 1) they did not make the source code publicly available. 2) they did a test between stations in north-eastern China and the Tibetan plateau (sampling continental lithosphere). I want to code it and test it on Zealanida which is a submerged continent with noise souced from oceanic environement. 

## Resources & Timeline


## Testing, validation, documentation



