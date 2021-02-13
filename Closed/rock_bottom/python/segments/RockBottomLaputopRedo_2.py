#!/usr/bin/env python
import os
import sys, getopt
import glob
from os.path import expandvars
from sys import path
from I3Tray import *
from icecube.icetray import I3Units
from icecube import icetray, dataclasses, dataio, icepick, recclasses, frame_object_diff
from icecube import rock_bottom, toprec, CascadeVariables
from icecube import gulliver, gulliver_modules, lilliput, tableio
from icecube.icetray.i3logging import log_debug,log_fatal
from icecube.icetop_Level3_scripts.modules import CheckContainment, MaxSignalCuts
from icecube.rock_bottom.modules import *
import math
import numpy as np
from icecube.tableio import I3TableWriter
from icecube.rootwriter import I3ROOTTableService
from icecube.icetop_Level3_scripts import icetop_globals

Year = sys.argv[1]
Run = sys.argv[2]

detector = 'IC79'
name = "Laputop1"

emily_work = "/data/user/edvorak/RecoTesting/"
INDIR="/data/ana/CosmicRay/IceTop_level3/sim/"+detector+"/"
infiles = glob.glob(INDIR+Year+'/Level3_'+detector+'_'+Year+'_Run0'+Run+'*.i3.gz')
gcdfile = glob.glob(INDIR+"GCD/Level3_"+Year+"_GCD.i3.gz")
infiles.insert(0, gcdfile[0])
print infiles

NameMe = "LaputopRepeat"
#OUTFILE = emily_work+"testfiles/"+NameMe+"_"+Year+"_Run0"+Run+"_"+NameMe+".i3.gz"
OUTFILE = emily_work+"testfiles/"+NameMe+"_"+Year+"_Run0"+Run+"_"+NameMe+".i3.gz"
HLCPulses=icetop_globals.icetop_HLCseed_clean_hlc_pulses
ExcludedHLCTanks='ClusterCleaningExcludedStations'

#icetray.I3Logger.global_logger = icetray.I3PrintfLogger()
#icetray.set_log_level(icetray.I3LogLevel.LOG_DEBUG)
#icetray.set_log_level_for_unit('Laputop', icetray.I3LogLevel.LOG_TRACE)

tray = I3Tray()
#**************************************************
#                 Reader and whatnot
#**************************************************
tray.AddModule("I3Reader","reader")(
	("FileNameList", infiles))

## Re-inflate the GCD from the diff's
from icecube.frame_object_diff.segments import uncompress
tray.AddSegment(uncompress, "uncompressme")

loglog = rock_bottom.ldf.LogLog()
nkg = rock_bottom.ldf.NKG()

#laputop_ltp = rock_bottom.functions.ERF(x_0=math.log10(0.1657), sigma=0.35, s=0.5)
laputop_ltp = rock_bottom.functions.I3LaputopTriggerProbability()

tray.AddService("I3SimpleSnowCorrectionServiceFactory", "SimpleSnow",
	Lambda= 2.1
	)

tray.AddService('I3GulliverMinuitFactory', 'Minuit',
	MinuitPrintLevel = -2,
	FlatnessCheck = True,
	Algorithm = 'SIMPLEX',
	MaxIterations = 2500,
	MinuitStrategy = 2,
	Tolerance = 0.01
	)

## Load signal model from laputop that requires the same calculations for the LDF LLH
tray.AddService('LaputopSignalModel', 'LaputopSignalModel',
	LDF=loglog,
	LTP=laputop_ltp,
	SnowService = "SimpleSnow"
	)

tray.AddService('GaussCurveModel', 'GaussCurveModel',
                        CRV=loglog,
                        use_top_sigma = True,
                        SnowService = "SimpleSnow")


## rock_bottom seed for step 1 
tray.AddModule(WriteSeed, 'write_seed',
	ShowerCOG = 'ShowerCOG',
	ShowerPlane = 'ShowerPlane',
	OutputName = 'SimpleSeed'
	)

## Laputop seed for step 1 
tray.AddService("I3LaputopSeedServiceFactory", name+"ToprecSeed",
	InCore = 'ShowerCOG',
	InPlane = 'ShowerPlane',
	Beta = 2.6,                  # first guess for Beta
	InputPulses = HLCPulses
	)

## Here are the three parameter modules for repeating laputop with rock_bottom (in order)
tray.AddService("I3ComboParametrizationFactory","simpar_L1_L")(
	( "StepX", 10.*I3Units.m ),
	( "StepY", 10.*I3Units.m ),
	( "RelativeBoundsX", [-200.0*I3Units.m,+200.0*I3Units.m] ),
	( "RelativeBoundsY", [-200.0*I3Units.m,+200.0*I3Units.m] ),
	( "StepLog10_S125", 1. ),
	( "BoundsLog10_S125", [-3. ,8.] ),
	( "StepBeta",  0.6),
	( "BoundsBeta", [2.9 , 3.1] )
	)

tray.AddService("I3ComboParametrizationFactory","simpar_L2_L")(
	( "StepT", 50.0*I3Units.ns ),
	( "StepX", 2.0*I3Units.m ),
	( "StepY", 2.0*I3Units.m ),
	( "RelativeBoundsX", [-15.0*I3Units.m,+15.0*I3Units.m] ),
	( "RelativeBoundsY", [-15.0*I3Units.m,+15.0*I3Units.m] ),
	("StepNX", 0.5),
	("StepNY", 0.5),
	( "RelativeBoundsNX", [-1.0,+1.0] ),
	( "RelativeBoundsNY", [-1.0,+1.0] ),
	( "StepLog10_S125", 0.045 ),
	( "BoundsLog10_S125", [-3. ,8.] ),
	( "StepBeta", 0.15 ),
	( "BoundsBeta", [2. ,4.] ),
	)

tray.AddService("I3ComboParametrizationFactory","simpar_L3_L")(
	( "StepX", 1.0*I3Units.m ),
	( "StepY", 1.0*I3Units.m ),
	( "RelativeBoundsX", [-45.0*I3Units.m,+45.0*I3Units.m] ),
	( "RelativeBoundsY", [-45.0*I3Units.m,+45.0*I3Units.m] ),
	( "StepLog10_S125", 0.045 ),
	( "BoundsLog10_S125", [-3. ,8.] ),
	( "StepBeta", 0.15 ),
	( "BoundsBeta", [0. ,10.] ),
	#( "StepT", 50.0*I3Units.ns ),
	#("StepNX", 0.5),
	#("StepNY", 0.5),
	( "StepT", 10.0*I3Units.ns ),
	("StepNX", 0.1),
	("StepNY", 0.1),
	( "RelativeBoundsNX", [-1.0,+1.0] ),
	( "RelativeBoundsNY", [-1.0,+1.0] ),
	)

## Here are the three parameter modules for laputop (in order)
tray.AddService("I3LaputopParametrizationServiceFactory", name+"ToprecParam1",
	FixCore = False,
	FixTrackDir = True,
	IsBeta = True,
	MinBeta = 2.9,   ## From toprec... 2nd iteration (DLP, using beta)
	MaxBeta = 3.1,
	maxLogS125 =8.0,        # Default is 6., be a bit safer, although should never happen to be this large
	VertexStepsize =10.0,   # The COG is very good for contained events, don't step too far
	LimitCoreBoxSize = 200.0
	)

tray.AddService("I3LaputopParametrizationServiceFactory", name+"ToprecParam2",
	FixCore = False,
	FixTrackDir = False,      # FREE THE DIRECTION!
	IsBeta = True,
	MinBeta = 2.0,   ## From toprec... 3rd iteration (DLP, using beta)
	MaxBeta = 4.0,
	LimitCoreBoxSize = 15.0,
	maxLogS125 =8.0,
	## Use these smaller stepsizes instead of the defaults:
	VertexStepsize =2.0,      # default is 20
	SStepsize = 0.045,        # default is 1
	BetaStepsize =0.15
	)

tray.AddService("I3LaputopParametrizationServiceFactory", name+"ToprecParam3",
	FixCore = False,
	FixTrackDir = True,
	IsBeta = True,
	MinBeta = 0.0,
	MaxBeta = 10.0,
	LimitCoreBoxSize = 45.0,
	maxLogS125 =8.0,
	## Use these smaller stepsizes instead of the defaults:
	VertexStepsize = 1.0,     # default is 20
	SStepsize = 0.045,        # default is 1
	BetaStepsize =0.15        # default is 0.6
	)

## Curvature Likelihood for repeating Laputop steps 2 and 3 but with rock_bottom
tray.AddService('I3CurveLikelihoodFactory', 'TopLikelihood_C',
	Model='GaussCurveModel',
	HLCPulses=HLCPulses,
	SaturatedPulses='',
	IgnoreTanks=ExcludedHLCTanks,
	Toprec = True,
	MinSignal =0.1
	)

## LDF Likelihood for repeating all 3 Laputopsteps but with rock_bottom
tray.AddService('I3TopLDFLikelihoodFactory', 'TopLikelihood_L',
	Model='LaputopSignalModel',
	HLCPulses=HLCPulses,
	SaturatedPulses='',
	Toprec = True,
	IgnoreTanks=ExcludedHLCTanks,
	MinSignal =0.1
	)

## Likelihood for repeating Laputop steps 2 and 3 but with rock_bottom
tray.AddService("I3EventLogLikelihoodCombinerFactory","dummy_LC",
	InputLogLikelihoods = ["TopLikelihood_L","TopLikelihood_C"],
	Multiplicity = 'Sum',
	RelativeWeights = [1.,1.]
	)

## Here are the three likelihood modules for laputop (in order)
tray.AddService("I3LaputopLikelihoodServiceFactory", name+"ToprecLike1",
	DataReadout = HLCPulses,
	BadTanks = ExcludedHLCTanks,
	DynamicCoreTreatment = 5.0,     # do the 5-meter core cut (used 11m before, but TF 5m and didn't see a big difference in the plots)
	SaturationLikelihood = True,
	MaxIntraStationTimeDiff =80.0,    # Don't use time fluctuating tanks for timing fits, could really mess up the hard work
	curvature ="",      # NO timing likelihood (at first; this will be overridden)
	SnowServiceName ="SimpleSnow",
	ldf = "dlp"
	)

tray.AddService("I3LaputopLikelihoodServiceFactory", name+"ToprecLike2",
	DataReadout = HLCPulses,
	BadTanks = ExcludedHLCTanks,
	DynamicCoreTreatment = 5.0,     # do the 5-meter core cut (used 11m before, but TF 5m and didn't see a big difference in the plots)
	SaturationLikelihood = True,
	MaxIntraStationTimeDiff =80.0,    # Don't use time fluctuating tanks for timing fits, could really mess up the hard work
	curvature ="gausspar",      # NO timing likelihood (at first; this will be overridden)
	SnowServiceName ="SimpleSnow",
	ldf = "dlp"
	)

tray.AddService("I3LaputopLikelihoodServiceFactory", name+"ToprecLike3",
	DataReadout = HLCPulses,
	BadTanks = ExcludedHLCTanks,
	DynamicCoreTreatment = 5.0,     # do the 5-meter core cut (used 11m before, but TF 5m and didn't see a big difference in the plots)
	SaturationLikelihood = True,
	MaxIntraStationTimeDiff =80.0,    # Don't use time fluctuating tanks for timing fits, could really mess up the hard work
	curvature ="gausspar",      # NO timing likelihood (at first; this will be overridden)
	SnowServiceName ="SimpleSnow",
	ldf = "dlp"
	)

## This module seeds step 1 of Laputop but with rock_bottom
tray.AddService("I3ComboSeedServiceFactory", "IT_Seeder_L",
	FirstGuesses=['SimpleSeed'],
	HLCPulses = HLCPulses,
	SignalModel='LaputopSignalModel',
	Beta = 2.6,
	Toprec = True,
	TimeShiftType="TFirst"
	)

## This module performs step 1 of Laputop but with rock_bottom
tray.AddModule("I3SimpleFitter", "IT_L_l1_L",
	SeedService = "IT_Seeder_L",
	Parametrization = "simpar_L1_L",
	LogLikelihood = "TopLikelihood_L",
	OutputName = "IT_L_l1_L",
	Minimizer ="Minuit"
	)

## This module seeds step 2 of Laputop but with rock_bottom
tray.AddService("I3ComboSeedServiceFactory", "IT_Seeder_L2",
	FirstGuesses=['IT_L_l1_L'],
	HLCPulses = HLCPulses,
	SignalModel='LaputopSignalModel',
	Toprec = False,
	InputReadout = HLCPulses,
	TimeShiftType="TFirst"
	)

## This module performs step 2 of Laputop but with rock_bottom
tray.AddModule("I3SimpleFitter", "IT_L_l2_L",
	SeedService = "IT_Seeder_L2",
	Parametrization = "simpar_L2_L",
	LogLikelihood = "dummy_LC",
	OutputName = "IT_L_l2_L",
	Minimizer ="Minuit"
	)

## This module seeds step 3 of Laputop but with rock_bottom
tray.AddService("I3ComboSeedServiceFactory", "IT_Seeder_L3",
	FirstGuesses=['IT_L_l2_L'],
	HLCPulses = HLCPulses,
	SignalModel='LaputopSignalModel',
	Toprec = False,
	InputReadout = HLCPulses,
	TimeShiftType="TFirst"
	)

## This module performs step 3 of Laputop but with rock_bottom
tray.AddModule("I3SimpleFitter", "IT_L_l3_L",
	SeedService = "IT_Seeder_L3",
	Parametrization = "simpar_L3_L",
	LogLikelihood = "dummy_LC",
	#LogLikelihood = "TopLikelihood_L",
	OutputName = "IT_L_l3_L",
	Minimizer ="Minuit"
	)

## This module performs all 3 Laputop steps
tray.AddModule("I3LaputopFitter", name,
	SeedService = name+"ToprecSeed",
	Parametrizations = [name+"ToprecParam%d"%i for i in range(1,4)],   # the three parametrizations
	LogLikelihoodServices = [name+"ToprecLike%d"%i for i in range(1,4)],     # the three likelihoods
	StoragePolicy ="OnlyBestFit",
	Minimizer ="Minuit"
	)

## ----- OUTPUT ------
tray.AddModule("I3Writer",'writer')(
	("filename", OUTFILE)#,
	)

#tray.Execute(5)
tray.Execute()

