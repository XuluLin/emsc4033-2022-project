# EMSC4033 project plan template

## Project title

## Executive summary

In one to two sentences, explain the background, the broad goals of the project and what the specific outcomes will be.

- Option 1: I use the 'NoisePy' package in Python that automates high-performance computation of ambient noise cross-correlation and stacking in my Honours project. It contains three main source files and two modules to perform its functionalities. I plan to make a tutorial of this package targeted audience who want to know in-depth about how this package runs. 

- Option 2: I use the 'aftan-1.1' package in Fortran that automates the inversion of stacked correlograms into group and phase dispersion curves. It contains two main executable programs to perform its functionalities. I plan to make a tutorial of this package. 

**Example:** _(this is based on the seismic monitoring dashboard that Louis showed). Seismic stations can be used to monitor human noise over the course of the day. Some seismometers stream data live to a server and so this processing can be done in near-real time. In this project I plan to build an online dashboard which processes the data once a day and uploads the results to github as 1) raw data, 2) an image that can be embedded in websites, 3) an updating csv table in github. I also plan to use the github "actions" engine to provide all the necessary processing power._

## Goals

- Option 1: 
    -Goal 1: break down each source code into different sub-tasks and decode with examples
    -Goal 2: explain the function calls with examples(often called from the modules) 

- Option 2: 
    -Goal 1: explain each subrountine with examples
    - ...

(Write things that you can assess whether they have been accomplished. For example, a goal like “improve visualisation of ocean output” is vague... But a goal that reads “implement functionality to plot streamlines of horizontal velocities in various slices from 3D ocean output” is specific enough.)

## Questions
- Option 1: the package is written in python and I can easily write my tutorial in the same environment. 
    - Issue 1: In github (https://github.com/mdenolle/NoisePy), they have a short tutorial on how to install and use the package using command lines. However it 
               does not give details about how it actually runs (the theory and the logic behind the scene). From the user end, this is sufficient, but not for 
               those who wants to debug/improve or just to understand why the code does what it claims to do. My aim is to address this by writing a detailed
               tutorial. Does this fulfill the requirements of a project in this course?
 
- Option 2: 
     - Issue 1: I need to write the tutorial in Fortran. But I cannot run and show each line like in a python environment. What I am thinking about is to make a                     video tutorial with voice-over of what each command is doing. So that I can compile it on the spot and show what the output is. Is this Ok?

My preference is option 1 if it gets your approval because it is just simpler to do. However, option 2 will benefit my project and I learn a lot more in this. 
What is your suggestions and what is your thought on the issues? 


## Background and Innovation  

_Give more details on the scientific problem that you are working on and how this project will advance the discipline or help with your own research.
(Where applicable, describe how people have been achieving this goal up to now, talk about existing packages, their limitations, whether you can generalise something to help other people use your code)._

## Resources & Timeline

_What do you have at your disposal already that will help the project along. Did you convince somebody else to help you ? Are there already some packages you can build upon. What makes it possible to do this project in the time available. Do you intend to continue this project in the future ?_

(For example:
  - I’ll be using data of X from satellite and then also data from baby blue seals…
  - I’ll step on existing package Y and build extra functionality on top of class W.
  - I’ll use textbook Z that describes algorithms a, b, c
  - …
)

## Testing, validation, documentation

**Note:** You need to think about how you will know your code is correct and achieves the goals that are set out above (specific tests that can be implemented automatically using, for example, the `assert` statement in python.)  It can be really helpful if those tests are also part of the documentation so that when you tell people how to do something with the code, the example you give is specifically targetted by some test code.

_Provide some specific tests with values that you can imagine `assert`ing_

