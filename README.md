# DissertationExamples
Here lies a small sampling of the programs I would write for my dissertation.  There are four main directories, Open_iPython and Open_Python, Closed, and Files.  A short description of each is given below.

* Files:
Files needed or created by the programs in this repository.  These include text, hdf, Pickle and png files.

* Closed:
Programs that will not run outside of thee specific enviroment developed for the IceCube Experiment.  I have written a large portion of the code here and is an example of my data handling and use of multiple languages.

* Open_Python:
Feel free to download and run these yourself!  These are an example of some plots I made for my disseertation that can be compared with the results of a machinne learning test located in the Open_iPython directory.

* Open_iPython:
Feel free to download and run these yourself!  This is a set of scripts that are an example of my use of machine learning to estimate the cosmic ray flux.  There are 4 parts to this works

  * StepA:  Two part code where simulation or data is extracted from HDF files and all key information is stored in Pickle files
  * StepB:  Takes the simulation and trains the machine
  * StepC:  The trained regression model is then applied to the data to return estimate values of energy and mass.
  * StepD:  Plot everything 
