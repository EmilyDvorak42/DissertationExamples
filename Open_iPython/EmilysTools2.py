import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor,MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors.kde import KernelDensity
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import r2_score
from scipy.stats import pearsonr

from sklearn import datasets
from sklearn.model_selection  import GridSearchCV

import tables
import pylab as pl

import math

def ColumnCleaner(filer,key):
    framer1 = pd.read_hdf(filer,key)
    framer1 = framer1.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    cols1 = framer1.columns.tolist()
    framer1.columns = [key+'_%s' % cols1[i] for i in xrange(0, len(cols1[:]))]
    return framer1

def DataGrabber175(filer):
    finalframe = pd.DataFrame()
    it_noqc = pd.read_hdf(filer,'IT73AnalysisIceTopQualityCuts')
    it_noqc = it_noqc.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    ii_noqc = pd.read_hdf(filer,'IT73AnalysisInIceQualityCuts')
    ii_noqc = ii_noqc.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    ii_myqc_g1 = pd.read_hdf(filer,'IT73AnalysisInIceQualityCuts_EM_good_ElossReco_IT_mpeLLH_itSEED_175')
    ii_myqc_g2 = pd.read_hdf(filer,'IT73AnalysisInIceQualityCuts_EM_good_ElossReco_II_speLLH_mpeSEED_175')
    ii_myqc_g1 = ii_myqc_g1.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    ii_myqc_g2 = ii_myqc_g2.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    frame1 = ColumnCleaner(filer,'IT_mpeLLH_itSEED_175')
    frame2 = ColumnCleaner(filer,'IT_mpeLLH_itSEED_175Params')  
    frame3 = ColumnCleaner(filer,'II_speLLH_mpeSEED_175')
    frame4 = ColumnCleaner(filer,'II_speLLH_mpeSEED_175Params')
    frame5 = ColumnCleaner(filer,'Laputop')
    frame6 = ColumnCleaner(filer,'LaputopParams')
    frame8 = ColumnCleaner(filer,'CoincMuonReco_SPEFit2')
    frame9 = ColumnCleaner(filer,'CoincMuonReco_MPEFit')
    itc = ColumnCleaner(filer,'Laputop_IT_Cont')
    iic = ColumnCleaner(filer,'CoincMuonReco_MPEFit_II_Cont')
    frame10 = ColumnCleaner(filer,'Good_COMBO_IT')
    frame11 = ColumnCleaner(filer,'Good_COMBO_II')
    frame12 = ColumnCleaner(filer,'Good_Laputop')
    frame13 = ColumnCleaner(filer,'Good_MPE')
    frame14 = ColumnCleaner(filer,'Stoch_Reco')
    frame15 = ColumnCleaner(filer,'Stoch_Reco2')
    frame16 = ColumnCleaner(filer,'good_ElossReco_IT_mpeLLH_itSEED_175Stoch_Reco_EM')
    frame17 = ColumnCleaner(filer,'good_ElossReco_II_speLLH_mpeSEED_175Stoch_Reco_EM')
    frame18 = ColumnCleaner(filer,'good_ElossReco_IT_mpeLLH_itSEED_175Stoch_Reco2_EM')
    frame19 = ColumnCleaner(filer,'good_ElossReco_II_speLLH_mpeSEED_175Stoch_Reco2_EM')
    frame20 = ColumnCleaner(filer,'G1newStoch')
    frame21 = ColumnCleaner(filer,'G2newStoch')
    frame22 = ColumnCleaner(filer,'G2diff')
    framed = pd.concat([ii_myqc_g1,ii_myqc_g2,it_noqc,ii_noqc,frame1,frame2,frame3,frame4,frame5,frame6,frame8,frame9,itc,iic,frame10,frame11,frame12,frame13,frame14,frame15,frame16,frame17,frame18,frame19,frame20,frame21,frame22],axis=1)
    return framed


def DataGrabber(filer):
    finalframe = pd.DataFrame()
    it_noqc = pd.read_hdf(filer,'IT73AnalysisIceTopQualityCuts')
    it_noqc = it_noqc.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    ii_noqc = pd.read_hdf(filer,'IT73AnalysisInIceQualityCuts')
    ii_noqc = ii_noqc.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    ii_myqc_g1 = pd.read_hdf(filer,'IT73AnalysisInIceQualityCuts_EM_testing_ElossReco_IT_mpeLLH_itSEED')
    ii_myqc_g2 = pd.read_hdf(filer,'IT73AnalysisInIceQualityCuts_EM_testing_ElossReco_II_speLLH_mpeSEED')
    ii_myqc_g1 = ii_myqc_g1.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    ii_myqc_g2 = ii_myqc_g2.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    frame1 = ColumnCleaner(filer,'IT_mpeLLH_itSEED_2')
    frame2 = ColumnCleaner(filer,'IT_mpeLLH_itSEED_2Params')  
    frame3 = ColumnCleaner(filer,'II_speLLH_mpeSEED_2')
    frame4 = ColumnCleaner(filer,'II_speLLH_mpeSEED_2Params')
    frame5 = ColumnCleaner(filer,'Laputop')
    frame6 = ColumnCleaner(filer,'LaputopParams')
    frame8 = ColumnCleaner(filer,'CoincMuonReco_SPEFit2')
    frame9 = ColumnCleaner(filer,'CoincMuonReco_MPEFit')
    itc = ColumnCleaner(filer,'Laputop_IT_Cont')
    #iic = ColumnCleaner(filer,'CoincMuonReco_MPEFit_II_Cont')
    frame10 = ColumnCleaner(filer,'Good_COMBO_IT')
    frame11 = ColumnCleaner(filer,'Good_COMBO_II')
    frame12 = ColumnCleaner(filer,'Good_Laputop')
    frame13 = ColumnCleaner(filer,'Good_MPE')
    frame14 = ColumnCleaner(filer,'Stoch_Reco')
    frame15 = ColumnCleaner(filer,'Stoch_Reco2')
    frame16 = ColumnCleaner(filer,'testing_ElossReco_IT_mpeLLH_itSEEDStoch_Reco_EM')
    frame17 = ColumnCleaner(filer,'testing_ElossReco_II_speLLH_mpeSEEDStoch_Reco_EM')
    frame18 = ColumnCleaner(filer,'testing_ElossReco_IT_mpeLLH_itSEEDStoch_Reco2_EM')
    frame19 = ColumnCleaner(filer,'testing_ElossReco_II_speLLH_mpeSEEDStoch_Reco2_EM')
    frame20 = ColumnCleaner(filer,'G1newStoch')
    frame21 = ColumnCleaner(filer,'G2newStoch')
    frame22 = ColumnCleaner(filer,'G2diff')
    framed = pd.concat([ii_myqc_g1,ii_myqc_g2,it_noqc,ii_noqc,frame1,frame2,frame3,frame4,frame5,frame6,frame8,frame9,itc,frame10,frame11,frame12,frame13,frame14,frame15,frame16,frame17,frame18,frame19,frame20,frame21,frame22],axis=1)
    #framed = pd.concat([ii_myqc_g1,ii_myqc_g2,it_noqc,ii_noqc,frame1,frame2,frame3,frame4,frame5,frame6,frame8,frame9,itc,iic,frame10,frame11,frame12,frame13,frame14,frame15,frame16,frame17,frame18,frame19,frame20,frame21,frame22],axis=1)
    return framed


def AntiPassedDataG1Cuts(dataframe, cutlist,reco):
        key_check = []
        for key in dataframe.keys():
            if key in cutlist:
                    print key
                    dataframe =(dataframe.loc[(dataframe[key] ==0)])
        #dataframe =(dataframe.loc[(dataframe['CoincMuonReco_MPEFit_II_Cont_value'] <0.8)])
        #dataframe =(dataframe.loc[(dataframe['Laputop_IT_Cont_value'] <=0.9)])
        return dataframe 



def PassedDataG1Cuts(dataframe, cutlist,reco):
        key_check = []
        for key in dataframe.keys():
            if key in cutlist:
                    print key
                    dataframe =(dataframe.loc[(dataframe[key] !=0)])
        #dataframe =(dataframe.loc[(dataframe['CoincMuonReco_MPEFit_II_Cont_value'] <0.8)])
        #dataframe =(dataframe.loc[(dataframe['Laputop_IT_Cont_value'] <=0.9)])
        return dataframe 

def PassedDataG2Cuts(dataframe, cutlist,reco):
        key_check = []
        for key in dataframe.keys():
                if key in cutlist:
                    print key
                    dataframe =(dataframe.loc[(dataframe[key] !=0)])
        #dataframe =(dataframe.loc[(dataframe['Laputop_IT_Cont_value'] >0.9)])
        #dataframe =(dataframe.loc[(dataframe['CoincMuonReco_MPEFit_II_Cont_value'] <0.8)])
        return dataframe 

def Grabber175(filer):
    finalframe = pd.DataFrame()
    it_noqc = pd.read_hdf(filer,'IT73AnalysisIceTopQualityCuts')
    it_noqc = it_noqc.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    ii_noqc = pd.read_hdf(filer,'IT73AnalysisInIceQualityCuts')
    ii_noqc = ii_noqc.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    ii_myqc_g1 = pd.read_hdf(filer,'IT73AnalysisInIceQualityCuts_EM_good_ElossReco_IT_mpeLLH_itSEED_175')
    ii_myqc_g2 = pd.read_hdf(filer,'IT73AnalysisInIceQualityCuts_EM_good_ElossReco_II_speLLH_mpeSEED_175')
    ii_myqc_g1 = ii_myqc_g1.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    ii_myqc_g2 = ii_myqc_g2.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    frame1 = ColumnCleaner(filer,'IT_mpeLLH_itSEED_175')
    frame2 = ColumnCleaner(filer,'IT_mpeLLH_itSEED_175Params')  
    frame3 = ColumnCleaner(filer,'II_speLLH_mpeSEED_175')
    frame4 = ColumnCleaner(filer,'II_speLLH_mpeSEED_175Params')
    frame5 = ColumnCleaner(filer,'Laputop')
    frame6 = ColumnCleaner(filer,'LaputopParams')
    frame7 = ColumnCleaner(filer,'MCPrimary')
    frame8 = ColumnCleaner(filer,'CoincMuonReco_SPEFit2')
    frame9 = ColumnCleaner(filer,'CoincMuonReco_MPEFit')
    itc = ColumnCleaner(filer,'True_IT_Cont')
    iic = ColumnCleaner(filer,'True_II_Cont')
    frame10 = ColumnCleaner(filer,'Good_COMBO_IT')
    frame11 = ColumnCleaner(filer,'Good_COMBO_II')
    frame12 = ColumnCleaner(filer,'Good_Laputop')
    frame13 = ColumnCleaner(filer,'Good_MPE')
    frame14 = ColumnCleaner(filer,'Weighting')
    frame15 = ColumnCleaner(filer,'Stoch_Reco')
    frame16 = ColumnCleaner(filer,'good_ElossReco_IT_mpeLLH_itSEED_175Stoch_Reco_EM')
    frame17 = ColumnCleaner(filer,'good_ElossReco_II_speLLH_mpeSEED_175Stoch_Reco_EM')
    frame18 = ColumnCleaner(filer,'good_ElossReco_IT_mpeLLH_itSEED_175Stoch_Reco2_EM')
    frame19 = ColumnCleaner(filer,'good_ElossReco_II_speLLH_mpeSEED_175Stoch_Reco2_EM')
    frame20 = ColumnCleaner(filer,'Good_SPE')  
    frame21 = ColumnCleaner(filer,'Stoch_Reco2')
    frame22 = ColumnCleaner(filer,'G2diff')
    frame23 = ColumnCleaner(filer,'G1newStoch')
    frame24 = ColumnCleaner(filer,'G2newStoch')
    framed = pd.concat([ii_myqc_g1,ii_myqc_g2,it_noqc,ii_noqc,frame1,frame2,frame3,frame4,frame5,frame6,frame7,frame8,frame9,itc,iic,frame10,frame11,frame12,frame13,frame14,frame15,frame16,frame17,frame18,frame19,frame20,frame21,frame22,frame23,frame24],axis=1)
    return framed
def Grabber(filer):
    finalframe = pd.DataFrame()
    it_noqc = pd.read_hdf(filer,'IT73AnalysisIceTopQualityCuts')
    it_noqc = it_noqc.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    ii_noqc = pd.read_hdf(filer,'IT73AnalysisInIceQualityCuts')
    ii_noqc = ii_noqc.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    ii_myqc_g1 = pd.read_hdf(filer,'IT73AnalysisInIceQualityCuts_EM_good_ElossReco_IT_mpeLLH_itSEED')
    ii_myqc_g2 = pd.read_hdf(filer,'IT73AnalysisInIceQualityCuts_EM_good_ElossReco_II_speLLH_mpeSEED')
    ii_myqc_g1 = ii_myqc_g1.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    ii_myqc_g2 = ii_myqc_g2.drop(['Run','Event','SubEvent','SubEventStream','exists'], axis=1)
    frame1 = ColumnCleaner(filer,'IT_mpeLLH_itSEED')
    frame2 = ColumnCleaner(filer,'IT_mpeLLH_itSEEDParams')  
    frame3 = ColumnCleaner(filer,'II_speLLH_mpeSEED')
    frame4 = ColumnCleaner(filer,'II_speLLH_mpeSEEDParams')
    frame5 = ColumnCleaner(filer,'Laputop')
    frame6 = ColumnCleaner(filer,'LaputopParams')
    frame7 = ColumnCleaner(filer,'MCPrimary')
    frame8 = ColumnCleaner(filer,'CoincMuonReco_SPEFit2')
    frame9 = ColumnCleaner(filer,'CoincMuonReco_MPEFit')
    itc = ColumnCleaner(filer,'True_IT_Cont')
    iic = ColumnCleaner(filer,'True_II_Cont')
    frame10 = ColumnCleaner(filer,'Good_COMBO_IT')
    frame11 = ColumnCleaner(filer,'Good_COMBO_II')
    frame12 = ColumnCleaner(filer,'Good_Laputop')
    frame13 = ColumnCleaner(filer,'Good_MPE')
    frame14 = ColumnCleaner(filer,'Weighting')
    frame15 = ColumnCleaner(filer,'Stoch_Reco')
    frame16 = ColumnCleaner(filer,'good_ElossReco_IT_mpeLLH_itSEEDStoch_Reco_EM')
    frame17 = ColumnCleaner(filer,'good_ElossReco_II_speLLH_mpeSEEDStoch_Reco_EM')
    frame18 = ColumnCleaner(filer,'good_ElossReco_IT_mpeLLH_itSEEDStoch_Reco2_EM')
    frame19 = ColumnCleaner(filer,'good_ElossReco_II_speLLH_mpeSEEDStoch_Reco2_EM')
    frame20 = ColumnCleaner(filer,'Good_SPE')  
    frame21 = ColumnCleaner(filer,'Stoch_Reco2')
    frame22 = ColumnCleaner(filer,'G2diff')
    frame23 = ColumnCleaner(filer,'G1newStoch')
    frame24 = ColumnCleaner(filer,'G2newStoch')
    framed = pd.concat([ii_myqc_g1,ii_myqc_g2,it_noqc,ii_noqc,frame1,frame2,frame3,frame4,frame5,frame6,frame7,frame8,frame9,itc,iic,frame10,frame11,frame12,frame13,frame14,frame15,frame16,frame17,frame18,frame19,frame20,frame21,frame22,frame23,frame24],axis=1)
    return framed

def llh_check(dataframe, lister):
    dataframe =(dataframe.loc[(dataframe[lister]!= 0)])
    return dataframe
def anti_llh_check(dataframe, lister):
    dataframe =(dataframe.loc[(dataframe[lister]== 0)])
    return dataframe
def MakeArray(df,reco):
    array = []
    for i in df[reco]:
        array.append(i)
    return array

def MakeLogArray(df,reco):
    array = []
    for i in df[reco]:
        array.append(np.log10(i))
    return array

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

def PassedMyG1Cuts(dataframe, cutlist,reco):
        key_check = []
        for key in dataframe.keys():
            if key in cutlist:
                    dataframe =(dataframe.loc[(dataframe[key] !=0)])
        dataframe =(dataframe.loc[(dataframe['MCPrimary_energy'] >10**6.)])
        dataframe =(dataframe.loc[(dataframe['True_IT_Cont_value'] <=0.9)])
        dataframe =(dataframe.loc[(dataframe['True_II_Cont_value'] <0.8)])
        return dataframe 

def PassedMyG2Cuts(dataframe, cutlist,reco):
        key_check = []
        for key in dataframe.keys():
                if key in cutlist:
                    dataframe =(dataframe.loc[(dataframe[key] !=0)])
        dataframe =(dataframe.loc[(dataframe['MCPrimary_energy'] >10**6.)])
        dataframe =(dataframe.loc[(dataframe['True_IT_Cont_value'] >0.9)])
        dataframe =(dataframe.loc[(dataframe['True_II_Cont_value'] <0.8)])
        return dataframe 

def PassedG1Cuts(dataframe, cutlist,reco):
        key_check = []
        for key in dataframe.keys():
            if key in cutlist:
                    dataframe =(dataframe.loc[(dataframe[key] !=0)])
        dataframe =(dataframe.loc[(dataframe['MCPrimary_energy'] >10**6.)])
        #dataframe =(dataframe.loc[(dataframe['True_IT_Cont_value'] <=0.9)])
        dataframe =(dataframe.loc[(dataframe['True_II_Cont_value'] <0.8)])
        return dataframe 

def PassedG2Cuts(dataframe, cutlist,reco):
        key_check = []
        for key in dataframe.keys():
                if key in cutlist:
                    dataframe =(dataframe.loc[(dataframe[key] !=0)])
        dataframe =(dataframe.loc[(dataframe['MCPrimary_energy'] >10**6.)])
        #dataframe =(dataframe.loc[(dataframe['True_IT_Cont_value'] >0.9)])
        dataframe =(dataframe.loc[(dataframe['True_II_Cont_value'] <0.8)])
        return dataframe 

def Resolution(bins,Nbins,values4binning,calculation,weights):
    xvalue = []
    xerr = []
    yvalue = []
    yerr = []
    reso_bins=np.linspace(-2.,6.,200)
    for k in np.arange(0,Nbins-1,1):
        binned_calcs = []
        binned_weigh = []
        for j in np.arange(0,len(values4binning),1):
            if bins[k] < float(values4binning[j]) <= bins[k+1] :
                binned_calcs.append(float(calculation[j]))
                binned_weigh.append(float(weights[j]))
        hist0, hist1, crap = plt.hist(binned_calcs, reso_bins,weights = binned_weigh)
        frac=0
        goodi=0
        nx = np.cumsum(hist0)
        for i in np.arange(0,len(nx),1):
                        frac = nx[i]/sum(hist0)
                        if frac > 0.68:
                                goodi = i
                                break
        yvalue.append(hist1[goodi])
        xvalue.append((bins[k] + bins[k+1])/2.)
        xerr.append(((bins[k] + bins[k+1])/2.)- bins[k])
    return xvalue, xerr, yvalue

def Profiled(bins,Nbins,values4binning,calculation):
    xvalue = []
    xerr = []
    yvalue = []
    yerr = []
    for i in np.arange(0,Nbins-1,1):
        binned_calcs = []
        for j in np.arange(0,len(calculation),1):
            if bins[i] < float(values4binning[j]) < bins[i+1] :
                binned_calcs.append(float(calculation[j]))
        yvalue.append(np.mean(binned_calcs))
        yerr.append(np.std(binned_calcs))
        xvalue.append((bins[i] + bins[i+1])/2.)
        xerr.append(((bins[i] + bins[i+1])/2.)- bins[i])
    return xvalue, xerr, yvalue, yerr


def Projection(zen,azi,Xi,Yi):
    nx = np.sin(zen)*np.cos(azi)
    ny = np.sin(zen)*np.sin(azi)
    nz = np.cos(zen)
    ratio = (nz)/(1950.+nz)#ratio = (1950.-MZz)/(0.-MZz)
    Xf = Xi + nx*(1.-(1./ratio))
    Yf = Yi + ny*(1.-(1./ratio))
    return Xf, Yf



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
    #dur0513=1.181e+05
    dur2012 = dur0512b+dur0612+dur0712+dur0812+dur0912+dur1012+dur1112+dur1212+dur0113+dur0213+dur0313+dur0413#+dur0513
    return dur2012

def duration2010to2012():
    dur2010to2012 = duration2010()+duration2011()+duration2012()
    return dur2010to2012

def SolidAngle():
        solid_angle = np.pi*(np.sin(45.*np.pi/180.)*np.sin(45.*np.pi/180.))
        return solid_angle

def SolidAngle2():
        solid_angle = np.pi*(np.sin(65.*np.pi/180.)*np.sin(65.*np.pi/180.))
        return solid_angle
    

def SrefConvert(Sref,gamma,epsi):
        Eo = (Sref-gamma)/epsi
        return Eo

def SrefConvertErr(typer,Sref,gamma,epsi,gammaErr,epsiErr):
        Err = ((epsi**-2.)*(gammaErr**2.))+(((()**2.)/(epsi**4.))*(epsiErr**2.))
        return np.sqrt(Err)


