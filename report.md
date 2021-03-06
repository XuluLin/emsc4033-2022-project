
# Report: Implementation of Frequency-time Normalisation


## Background and objectives

Normalisation is a key step to satisfy the condition of a diffuse wavefield in order to extract Green's function in ambient noise tomography. Shen et al. (2012) proposed an improved method to do such -- frequency-time normalisation. Conceptually, this method decomposes the pre-processed waveform into different frequency window and computes the absolute value of the Hilbert transform (envelope) of the pre-processed waveform in each frequency window. The final result is returned after dividng the pre-processed waveform by its envelope function. Then all the normalised waveforms are summed to produce a finalised waveform. This proposed method is claimed to have a better signal-to-noise ratio in the cross-correlation function. However, the code of this method is not publicly available. 

The overall objective of this project is to implement frequency-time normalisation and make it available for public access. Python was chosen as the coding language because it is the most widely used, free scientifically programming language, and there are well-developed mathematical and signal processing packages available.

## Instructions 
README.md has detailed instructions about installation and functionality of this repository. The main notebook `FTN.ipynb` provides detailed guided instructions to define user's inputs and to use the modules. It is not intended as a tutorial, but the comments and docstrings are there to help newcomers to navigate through the procedure with ease. A brief outline of the workflow of this project is: download -> pre-process -> filter -> normalisation. 

## List of dependencies

The following is a list of Python packages that need to be pre-installed. 

If Python is installed via Anaconda, most of them will have been installed. Installation links or instructions will be provided after packages that the author needed to manually install. Different users may need to manually install different packages. Some packages will not be used for this normalisation method but will be good to have for ambient-noise cross correlation. 

- import os 
- import glob
- import copy
- import obspy (Python framework for processing seismological data: https://anaconda.org/conda-forge/obspy)
- import scipy
- import time
- import pycwt (wavelet spectral analysis: https://pycwt.readthedocs.io/en/latest/)
- import pyasdf (Adaptable Seismic Data Format:https://seismicdata.github.io/pyasdf/)
- import datetime
- import numpy as np
- import pandas as pd
- import sys
- from numba import jit
- from scipy.signal import hilbert
- from obspy.signal.util import _npts2nfft
- from obspy.signal.invsim import cosine_taper
- from scipy.fftpack import fft,ifft,next_fast_len
- from obspy.signal.filter import bandpass,lowpass
- from obspy.signal.regression import linear_regression
- from obspy.core.util.base import _get_function_from_entry_point
- from obspy.core.inventory import Inventory, Network, Station, Channel, Site
- from obspy.clients.fdsn import Client

## Testing 
As mentioned in ProjectPlanner.md, with practical needs, there are four tests in 'test_FTN.py': the existence of the function, the type of input and output, the accuracy of the output, and exception handling. 

- the existence of the function the type of input and output are tests for all function using `assert`. But to avoid triviality, for functions that have inputs from previous functions, or for function with inpputs being the outputs of previous functions, types of inputs and outputs are no longer tested. 

- tests for the accuracy of output(s) are implemented for functions that returns numerical results. This includes target_frequency and target_frequency_window in `nomalisation.py`. These two functions returns the targeted frequency range and the upper and lower bounds of each frequency window respectively. A simple test case with known output was passed through the functions. Although other functions that perform filtering and Hilbert transform in `normalisation.py` also output numerical results, it is hard to write test to check their accuracy because there are no simple test inputs with known output. 

- some functions include exceptions because of the workflow of this repository. Many functions are dependent on outputs of previous functions so notifying the user whether the output is empty or not is crucial for debugging. Hence, exceptions of empty lists/arrays are raised in modules where appropriate. In tests, these are tested using `pytest.raises(ErrorName)` with inputs that delibrately give empty outputs and ValueError is expected to be raised. If the exception is succesfully raised, the test will be passed and vice versa. 


## Limitations and future improvements 
The major limitation of this project lies in its generalisability. Ambient-noise cross correlation is an imaging technique that generally requires years of data from tens to hundreds of stations. The modules in this repository have been only tested on two to three stations and on hour-long data with consideration of computational time and processing capacity of local machines. Future work needs to be invested in testing the modules on more stations and longer duration, which will likely involve parallel computing on a remote server. Then modifying these scripts incorporating the use of MPI (https://mpi4py.readthedocs.io/en/stable/) is essential to implement on multiple processors. 

Another potential improvement lies in exception handling. Initially, the main script does not contain any exceptions; instead, I used exceptions in the testing script. After consulting with tutor, I realised that exceptions that are necessary for the user to know should be placed in the main script. There is `pytest.raise` available to test if the exception is raised successfully. After this improvement, the code is more logical and user-oriented. Future work can be further improving exception handling. Apart from just raisng ValueError for empty output, there might be exceptions that can be raised which help the user to debug logic error. For example, in pre-processing, can we test whether the waveform has been successfully detrended? Can an exception be raise to warn the user about the data quality at this stage? This involves understanding of the maths behind it which is out of the scope of the project, but the code will become more beginer friendly both from a coding and science perspective. 

Last but not least, Linux command-line is a standard environment for computation in seismology. However, the modules and notebooks in this repository are not yet accommodated for that. Future improvements can involve modifying the code to suit this environment. For example, the user-input parameter sections may be suitable to be put into the script. Then we need to guide the user to open the corresponding module script to change the parameters inside. 

