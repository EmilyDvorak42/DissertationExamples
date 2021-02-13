#!/usr/bin/env python
# from i3TOhdf.py
# Tools specific for grabbing specific frame information to manipulate and write into the HDF file

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

import Tools
from Tools import *

Nfiles = 25000.
itconfig = phys_services.I3ScaleCalculator.IT81
icconfig = phys_services.I3ScaleCalculator.IC86


# Evaluate new count for event energy losses in ice for Group 1 events
def NewStochG1(frame):
	reco = "IT_mpeLLH_itSEED"
	mass_guess = 1
	deltaE = 500.
	meloss = []
	mdepth = []
	nhe_m = 0
	if reco in frame:
	   if "good_ElossReco_"+reco+"Millipede_dEdX_EM" in frame:
		RO2zen = frame[reco].dir.zenith
		for X in frame["good_ElossReco_"+reco+"Millipede_dEdX_EM"]:
			meloss.append(X.energy)
			mdepth.append(2000. - X.pos.z)
		mXbin, mstochloss = StochGrab(frame,"good_ElossReco_"+reco+"Stoch_Reco_EM")
		meloss_fit = muonBundleEnergyLossFull(mdepth,frame["good_ElossReco_"+reco+"Stoch_Reco_EM"].primEnergyEstimate,RO2zen,mass_guess)
		mdepth2, meloss2, meloss_fit2, meloss_cut2, m_nhe, Eguess, mdepth3 = NewNHEcounterCut(mdepth,meloss,mXbin, mstochloss,frame["good_ElossReco_"+reco+"Stoch_Reco_EM"].primEnergyEstimate,RO2zen,mass_guess,deltaE)
		nhe_m=m_nhe
		while m_nhe > 0:
			mdepth2, meloss2, meloss_fit2, meloss_cut2, m_nhe, Eguess, mdepth3 = NewNHEcounterCut(mdepth2,meloss2,mdepth2,meloss_fit2,Eguess,RO2zen,mass_guess,deltaE)
			nhe_m += m_nhe
	#return nhe_m
	frame['G1newStoch']=dataclasses.I3Double(nhe_m)
	
# Evaluate new count for event energy losses in ice for Group 2 events
def NewStochG2(frame):
	reco = "II_speLLH_mpeSEED"
	nhe_m = 0
	mass_guess = 1
	deltaE = 500.
	meloss = []
	mdepth = []
	if reco in frame:
	   if "good_ElossReco_"+reco+"Millipede_dEdX_EM" in frame:
		RO2zen = frame[reco].dir.zenith
		for X in frame["good_ElossReco_"+reco+"Millipede_dEdX_EM"]:
			meloss.append(X.energy)
			mdepth.append(2000. - X.pos.z)
		mXbin, mstochloss = StochGrab(frame,"good_ElossReco_"+reco+"Stoch_Reco_EM")
		meloss_fit = muonBundleEnergyLossFull(mdepth,frame["good_ElossReco_"+reco+"Stoch_Reco_EM"].primEnergyEstimate,RO2zen,mass_guess)
		mdepth2, meloss2, meloss_fit2, meloss_cut2, m_nhe, Eguess, mdepth3 = NewNHEcounterCut(mdepth,meloss,mXbin, mstochloss,frame["good_ElossReco_"+reco+"Stoch_Reco_EM"].primEnergyEstimate,RO2zen,mass_guess,deltaE)
		nhe_m=m_nhe
		while m_nhe > 0:
			mdepth2, meloss2, meloss_fit2, meloss_cut2, m_nhe, Eguess, mdepth3 = NewNHEcounterCut(mdepth2,meloss2,mdepth2,meloss_fit2,Eguess,RO2zen,mass_guess,deltaE)
			nhe_m += m_nhe
	#return nhe_m
	frame['G2newStoch']=dataclasses.I3Double(nhe_m)
	

#  Check to see whether the reconstructed event was containmennt parameters for Group 2
def G2Contain(frame):
	reco = "II_speLLH_mpeSEED"
	cii_type = "MPEFit"
	G2pass = 1000.
	if reco in frame:
		if (("CoincMuonReco_"+cii_type in frame) and (str( frame["CoincMuonReco_"+cii_type].fit_status)=='OK')):
				RO2 = frame[reco]
				RO2prms = frame[reco+"Params"]
				RO1 = frame["CoincMuonReco_"+cii_type]
				RO1Xf = RO1.pos.x
				RO1Yf = RO1.pos.y
				RO1Zf = RO1.pos.z
				RO1zen = RO1.dir.zenith
				RO1azi = RO1.dir.azimuth
				RO1Xi, RO1Yi,z = Projection(RO1Xf,RO1Yf,RO1zen,RO1azi,1950.,'up')
				G2pass = DistFromCore(RO1Xi,RO1Yi,RO2.pos.x,RO2.pos.y)
	#return G2pass
	frame['G2diff']=dataclasses.I3Double(G2pass)


#  Check to see whether the simulated event was contained within the detector
def Contained(frame):
	if "I3Geometry" in frame:
		geo = frame["I3Geometry"]
		calculator = phys_services.I3ScaleCalculator(geo, icconfig, itconfig)
		frame['True_IT_Cont']=dataclasses.I3Double(calculator.scale_icetop(frame["MCPrimary"]))
		frame['True_II_Cont']=dataclasses.I3Double(calculator.scale_inice(frame["MCPrimary"]))

# Check to eensure reconstructions are successsful
def RecoSuccess(frame):
	it_combo_count = 0
	ii_combo_count = 0
	it_count = 0
	ii_count = 0
	ii_counts = 0
	if (('IT_mpeLLH_itSEED' in frame) and ( int(frame['IT_mpeLLH_itSEED'].fit_status) == 0)):
		it_combo_count = 1
	if (('II_speLLH_mpeSEED' in frame) and ( int(frame['II_speLLH_mpeSEED'].fit_status) == 0)):
		ii_combo_count = 1
	if (('Laputop' in frame) and (int(frame['Laputop'].fit_status) == 0)):
		it_count = 1
	if (('CoincMuonReco_SPEFit2' in frame) and (int(frame['CoincMuonReco_SPEFit2'].fit_status) == 0)):
		ii_counts = 1
	if (('CoincMuonReco_MPEFit' in frame) and (int(frame['CoincMuonReco_MPEFit'].fit_status) == 0)):
		ii_count = 1
	frame['Good_COMBO_IT']= dataclasses.I3Double(it_combo_count)
	frame['Good_COMBO_II']= dataclasses.I3Double(ii_combo_count)
	frame['Good_Laputop']= dataclasses.I3Double(it_count)
	frame['Good_MPE']= dataclasses.I3Double(ii_count)
	frame['Good_SPE']= dataclasses.I3Double(ii_counts)


# Weight the stastics based on the prodced spectrum to reflect the true energy spectrum
def Weighting27(frame):
	logE = np.log10(frame["MCPrimary"].energy)                                        
	nev = 0
	if logE > 6.0:
		if logE < 8.0:
			nev +=1000.0
		if logE >= 7.0:
			nev += 480.0
		if logE >= 6.0:
			if logE < 7.0:
				rgen = 1100.0
		if logE >= 7.0:
			if logE < 8.0:
				rgen = 1700.0
		if logE >= 8.0:
			if logE < 9.0:
				rgen = 2600.0
		if logE >= 9.0:
			rgen = 2900.0
                                                                
		weigh = (1.0/nev)*rgen*rgen/1500.0/1500.0                                                
		eWeight = frame["MCPrimary"].energy**(-2.7)
	
		weighter_all = eWeight*Nfiles*weigh
		frame['Weighting']= dataclasses.I3Double(weighter_all)
	else:
		frame['Weighting']= dataclasses.I3Double(1.)















