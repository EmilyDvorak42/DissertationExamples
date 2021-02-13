#!/usr/bin/env python
# from i3TOhdf.py
# This script was written to take IceCube specific files and convert their data into a HDF file readable with python 'pandas'.
# Each frame is an event that contains objects describing components of the event.
# The tray is  analogous to an icecube tray, with each event being a cube.
# Each module added to the tray calls different python or C++ programs that make a calculation and can add or remove information from the frame.

# python libraries
import os
import sys, getopt
import glob
from os.path import expandvars
from sys import path
import math
import numpy as np
import matplotlib
#matplotlib.use('agg')

# IceCube specific libraries
from I3Tray import *
from icecube.icetray import I3Units
from icecube import icetray, dataclasses, dataio, icepick, recclasses, frame_object_diff, rock_bottom
from icecube import phys_services, hdfwriter, tableio, stochastics, millipede, lilliput
from icecube import icetray, dataclasses, dataio, recclasses, simclasses, phys_services, rock_bottom, stochastics
from icecube.tableio import I3TableWriter
from icecube.hdfwriter import I3HDFWriter
from icecube.rock_bottom import converters 

# local libraries
import Tools
from Tools import *
import HDFtools
from HDFtools import *

emily = "/data/user/edvorak/"
emily_work = emily+"BestPlotters/"


Nfiles = 25000.
infiles_name = ["ic86_goodA_p_he"]

infiles = []
for i in np.arange(0,len(infiles_name),1):
        txtfilename = emily_work+"text/"+infiles_name[i]+".txt"
        with open(txtfilename) as f:
                for line in f:
                        lin = line.split("\n")
                        infiles.append(lin[0])

outfile = emily+"HDFfiles/"+infiles_name[0]+'.hdff'
print outfile


# Initiate Tray for Files to be Read or Written
tray = I3Tray()

# Read Each Tray of Data one at a time
tray.AddModule("I3Reader","reader")(
	("FileNameList", infiles))

# Apply functions defined above so all necessary values end up in the final HDF files
tray.AddModule(RecoSuccess,'oks')
tray.AddModule(Weighting27,'weigh')
tray.AddModule(Contained,'contain1')
tray.AddModule(NewStochG1,'contain2')
tray.AddModule(NewStochG2,'contain3')
tray.AddModule(G2Contain,'contain4')


# Write HDF file with all specific information
tray.AddSegment(I3HDFWriter,'writer1',
		output = outfile,
                SubEventStreams=['ice_top','in_ice','IceTopSplit','InIceSplit','fullevent','nullsplit'],
                keys = ['Laputop','LaputopParams','MCPrimary','IT_mpeLLH_itSEED','IT_mpeLLH_itSEEDParams','II_speLLH_mpeSEED','II_speLLH_mpeSEEDParams','IT73AnalysisIceTopQualityCuts','IT73AnalysisInIceQualityCuts','IT73AnalysisInIceQualityCuts_EM_good_ElossReco_IT_mpeLLH_itSEED','IT73AnalysisInIceQualityCuts_EM_good_ElossReco_II_speLLH_mpeSEED','good_ElossReco_IT_mpeLLH_itSEEDStoch_Reco2_EM','good_ElossReco_IT_mpeLLH_itSEEDStoch_Reco2_red','good_ElossReco_IT_mpeLLH_itSEEDStoch_Reco_red','good_ElossReco_IT_mpeLLH_itSEEDStoch_Reco_EM','good_ElossReco_II_speLLH_mpeSEEDStoch_Reco2_EM','good_ElossReco_II_speLLH_mpeSEEDStoch_Reco2_red','good_ElossReco_II_speLLH_mpeSEEDStoch_Reco_red','good_ElossReco_II_speLLH_mpeSEEDStoch_Reco_EM','Millipede','MillipedeFitParams','Millipede_dEdX','Stoch_Reco','Stoch_Reco2','CoincMuonReco_SPEFit2','CoincMuonReco_MPEFit','True_IT_Cont','True_II_Cont','Good_MPE','Good_SPE','Good_COMBO_IT','Good_COMBO_II','Good_Laputop','Weighting','G1newStoch','G2newStoch','G2diff'])

# Execute each tray at a time
tray.Execute()










