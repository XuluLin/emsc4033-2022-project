# emsc4033-2022-project

# Implementation of frequency-time normalisation
Xulu Lin (u6989382)

## Introduction
This repository contains Python scripts for frequency-time normalisation (Shen et al., 2012). Frequency-time normalisation is an improved normalisation method for ambient-noise cross correlation. The paper provides a detailed explanation of the theory. However, the code is not made available publicly. The Python scripts in this repository are written for users that need comprehensive modules to implement frequency-time normalisation. 

## Installation
You will need Python to execute the modules. Follow this link to download Python https://www.python.org/downloads/. Note that it is written and tested in the 'Jupyter notebook' 6.3.0 interactive Web-based platform with ipython kernel. It is not written for command-line environment. You will also need multiple pre-installed Python packages. Please refer to `src/dependencies.py` for more details. 

## Functionality 
There are 4 modules (.py file) and a notebook (.ipynb file) for frequency-time normalisation, 1 testing module and 1 testing notebook. 

- import all the required pre-installed Python packages: `dependencies.py`.

- download and pre-processing: `download_raw_data.py` and `processing.py`. 

- frequency-time normalisation: `normalisation.py`. 

- main script to guide the user to define parameters and use these modules: `FTN.ipynb`. 

- tests: `test_FTN.py` and `run_test_FTN.ipynb`. 


## Reference 
Shen, Y., Ren, Y., Gao, H. and Savage, B. (2012). An Improved Method to Extract Very‐Broadband Empirical Green’s Functions from Ambient Seismic Noise. Bulletin of the Seismological Society of America, [online] 102(4), pp.1872–1877. doi:10.1785/0120120023.


