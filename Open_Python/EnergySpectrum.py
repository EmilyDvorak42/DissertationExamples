#!/usr/bin/env python

import matplotlib as mpl
mpl.use("Agg")
import numpy as np
import pylab
import matplotlib.pyplot as plt
import sys
import logging
import glob, os
from optparse import OptionParser
from os.path import expandvars
import math
from scipy import optimize
import Tools
from Tools import *

emily = "/Users/dork/Home/GitHub/Files/"
starter = 'fourth'
reco_object = "IT_mpeLLH_itSEED"
type_list = ['S125all_other','S125all']
type_lists = ['S125all_other','S125all']
#type_list = ['S125all','S125all_other']
#type_lists = ['S125all','S125all_other']
binN = 30

sim = str(sys.argv[1])
print sim
if sim == '125':
	fileset = 'ic86_goodA_'
if sim == '175':
	fileset = 'sim175'

g1_solid_angle = SolidAngle(40.)
g2_solid_angle = SolidAngle(65.)
livetime = durationEmily()


g2Eps = [1.018,1.062]
g2EpsErr = [0.041,0.04]
g2Gam = [-6.048,-6.365]
g2GamErr = [0.317,0.307]
g2newGamErr = np.sqrt(((g2GamErr[0]**2.)+(g2GamErr[1]**2.))/4.)
g2newEpsErr = np.sqrt(((g2EpsErr[0]**2.)+(g2EpsErr[1]**2.))/4.)
g2newEps = (g2Eps[1]+g2Eps[0])/2.
g2newGam = (g2Gam[1]+g2Gam[0])/2.

Eps = [0.927,1.021,0.965,1.086]
Gam = [-5.49,-6.135,-5.771,-6.602]

EpsErr = [0.034,0.006,0.047,0.007]
GamErr = [0.261,0.047,0.365,0.05]

oldEpsErr = np.sqrt(((EpsErr[0]**2.)+(EpsErr[2]**2.))/4.)
newEpsErr = np.sqrt(((EpsErr[1]**2.)+(EpsErr[3]**2.))/4.)
oldGamErr = np.sqrt(((GamErr[0]**2.)+(GamErr[2]**2.))/4.)
newGamErr = np.sqrt(((GamErr[1]**2.)+(GamErr[3]**2.))/4.)

newEps = (Eps[1]+Eps[3])/2.
newGam = (Gam[1]+Gam[3])/2.
oldEps = (Eps[0]+Eps[2])/2.
oldGam = (Gam[0]+Gam[2])/2.
"""
print newEps, newEpsErr, newGam, newGamErr
print Eest(2.,newEps,newGam)
print EestErr(2.,1.,newEps,newEpsErr,newGam,newGamErr)
print oldEps, oldEpsErr, oldGam, oldGamErr
print Eest(2.,oldEps,oldGam)
print EestErr(2.,1.,oldEps,oldEpsErr,oldGam,oldGamErr)

"""
AllEpsErr = np.sqrt(((newEpsErr**2.)+(g2newEpsErr**2.))/4.)
AllGamErr = np.sqrt(((newGamErr**2.)+(g2newGamErr**2.))/4.)
AllEps = (newEps+g2newEps)/2.
AllGam = (newGam+g2newGam)/2.
#print AllEps, AllEpsErr, AllGam, AllGamErr









for j in np.arange(0,len(type_lists),1):
	txtdirG1 = emily+starter+"_onData_10000_1000_G1_"+reco_object+"_2013_reco_True_noLOG_"+type_list[j]+".txt"
	txtdirG2 = emily+starter+"_onData_100_1000_G2_"+reco_object+"_2013_reco_True_noLOG_"+type_list[j]+".txt"
	txtdirAll = emily+starter+"_onData_100_1000_ALL_"+reco_object+"_2013_reco_True_noLOG_"+type_list[j]+".txt"

	pltdir = emily+starter+"_"+reco_object+"_2013_reco_True_noLOG_"+type_lists[j]
	filelist_name = [txtdirG1,txtdirG2,txtdirAll]
	G1t1oX = []
	G1r2oX = []
	G2t1oX = []
	G2r2oX = []
	ALLt1oX = []
	ALLr2oX = []

	txtfilename = filelist_name[0]
	with open(txtfilename) as f:
			for line in f:
					lin = line.split("\n")[0].split("\t")
					if lin[0] == "R02":	
					    if float(lin[1])>0:
						if j == 0:
							G1r2oX.append(SrefConvert(np.log10(float(lin[1])),newGam,newEps))
						if j == 1:
							G1r2oX.append(SrefConvert(float(lin[1]),newGam,newEps))
	txtfilename = filelist_name[1]
	with open(txtfilename) as f:
			for line in f:
					lin = line.split("\n")[0].split("\t")
					if lin[0] == "R02":	
					    if float(lin[1])>0:
						if j == 0:
							G2r2oX.append(SrefConvert(np.log10(float(lin[1])),g2newGam,g2newEps))
						if j == 1:
							G2r2oX.append(SrefConvert(float(lin[1]),g2newGam,g2newEps))
	txtfilename = filelist_name[2]
	with open(txtfilename) as f:
			for line in f:
					lin = line.split("\n")[0].split("\t")
					if lin[0] == "L01":	
					    if float(lin[1])>0:
						if j == 0:
							ALLt1oX.append(SrefConvert(np.log10(float(lin[1])),oldGam,oldEps))
						if j == 1:
							ALLt1oX.append(SrefConvert(float(lin[1]),oldGam,oldEps))
					if lin[0] == "R02":	
					    if float(lin[1])>0:
						if j == 0:
							ALLr2oX.append(SrefConvert(np.log10(float(lin[1])),AllGam,AllEps))
						if j == 1:
							ALLr2oX.append(SrefConvert(float(lin[1]),AllGam,AllEps))



	


	#bins = np.linspace(0,5,binN)
	eng_bins = np.linspace(5,10,binN)
	G1r2_ystep, G1r2_almost_xstep, crap = plt.hist(G1r2oX, eng_bins)
	G2r2_ystep, G2r2_almost_xstep, crap = plt.hist(G2r2oX, eng_bins)
	ALLt1_ystep, ALLt1_almost_xstep, crap = plt.hist(ALLt1oX, eng_bins)
	ALLr2_ystep, ALLr2_almost_xstep, crap = plt.hist(ALLr2oX, eng_bins)
	ALLt1_logE = []#len(ALLt1oX)
	ALLr2_logE = []#len(ALLr2oX)
	G1r2_logE = []#len(G1r2oX)
	G2r2_logE = []#len(G2r2oX)

	

	G2r2_spectrum = []
	G1r2_spectrum = []
	ALLr2_spectrum = []
	ALLt1_spectrum = []

	G1r2_xstep = []
	G2r2_xstep = []
	ALLt1_xstep = []
	ALLr2_xstep = []
	for i in np.arange(0,binN-1,1):
	        ALLt1_xstep.append(eng_bins[i])#(ALLt1_almost_xstep[i]+ALLt1_almost_xstep[i+1])/2.)
	        ALLr2_xstep.append(eng_bins[i])#(ALLt1_almost_xstep[i]+ALLt1_almost_xstep[i+1])/2.)
	        G1r2_xstep.append(eng_bins[i])#(ALLt1_almost_xstep[i]+ALLt1_almost_xstep[i+1])/2.)
	        G2r2_xstep.append(eng_bins[i])#(ALLt1_almost_xstep[i]+ALLt1_almost_xstep[i+1])/2.)


		ALLt1_effective_area =  effective_area(eng_bins[i]) 
		#ALLt1_effective_area =  effective_area(ALLt1_almost_xstep[i]) 
		#ALLt1_spectrum.append((ALLt1_ystep[i]/(livetime*solid_angle*ALLt1_effective_area*(10.**ALLt1_logE[i]))))
		#ALLt1_spectrum.append((ALLt1_ystep[i]/(livetime*solid_angle*ALLt1_effective_area))
		ALLt1_spectrum.append((ALLt1_ystep[i]/(livetime*g1_solid_angle*ALLt1_effective_area)))


		ALLr2_effective_area =  effective_area(eng_bins[i]) 
		#ALLt1_effective_area =  effective_area(ALLt1_almost_xstep[i]) 
		#ALLr2_spectrum.append((ALLr2_ystep[i]/(livetime*solid_angle*ALLr2_effective_area*(10.**ALLr2_logE[i]))))
		#ALLr2_spectrum.append((ALLr2_ystep[i]/(livetime*solid_angle*ALLr2_effective_area * aALLr2_nevents)))
		#ALLr2_spectrum.append((ALLr2_ystep[i]/(livetime*solid_angle*ALLr2_effective_area)))

		G1r2_effective_area =  effective_area(eng_bins[i]) 
		#G1r2_effective_area =  effective_area(G1r2_almost_xstep[i]) 
		#G1r2_spectrum.append((G1r2_ystep[i]/(livetime*solid_angle*G1r2_effective_area*(10.**G1r2_logE[i]))))
		#G1r2_spectrum.append((G1r2_ystep[i]/(livetime*solid_angle*G1r2_effective_area * aG1r2_nevents)))
		G1r2_spectrum.append((G1r2_ystep[i]/(livetime*g1_solid_angle*G1r2_effective_area)))

		G2r2_effective_area =  effective_area(eng_bins[i]) 
		#G2r2_effective_area =  effective_area(G2r2_almost_xstep[i]) 
		#G2r2_spectrum.append((G2r2_ystep[i]/(livetime*solid_angle*G2r2_effective_area*(10.**G2r2_logE[i]))))
		#G2r2_spectrum.append((G2r2_ystep[i]/(livetime*solid_angle*G2r2_effective_area * aG2r2_nevents)))
		G2r2_spectrum.append((G2r2_ystep[i]/(livetime*g2_solid_angle*G2r2_effective_area)))


	pylab.figure()
	plt.plot(ALLt1_xstep, ALLt1_spectrum,linewidth=1.5, drawstyle='steps',color = 'k')
	#plt.plot(ALLr2_xstep, ALLr2_spectrum,linewidth=1.5, drawstyle='steps',color = 'r')
	plt.plot(G1r2_xstep, G1r2_spectrum,linewidth=1.5, drawstyle='steps',color = 'g')
	plt.plot(G2r2_xstep, G2r2_spectrum,linewidth=1.5, drawstyle='steps',color = 'b')
	pylab.legend(["IT-II only","3D Group-I","3D Group-II"],loc=1)
	pylab.ylabel("Rate [1/s]")
	pylab.ylim([10**-10,5.*10**-8])
	pylab.xlim([6,10])
	pylab.yscale('log')
	pylab.ylabel(r"$\frac{dN}{dE} [1/sm^{2}sr GeV]$")
	pylab.xlabel(r"log$_{10}(E_{est}/[GeV]$)")
	plt.grid(True,which="both",ls="-")
	pylab.savefig(pltdir+"_final.png")
	pylab.close()







