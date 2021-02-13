#!/usr/bin/env python

import matplotlib as mpl
mpl.use("Agg")
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy import optimize
import sys
import logging
import glob, os
from optparse import OptionParser
from os.path import expandvars

import math


def SrefConvert(Sref,gamma,epsi):
	Eo = (Sref-gamma)/epsi
	return Eo

def SrefConvertErr(typer,Sref,gamma,epsi,gammaErr,epsiErr):
	Err = ((epsi**-2.)*(gammaErr**2.))+(((()**2.)/(epsi**4.))*(epsiErr**2.))
	return np.sqrt(Err)









def open_angle(LZ,LA,MZ,MA):
    laputop_x     = np.sin(LZ)*np.cos(LA)
    laputop_y     = np.sin(LZ)*np.sin(LA)
    laputop_z     = np.cos(LZ)
    primary_x     = np.sin(MZ)*np.cos(MA)
    primary_y     = np.sin(MZ)*np.sin(MA)
    primary_z     = np.cos(MZ)
    opening_angle =  np.degrees(np.arccos(laputop_x*primary_x + laputop_y*primary_y + laputop_z*primary_z))
    return opening_angle

def DistFromCore(LX,LY,MX,MY):
    return np.sqrt(((MX-LX)*(MX-LX))+((MY-LY)*(MY-LY)))

weighter = 2.7
LEstop = 8.
HEstop = 7.
def Weighting(logE,dataset,le_weighter,he_weighter):
	if (dataset == "7006") or (dataset == "7007") or (dataset == "7579") or (dataset == "7784"):
		weighN_le = 25000.
		weighN_he = 20000.
	if (dataset == "12360") or (dataset == "12362") or (dataset == "20143") or (dataset == "20144"):
		weighN_le = 30000.
		weighN_he = 12000.
	
	nev = 0.
	if logE < LEstop:
		nev +=1000.0
	if logE >= HEstop:
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
	eWeight = logE**(-1.*weighter)
	if dataset == le_weighter:
		the_weighter_all = eWeight*weighN_le*weigh
	elif dataset == he_weighter:
		the_weighter_all = eWeight*weighN_he*weigh
	return the_weighter_all

def Profiled(bins, binN, valuesBinned, calculation, weighters):
	full_calc = []
	full_weigh =[]
	for i in np.arange(0,binN-1,1):
		weights = []
		calc = []
	        for j in np.arange(0,len(calculation)-1,1):
			if bins[i]< valuesBinned[j] < bins[i+1]:
				calc.append(calculation[j])
				weights.append(weighters[j])
		full_calc.append(calc)
		full_weigh.append(weights)
	y_error = []
	y_value = []
	x_error = []
	x_value = []
	for k in np.arange(0,binN-1,1):
		if len(full_calc[k])>0:
			x_value.append((bins[k]+bins[k+1])/2.)
			x_error.append(((bins[k]+bins[k+1])/2.)-bins[k])
			average = np.average(full_calc[k], weights=full_weigh[k])
			y_value.append(average)
    			y_error.append(np.sqrt(np.average((full_calc[k]-average)**2, weights=full_weigh[k])))
	return x_value, x_error, y_value, y_error

def DataProfiled(bins, binN, valuesBinned, calculation):
	full_calc = []
	full_weigh =[]
	for i in np.arange(0,binN-1,1):
		weights = []
		calc = []
	        for j in np.arange(0,len(calculation)-1,1):
			if bins[i]<	valuesBinned[j] < bins[i+1]:
				calc.append(calculation[j])
				weights.append(1.)
		full_calc.append(calc)
		full_weigh.append(weights)
	y_error = []
	y_value = []
	x_error = []
	x_value = []
	for k in np.arange(0,binN-1,1):
		if len(full_calc[k])>0:
			x_value.append((bins[k]+bins[k+1])/2.)
			x_error.append(((bins[k]+bins[k+1])/2.)-bins[k])
			average = np.average(full_calc[k], weights=full_weigh[k])
			y_value.append(average)
    			y_error.append(np.sqrt(np.average((full_calc[k]-average)**2, weights=full_weigh[k])))
	return x_value, x_error, y_value, y_error














def Resolution(bins, binN, valuesBinned, calculation, weighters, y_bins):
	full_calc = []
	full_weigh =[]
	for i in np.arange(0,binN-1,1):
		weights = []
		calc = []
	        for j in np.arange(0,len(calculation)-1,1):
			if bins[i]<	valuesBinned[j] < bins[i+1]:
				calc.append(calculation[j])
				weights.append(weighters[j])
		full_calc.append(calc)
		full_weigh.append(weights)
	y_error = []
	y_value = []
	x_error = []
	x_value = []
	for k in np.arange(0,binN-1,1):
                hist0, hist1, crap = plt.hist(full_calc[k], y_bins,weights = full_weigh[k])
                frac=0
		goodi=0
                nx = np.cumsum(hist0)
                for i in np.arange(0,len(nx),1):
                        frac = nx[i]/sum(hist0)
                        if frac > 0.68:
                                goodi = i
                                break
                y_value.append(hist1[goodi])
                x_value.append((bins[k]+bins[k+1])/2.)
	return x_value, y_value


def FileListReturn(path):
	filelist = []
        with open(path) as f:
                for line in f:
                        lin = line.split("\n")
                        filelist.append(lin[0])
	return filelist


def Projection(x,y,zen,azi,z,direc):
	if direc == "up":
		dire = -1.
	if direc == "down":
		dire = 1.
	nx = np.sin(zen)*np.cos(azi) 
	ny = np.sin(zen)*np.sin(azi) 
	nz = np.cos(zen) 
	ratio = (nz)/(z+nz)#ratio = (1950.-MZz)/(0.-MZz)
	X = x + nx*dire*(1.-(1./ratio))
	Y = y + ny*dire*(1.-(1./ratio))
	return X, Y, z

def QualityCuts(f,qc_frame):
	passer = True
	inform = f[qc_frame]
	for info in inform:
		if info[1] == False:
			passer = False
	return passer

def SomeQualityCuts(f,qc_frame,excepts):
	passer = True
	inform = f[qc_frame]
	counter = 0
	for info in inform:
		if counter not in excepts:
			if info[1] == False:
				passer = False
		counter +=1
	return passer











def StochGrab(f,frame_object):
        depth = []
        depth.append(1000)
        depth.append(1500)
        depth.append(1600)
        depth.append(1700)
        depth.append(1800)
        depth.append(1900)
        depth.append(2000)
        depth.append(2100)
        depth.append(2200)
        depth.append(2300)
        depth.append(2400)
        depth.append(3000)
        eloss = []
        eloss.append(f[frame_object].eLoss_1000)
        eloss.append(f[frame_object].eLoss_1500)
        eloss.append(f[frame_object].eLoss_1600)
        eloss.append(f[frame_object].eLoss_1700)
        eloss.append(f[frame_object].eLoss_1800)
        eloss.append(f[frame_object].eLoss_1900)
        eloss.append(f[frame_object].eLoss_2000)
        eloss.append(f[frame_object].eLoss_2100)
        eloss.append(f[frame_object].eLoss_2200)
        eloss.append(f[frame_object].eLoss_2300)
        eloss.append(f[frame_object].eLoss_2400)
        eloss.append(f[frame_object].eLoss_3000)
        return depth, eloss

def muonBundleEnergyLossFull(slantDepth,eng,zenith,A):
        E0 = eng
        #E0 = np.pow(10**(par[0])*1.e6);   # seed in Log10(E0/PeV)
        k = 14.5    # 14.5
        g_mu = 1.757 # gamma_mu
        a = 0.237881    # a_ionisationLossConstant
        b = .00032852   # b_stochasticLossConstant
        eloss = []
        for i in slantDepth:
                E_min = a/b * (np.exp(b*i) -1.);

                #log_trace("The params for the calculation: k :%lf, a %lf b %lf A %lf E0 %lf g_mu %lf slantdepth %lf",k,a,b,A,E0,g_mu,slantDepth);
                eloss.append(np.exp(-b*i)*k*A/np.cos(zenith)*g_mu*((E0/A)**(g_mu-1.))* ( -((E0/A)**(-g_mu))*(a/g_mu - b/(1-g_mu)*E0/A) + ((E_min)**(-g_mu))* (a/g_mu - b/(1-g_mu)*E_min)))
        return eloss




def muonBundleEnergyLoss(slantDepth,eng,zenith,A):
        #eLoss = 0.;    
        E0 = eng
        #E0 = np.pow(10**(par[0])*1.e6);   # seed in Log10(E0/PeV)
        k = 14.5    # 14.5
        g_mu = 1.757 # gamma_mu
        a = 0.237881    # a_ionisationLossConstant
        b = .00032852   # b_stochasticLossConstant

        E_min = a/b * (np.exp(b*slantDepth) -1.);

        eLoss = np.exp(-b*slantDepth)*k*A/np.cos(zenith)*g_mu*((E0/A)**(g_mu-1.))* ( -((E0/A)**(-g_mu))*(a/g_mu - b/(1-g_mu)*E0/A) + ((E_min)**(-g_mu))* (a/g_mu - b/(1-g_mu)*E_min)) ;         #//minus sign corrected in first term!!
        return eLoss

def StrongNHEcounterCut(mill_x, mill_e, stoch_x, stoch_e, eng, zenith,A,deltaE):
        eloss_cut = []
        eloss = []
        depth = []
        count = 0
        #print mill_e
        for i in np.arange(0,len(mill_e),1):
                if mill_e[i] > (7.*muonBundleEnergyLoss(mill_x[i],eng,zenith,A)**0.9):
                        count +=1
                else:
                        eloss_cut.append(7.*muonBundleEnergyLoss(mill_x[i],eng,zenith,A)**0.9)
                        eloss.append(mill_e[i])
                        depth.append(mill_x[i])
        pop, pcov = optimize.curve_fit(muonBundleEnergyLoss, depth, eloss, bounds=[[0., zenith*0.999999,A*0.999999],[np.inf,zenith*1.0000001,A*1.0000001]])
        eloss_fit = muonBundleEnergyLossFull(depth,pop[0],zenith,A)
        return depth, eloss, eloss_fit, eloss_cut, count, pop[0]



def StandardNHEcounterCut(mill_x, mill_e, stoch_x, stoch_e, eng, zenith,A,deltaE):
        eloss_cut = []
        eloss = []
        depth = []
        count = 0
        for i in np.arange(0,len(mill_e),1):
                if mill_e[i] > (5.*muonBundleEnergyLoss(mill_x[i],eng,zenith,A)**0.8):
                        count +=1
                else:
                        eloss_cut.append(5.*muonBundleEnergyLoss(mill_x[i],eng,zenith,A)**0.8)
                        eloss.append(mill_e[i])
                        depth.append(mill_x[i])
        print depth, eloss, 0., zenith*0.999999,A*0.999999,np.inf,zenith*1.0000001,A*1.0000001
        pop, pcov = optimize.curve_fit(muonBundleEnergyLoss, depth, eloss, bounds=[[0., zenith*0.999999,A*0.999999],[np.inf,zenith*1.0000001,A*1.0000001]])
        eloss_fit = muonBundleEnergyLossFull(depth,pop[0],zenith,A)
        return depth, eloss, eloss_fit, eloss_cut, count, pop[0]




def NewNHEcounterCut(mill_x, mill_e, stoch_x, stoch_e, eng, zenith,A,deltaE):
        eloss_cut = []
        eloss = []
        depth = []
        depth2 = []
        count = 0
        #print mill_e
        for i in np.arange(0,len(mill_e),1):
		if mill_e[i] > (muonBundleEnergyLoss(mill_x[i],eng,zenith,A)+deltaE):
                        count +=1
			#eloss_cut.append(0.)#(muonBundleEnergyLoss(mill_x[i],eng,zenith,A)+deltaE))
                        eloss.append(0.)
                        depth2.append(mill_x[i])
                else:
			eloss_cut.append((muonBundleEnergyLoss(mill_x[i],eng,zenith,A)+deltaE))
                        eloss.append(mill_e[i])
                        depth.append(mill_x[i])
                        depth2.append(mill_x[i])
        pop, pcov = optimize.curve_fit(muonBundleEnergyLoss, depth2, eloss, bounds=[[0., zenith*0.999999,A*0.999999],[np.inf,zenith*1.0000001,A*1.0000001]])
        eloss_fit = muonBundleEnergyLossFull(depth,pop[0],zenith,A)
        return depth2, eloss, eloss_fit, eloss_cut, count, pop[0], depth




def effective_area(logEnergy=6.0,A=1,sigmoid=1):
    '''
    # from Tom Feusels. Sigmoid 1 is default. 
    if A == 1:
        if sigmoid ==1:
            p0=1.351 * 1e5
            p1=8.8
            p2=52
            p3=0
        elif sigmoid ==2:
            p0=1.3 * 1e5
            p1=9.0
            p2=53
            p3=700
    elif A == 56:
        if sigmoid ==1:
            p0=1.377 * 1e5
            p1=8.0
            p2=48.
            p3=0
        elif sigmoid ==2:
            p0=1.51 * 1e5
            p1=7.7
            p2=46
            p3=-1800
    A_eff = p0 / (1 + np.exp(-p1 * logEnergy + p2))
    '''
    
    # from Tom Feusels. Final
    if logEnergy <= 6.9: 
        A_eff = -2.91034e7 + 1.28627e7 * logEnergy -1.88283e6 * logEnergy**2 + 9.17134e4 * logEnergy**3
    else:
        A_eff = 1.17342e5 + 2.74995e3 * logEnergy 
        
    #eff_area_LE->SetParameters(-2.91034e7,1.28627e7,-1.88283e6,9.17134e4
    #eff_area_HE->SetParameters(1.17342e5,2.74995e3);
    return A_eff        
def durationEmily():
    dur0512b=1.363e+06  
    dur0612=2.502e+06 
    dur0712=2.527e+06
    dur0812=2.637e+06
    dur0912=2.493e+06
    dur1012=2.571e+06
    dur1112=2.244e+06
    dur1212=2.356e+06
    dur0113=2.368e+06
    dur0213=2.238e+06
    dur0313=2.452e+06 
    dur0413=2.392e+06
    dur2012 = dur0512b+dur0612+dur0712+dur0812+dur0912+dur1012+dur1112+dur1212+dur0113+dur0213+dur0313+dur0413
    return dur2012

def duration2010():
    dur0610=2.313e+06
    dur0710=2.472e+06
    dur0810=2.283e+06
    dur0910=2.513e+06
    dur1010=2.569e+06 
    dur1110=2.239e+06
    dur1210=2.432e+06 
    dur0111=2.070e+06
    dur0211=2.264e+06 
    dur0311=2.482e+06
    dur0411=2.169e+06
    dur0511a= 996000.
    dur2010 = dur0610+dur0710+dur0810+dur0910+dur1010+dur1110+dur1210+dur0111+dur0211+dur0311+dur0411+dur0511a
    return dur2010
def duration2011():
    dur0511b=1.493e+06
    dur0611=2.530e+06
    dur0711=2.531e+06
    dur0811=2.645e+06
    dur0911=2.520e+06
    dur1011=2.633e+06
    dur1111=2.426e+06
    dur1211=2.353e+06
    dur0112=2.207e+06 
    dur0212=2.198e+06 
    dur0312=2.506e+06
    dur0412=2.267e+06
    dur0512a=1.091e+06
    dur2011 = dur0511b+dur0611+dur0711+dur0811+dur0911+dur1011+dur1111+dur1211+dur0112+dur0212+dur0312+dur0412+dur0512a
    return dur2011
  
def duration2012():
    dur0512b=1.363e+06  
    dur0612=2.502e+06 
    dur0712=2.527e+06
    dur0812=2.637e+06
    dur0912=2.493e+06
    dur1012=2.571e+06
    dur1112=2.244e+06
    dur1212=2.356e+06
    dur0113=2.368e+06
    dur0213=2.238e+06
    dur0313=2.452e+06 
    dur0413=2.392e+06
    dur0513=1.181e+05
    dur2012 = dur0512b+dur0612+dur0712+dur0812+dur0912+dur1012+dur1112+dur1212+dur0113+dur0213+dur0313+dur0413+dur0513
    return dur2012
def duration2010to2012():
    dur2010to2012 = duration2010()+duration2011()+duration2012()
    return dur2010to2012
def duration2012():
    dur0512b=1.363e+06  
    dur0612=2.502e+06 
    dur0712=2.527e+06
    dur0812=2.637e+06
    dur0912=2.493e+06
    dur1012=2.571e+06
    dur1112=2.244e+06
    dur1212=2.356e+06
    dur0113=2.368e+06
    dur0213=2.238e+06
    dur0313=2.452e+06 
    dur0413=2.392e+06
    dur0513=1.181e+05
    dur2012 = dur0512b+dur0612+dur0712+dur0812+dur0912+dur1012+dur1112+dur1212+dur0113+dur0213+dur0313+dur0413+dur0513
    return dur2012

def ZFactorErr(data,dataE,proton,protonE,iron,ironE):

	sigma = []
	for i in np.arange(0,min(len(data),len(proton),len(iron)),1):
		if (proton[i] == 0) and (iron[i] == 0):
			sigma.append(10000.)
		else:
			A = ((dataE[i])**2.)*((1/(iron[i]-proton[i]))**2.)
			B = ((ironE[i])**2.)*(((proton[i]-data[i])/((iron[i]-proton[i])**2.))**2.)
			C = ((protonE[i])**2.)*(((data[i]-iron[i])/((iron[i]-proton[i])**2.))**2.)

			sigma.append(np.sqrt(A+B+C))
	return sigma


def SolidAngle(zen):
	solid_angle = np.pi*(np.sin(zen*np.pi/180.)*np.sin(zen*np.pi/180.))
	return solid_angle




#spectrum = 1./(livetime*solid_angle*effective_area) * nevents



