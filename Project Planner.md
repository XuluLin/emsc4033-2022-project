# EMSC4033 project plan template

## Implementing frequency-time normalisation for ambient noise cross-correlation

## Executive summary

In one to two sentences, explain the background, the broad goals of the project and what the specific outcomes will be.

- Normalisation is a key step to satisfy the condition of a diffuse wavefield in order to extract Green's function in ambient noise tomography. Shen et al. (2012) proposed an improved method to do such -- frequency-time normalisation. However, the code of this method is not available. The goal of this project is to develop the code in python and implement it for ambient noise cross-correlation. 


**Example:** _(this is based on the seismic monitoring dashboard that Louis showed). Seismic stations can be used to monitor human noise over the course of the day. Some seismometers stream data live to a server and so this processing can be done in near-real time. In this project I plan to build an online dashboard which processes the data once a day and uploads the results to github as 1) raw data, 2) an image that can be embedded in websites, 3) an updating csv table in github. I also plan to use the github "actions" engine to provide all the necessary processing power._

## Goals

- frequency-time normalisation: 

    - Goal 1: read through the theory and identify what packages are needed. 
    
    - Goal 2: write up the code and test it with the station pairs in the paper and with several of my catalogue in Zealandia. 

    - Goal 3: compare the results with the one produced by one-bit and running-mean-average normalisations. 
   
    - Goal 4: write tests for frquency-time normalisation


(Write things that you can assess whether they have been accomplished. For example, a goal like “improve visualisation of ocean output” is vague... But a goal that reads “implement functionality to plot streamlines of horizontal velocities in various slices from 3D ocean output” is specific enough.)


## Background and Innovation  

One-bit and running-mean-average normalisations have been widely used to pre-process the ambient noise raw data. Shen et al. (2012)'s frequency-time normalisation has claimed to boost the signal-to-noise ratio of the correlogram by a factor of 2. The issue with this is 1) they did not make the source code publicly available. 2) they did a test between stations in north-eastern China and the Tibetan plateau (sampling continental lithosphere). I want to code it and test it on Zealanida which is a submerged continent with noise souced from oceanic environement. 

## Resources & Timeline


## Testing, validation, documentation



