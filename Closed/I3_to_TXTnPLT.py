#!/usr/bin/env python
# from SimPlotter4.py
import matplotlib as mpl
mpl.use("Agg")
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import sys
import logging
import glob, os
from optparse import OptionParser
from os.path import expandvars
from icecube import icetray, dataclasses, dataio, recclasses, simclasses, phys_services, rock_bottom, stochastics
from icecube.dataclasses import I3Double
from I3Tray import *
import math
from icecube.recclasses import I3LaputopParams, LaputopParameter
from icecube.dataclasses import I3FilterResultMap
Par = LaputopParameter # an enum, contains Parameter names
#from Tools import open_angle
from Tools import *
emily = "/data/user/edvorak/"
starter = "good_"
binN = 30
eng_bins = np.linspace(5.,9.5,binN)

other = sys.argv[1]		# "II" or "IT"
if other =='1':
	typer = "G1"
	cii_type = 'MPEFit'
	cutter = 0.
if other =='2':

	typer = "G2"
	cii_type = 'SPEFit2'

ii_typr = sys.argv[2]
if ii_typr == "True":
	apply_qcuts = True
	apply_qcuts_g2= True
if ii_typr == "False":
	apply_qcuts = False
	apply_qcuts_g2= False
mass_guess =16.
cutter = float(sys.argv[4])
deltaE = float(sys.argv[5])

if sys.argv[3] == "79p":
	itconfig = phys_services.I3ScaleCalculator.IT73
	icconfig = phys_services.I3ScaleCalculator.IC79
	filelist_name = ["ic79_goodA_p"]
	le_weighter = "7006"
	he_weighter = "7579"
	weighN_le = 30000.
	weighN_he = 12000.
if sys.argv[3] == "79i":
	itconfig = phys_services.I3ScaleCalculator.IT73
	icconfig = phys_services.I3ScaleCalculator.IC79
	filelist_name = ["ic79_goodA_i"]
	le_weighter = "7007"
	he_weighter = "7784"
	weighN_le = 30000.
	weighN_he = 12000.
if sys.argv[3] == "86p":
	itconfig = phys_services.I3ScaleCalculator.IT81
	icconfig = phys_services.I3ScaleCalculator.IC86
	filelist_name = ["ic86_goodA_p"]
	#filelist_name = ["singular"]
	le_weighter = "12360"
	he_weighter = "20143"
	weighN_le = 20000.
	weighN_he = 25000.
if sys.argv[3] == "86i":
	itconfig = phys_services.I3ScaleCalculator.IT81
	icconfig = phys_services.I3ScaleCalculator.IC86
	filelist_name = ["ic86_goodA_i"]
	le_weighter = "12362"
	he_weighter = "20144"
	weighN_le = 20000.
	weighN_he = 25000.
reco_object = "IT_mpeLLH_itSEED"
reco_object2 = "II_speLLH_mpeSEED"
#reco_object = "IT_mpeLLH_itSEED_final"
#reco_object2 = "II_speLLH_mpeSEED_final"
figdir = emily+"Plotting/plots/fourth_"+str(int(cutter))+"_"+str(int(deltaE))+"_"+typer+"_"+filelist_name[0]+"_"+reco_object+"_QC_noLOG"
txtdir = emily+"BestPlotters/text/fourth_"+str(int(cutter))+"_"+str(int(deltaE))+"_"+typer+"_"+reco_object+"_"+filelist_name[0]+"_"+str(apply_qcuts)+"_noLOG"


weighter = 2.7
LEstop = 8.
HEstop = 7.

ii_cutter = 0.8
it_cutter = 0.9

ro1zen =[]
ro2zen =[]
lo1zen =[]

trueX =[]
trueY =[]
weight = []
tr1r = []
MCr = []
l1MCr = []
r1MCr = []
r2MCr = []
lo1r = []
ro1r = []
ro2r = []
tlo1xd = []
tlo1yd = []
blo1xd = []
blo1yd = []
lo1x = []
lo1y = []
lo1z = []
lo1a = []
lo1AR = []
lo1CRt = []
lo1CRb = []
lo1cont = []
t_dedx_n=[]
t_nhe_n=[]
t_eng_n=[]
t_eng_3=[]
t_nhe_3=[]
t_dedx_3=[]
t_nhe_4=[]
t_dedx_4=[]
o_dedx_n=[]
o_nhe_n=[]
o_eng_n=[]
o_eng_3=[]
o_nhe_3=[]
o_dedx_3=[]
o_nhe_4=[]
o_dedx_4=[]
m_dedx_n=[]
m_nhe_n=[]
m_eng_n=[]
m_eng_3=[]
m_nhe_3=[]
m_dedx_3=[]
m_nhe_4=[]
m_dedx_4=[]

tro1xd = []
tro1yd = []
bro1xd = []
bro1yd = []
ro1x = []
ro1y = []
ro1z = []
ro1a = []
ro1AR = []
ro1CRt = []
ro1CRb = []
ro1cont = []
ro1amp = []

tro2xd = []
tro2yd = []
bro2xd = []
bro2yd = []
ro2x = []
ro2y = []
ro2z = []
ro2a = []
ro2AR = []
ro2CRt = []
ro2CRb = []
ro2cont = []
ro2amp = []

o_r1MCe=[]
o_r1weight=[]
m_r2MCe=[]
m_r2weight=[]

o_nhe_stoch=[]
o_mass_stoch=[]
o_nhe_stoch2=[]
o_mass_stoch2=[]
m_nhe_stoch=[]
m_mass_stoch=[]
m_nhe_stoch2=[]
m_mass_stoch2=[]


lo1chi2_ldf=[]
lo1chi2_time=[]
ro2chi2_ldf=[]
ro2chi2_time=[]
lo1S125=[]
ro1S125=[]
ro2S125=[]
lo1S125nl=[]
ro1S125nl=[]
ro2S125nl=[]
lo1beta=[]
ro2beta=[]
MCe = []
lMCe = []
r1MCe = []
r2MCe = []
r3MCe = []
ro1_eloss = []
ro2_eloss = []
ro1_e = []
ro2_e = []
lweight = []
r1weight = []
r2weight=[]
r3weight = []
truezen = []

filelist = FileListReturn(emily+"BestPlotters/text/"+filelist_name[0]+".txt")

for filer in filelist:
	if len(filer.split("_")) == 4:
		dataset = filer.split("_")[2]
	else:
		dataset = filer.split("_")[3]
	print filer
	filenamed =  glob.glob(filer)[0]
	i3f = dataio.I3File(str(filenamed), "r")
	for f in i3f:
		filtered = False	
		if "MCPrimary" in f:
	       		geo = f["I3Geometry"]
			MCP = f["MCPrimary"]
			calculator = phys_services.I3ScaleCalculator(geo, icconfig, itconfig)
			scale_inice = calculator.scale_inice(MCP)
			scale_icetop = calculator.scale_icetop(MCP)
			filtered = Grouper(geo,MCP,icconfig,itconfig,typer)
			if filtered == True:
				logE = np.log10(MCP.energy)
				nev =0
				if logE > 6.0:
					MXi = MCP.pos.x
					MYi = MCP.pos.y
					MZi = MCP.pos.z
					zen = MCP.dir.zenith
					azi = MCP.dir.azimuth
					MXf, MYf,z = Projection(MXi,MYi,zen,azi,1950.,'down')
					weighter_all =  Weighting(logE,dataset,le_weighter,he_weighter)
					weight.append(Weighting(logE,dataset,le_weighter,he_weighter))
					MCr.append(np.sqrt((MXi*MXi)+(MYi*MYi))) 	
					trueX.append(MXi)
					trueY.append(MYi)
					truezen.append(np.degrees(zen))
					MCe.append(logE)

					inform =False
					if (("Laputop" in f) and (str( f["Laputop"].fit_status)=='OK')):
						if apply_qcuts == True: 
						        inform = QualityCuts(f,"IT73AnalysisIceTopQualityCuts")
							if (inform == True) :
								LUT = f["Laputop"]
								LUTprms = I3LaputopParams.from_frame(f, "LaputopParams")
								LXi = LUT.pos.x
								LYi = LUT.pos.y
								LZi = LUT.pos.z
								LO1zen = LUT.dir.zenith
								LO1azi = LUT.dir.azimuth
								LXf, LYf,z = Projection(LXi,LYi,zen,azi,1950.,'down')
								l1MCr.append(np.sqrt((MXi*MXi)+(MYi*MYi)))
								lo1r.append(np.sqrt((LXi*LXi)+(LYi*LYi))) 	
								tlo1xd.append(MXi-LXi) 	
								tlo1yd.append(MYi-LYi) 
								blo1xd.append(MXf-LXf) 
								blo1yd.append(MYf-LYf) 
								lo1x.append(LXi) 
								lo1y.append(LYi) 
								lo1z.append(np.degrees(MCP.dir.zenith-LO1zen))
								lo1a.append(np.degrees(MCP.dir.azimuth-LO1azi))
								lo1AR.append(open_angle(LO1zen,LO1azi,zen,azi))
								lo1CRt.append(DistFromCore(LXi,LYi,MXi,MYi))
								lo1CRb.append(DistFromCore(LXf,LYf,MXf,MYf))

								lo1cont.append(scale_icetop)
								lweight.append(weighter_all)
								lMCe.append(logE)

								lo1S125nl.append(10.**LUTprms.value(Par.Log10_S125))
								lo1S125.append(LUTprms.value(Par.Log10_S125))
								lo1beta.append(LUTprms.value(Par.Beta))
								lo1_ndof =LUTprms.ndf
								lo1_chi2_ldf =LUTprms.chi2_ldf
								lo1_chi2_time =LUTprms.chi2_time
								lo1chi2_ldf.append(lo1_ndof*lo1_chi2_ldf)
								lo1zen.append(np.degrees(LO1zen))
								lo1chi2_time.append(lo1_ndof*lo1_chi2_time)

						if (("CoincMuonReco_"+cii_type in f) and (str( f["CoincMuonReco_"+cii_type].fit_status)=='OK')):
							if (('Stoch_Reco' in f) or ('Stoch_Reco2' in f)):
								RO1 = f["CoincMuonReco_"+cii_type]
							if apply_qcuts == True:
							        inform = QualityCuts(f,"IT73AnalysisInIceQualityCuts")
							if (inform == True) :
								RO1Xf = RO1.pos.x
								RO1Yf = RO1.pos.y
								RO1Zf = RO1.pos.z
								RO1zen = RO1.dir.zenith
								ro1zen.append(np.degrees(RO1zen))
								RO1azi = RO1.dir.azimuth
								RO1Xi, RO1Yi,z = Projection(RO1Xf,RO1Yf,zen,azi,1950.,'up')
								r1MCr.append(np.sqrt((MXi*MXi)+(MYi*MYi)))
								ro1r.append(np.sqrt((RO1Xi*RO1Xi)+(RO1Yi*RO1Yi))) 	
								tro1xd.append(MXi-RO1Xi) 
								tro1yd.append(MYi-RO1Yi) 
								bro1xd.append(MXf-RO1Xf) 
								bro1yd.append(MYf-RO1Yf) 
								ro1x.append(RO1Xi) 
								ro1y.append(RO1Yi) 
								ro1z.append(np.degrees(MCP.dir.zenith-RO1zen))
								ro1a.append(np.degrees(MCP.dir.azimuth-RO1azi))
								ro1AR.append(open_angle(RO1zen,RO1azi,zen,azi))
								ro1CRt.append(DistFromCore(RO1Xi,RO1Yi,MXi,MYi))
								ro1CRb.append(DistFromCore(RO1Xf,RO1Yf,MXf,MYf))
	
								ro1cont.append(scale_icetop)
								r1weight.append(weighter_all)
								r1MCe.append(logE)
								o_r1weight.append(weighter_all)
								o_r1MCe.append(logE)
                                                                oeloss = []
                                                                odepth = []
                                                                for X in f["Millipede_dEdX"]:
                                                                        oeloss.append(X.energy)
                                                                        odepth.append(2000. - X.pos.z)
                                                                oXbin, ostochloss = StochGrab(f,"Stoch_Reco")
                                                                oeloss_fit = muonBundleEnergyLossFull(odepth,f["Stoch_Reco"].primEnergyEstimate,RO1zen,mass_guess)
                                                                odepth2, oeloss2, oeloss_fit2, oeloss_cut2, o_nhe, oEguess, odepth3 = NewNHEcounterCut(odepth,oeloss,oXbin, ostochloss,f["Stoch_Reco"].primEnergyEstimate,RO1zen,mass_guess,deltaE)
                                                                nhe_o=o_nhe
                                                                oloss_s=[]
                                                                ocut_s=[]
                                                                ofit_s=[]
                                                                iodep_s=[]
                                                                odep_s=[]
                                                                odep_cuts=[]
                                                                while o_nhe > 0:
                                                                        odep_cuts.append(odepth3)
                                                                        #imdep_s.append(mdepth)
                                                                        odep_s.append(odepth2)
                                                                        oloss_s.append(oeloss2)
                                                                        ocut_s.append(oeloss_cut2)
                                                                        ofit_s.append(oeloss_fit2)
                                                                        odepth2, oeloss2, oeloss_fit2, oeloss_cut2, o_nhe, oEguess, odepth3 = NewNHEcounterCut(odepth2,oeloss2,odepth2,oeloss_fit2,oEguess,RO1zen,mass_guess,deltaE)
                                                                        nhe_o += o_nhe
                                                                iodep_s.append(odepth)
                                                                odep_s.append(odepth2)
                                                                oloss_s.append(oeloss2)
                                                                odep_cuts.append(odepth3)
                                                                ocut_s.append(oeloss_cut2)
                                                                ofit_s.append(oeloss_fit2)
				

                                                                o_dedx_n.append(np.log10(muonBundleEnergyLoss(1500.,oEguess,RO1zen,mass_guess)))
                                                                o_nhe_n.append(nhe_o)
                                                                o_eng_n.append(np.log10(oEguess))




								o_mass_stoch.append(f['Stoch_Reco'].eLoss_1500)
								o_dedx_3.append(f['Stoch_Reco'].eLoss_1500)
								o_nhe_stoch.append(f['Stoch_Reco'].nHEstoch)
								o_nhe_3.append(f['Stoch_Reco'].nHEstoch)
								o_mass_stoch2.append(f['Stoch_Reco2'].eLoss_1500)
								o_dedx_4.append(f['Stoch_Reco2'].eLoss_1500)
								o_nhe_stoch2.append(f['Stoch_Reco2'].nHEstoch)
					                        o_eng_3.append(np.log10(f['Stoch_Reco'].primEnergyEstimate))
								o_nhe_4.append(f['Stoch_Reco2'].nHEstoch)



					inform =False
					if (((reco_object in f) and (str( f[reco_object].fit_status)=='OK'))) or ( ((reco_object2 in f) and (str( f[reco_object2].fit_status)=='OK'))):
						if typer == "G2":
							reco = reco_object2
							dtyper = "II"
							apply_qcuts_g2 = True
								
						if typer == "G1":
							reco = reco_object
							dtyper = "IT"
							apply_qcuts_g2 = False

						if ((starter+'ElossReco_'+reco+'Stoch_Reco_EM' in f) and (starter+'ElossReco_'+reco+'Stoch_Reco2_EM' in f)):
							if apply_qcuts == True:
								if apply_qcuts_g2 == False:
						        		inform = SomeQualityCuts(f,"IT73AnalysisIceTopQualityCuts",[0,5,6])
								if apply_qcuts_g2 == True:
						        		inform = SomeQualityCuts(f,"IT73AnalysisIceTopQualityCuts",[0,1,2,3,5,6])
								if inform == True:
						        		inform = QualityCuts(f,"IT73AnalysisInIceQualityCuts_EM_"+starter+"ElossReco_"+reco)
							if (inform == True) :
								RO2 = f[reco]
								RO2prms = f[reco+"Params"]
								if (("CoincMuonReco_"+cii_type in f) and (str( f["CoincMuonReco_"+cii_type].fit_status)=='OK')):
									if (('Stoch_Reco' in f) or ('Stoch_Reco2' in f)):
										RO1 = f["CoincMuonReco_"+cii_type]
	
										RO1Xf = RO1.pos.x
										RO1Yf = RO1.pos.y
										RO1Zf = RO1.pos.z
										RO1zen = RO1.dir.zenith
										RO1azi = RO1.dir.azimuth
										RO1Xi, RO1Yi,z = Projection(RO1Xf,RO1Yf,RO1zen,RO1azi,1950.,'up')
										if 1.4 < RO2prms["Beta"] < 9.5:
											if DistFromCore(RO1Xi,RO1Yi,RO2.pos.x,RO2.pos.y)< cutter:

												RO2Xi = RO2.pos.x
												RO2Yi = RO2.pos.y
												RO2Zi = RO2.pos.z
												RO2zen = RO2.dir.zenith
												RO2azi = RO2.dir.azimuth
												RO2Xf, RO2Yf,z = Projection(RO2Xi,RO2Yi,zen,azi,1950.,'down')
												if np.isnan(open_angle(RO2zen,RO2azi,RO2zen,RO2azi)) == False:
													r2MCr.append(np.sqrt((MXi*MXi)+(MYi*MYi)))
													ro2r.append(np.sqrt((RO2Xi*RO2Xi)+(RO2Yi*RO2Yi))) 	
													tro2xd.append(MXi-RO2Xi) 
													tro2yd.append(MYi-RO2Yi) 
													bro2xd.append(MXf-RO2Xf) 
													bro2yd.append(MYf-RO2Yf) 
													ro2x.append(RO2Xi) 
													ro2y.append(RO2Yi) 
													ro2z.append(np.degrees(MCP.dir.zenith-RO2zen))
													ro2a.append(np.degrees(MCP.dir.azimuth-RO2azi))
						
													ro2AR.append(open_angle(RO2zen,RO2azi,RO2zen,RO2azi))
													ro2CRt.append(DistFromCore(RO2Xi,RO2Yi,MXi,MYi))
													ro2CRb.append(DistFromCore(RO2Xf,RO2Yf,MXf,MYf))
		
													ro2cont.append(scale_icetop)
													r2weight.append(weighter_all)
													r2MCe.append(logE)
		
													ro2S125nl.append(10.**RO2prms["Log10_S125"])
													ro2S125.append(RO2prms["Log10_S125"])
													ro2zen.append(np.degrees(RO2zen))
													ro2beta.append(RO2prms["Beta"])
													ro2amp.append(RO2prms["Amp"])
													ro2chi2_ldf.append(RO2prms["Chi2_ldf"])
													ro2chi2_time.append(RO2prms["Chi2_time"])
	
													m_r2weight.append(weighter_all)
													m_r2MCe.append(logE)
					                                                                meloss = []
					                                                                mdepth = []
					                                                                for X in f[starter+"ElossReco_"+reco+"Millipede_dEdX_EM"]:
	                                        				                                meloss.append(X.energy)
                                                                        					mdepth.append(2000. - X.pos.z)
					                                                                mXbin, mstochloss = StochGrab(f,starter+"ElossReco_"+reco+"Stoch_Reco_EM")
                                        					                        meloss_fit = muonBundleEnergyLossFull(mdepth,f[starter+"ElossReco_"+reco+"Stoch_Reco_EM"].primEnergyEstimate,RO2zen,mass_guess)
					                                                                mdepth2, meloss2, meloss_fit2, meloss_cut2, m_nhe, Eguess, mdepth3 = NewNHEcounterCut(mdepth,meloss,mXbin, mstochloss,f[starter+"ElossReco_"+reco+"Stoch_Reco_EM"].primEnergyEstimate,RO2zen,mass_guess,deltaE)
                                        					                        nhe_m=m_nhe
					                                                                mloss_s=[]
                                        					                        mcut_s=[]
					                                                                mfit_s=[]
                                        					                        imdep_s=[]
					                                                                mdep_s=[]
                                        					                        mdep_cuts=[]
					                                                                while m_nhe > 0:
                                        					                                mdep_cuts.append(mdepth3)
					                                                                        #imdep_s.append(mdepth)
                                        					                                mdep_s.append(mdepth2)
					                                                                        mloss_s.append(meloss2)
                                        					                                mcut_s.append(meloss_cut2)
					                                                                        mfit_s.append(meloss_fit2)
                                        				                                	mdepth2, meloss2, meloss_fit2, meloss_cut2, m_nhe, Eguess, mdepth3 = NewNHEcounterCut(mdepth2,meloss2,mdepth2,meloss_fit2,Eguess,RO2zen,mass_guess,deltaE)
                                                                        					nhe_m += m_nhe
					                                                                imdep_s.append(mdepth)
					                                                                mdep_s.append(mdepth2)
					                                                                mloss_s.append(meloss2)
					                                                                mdep_cuts.append(mdepth3)
					                                                                mcut_s.append(meloss_cut2)
					                                                                mfit_s.append(meloss_fit2)

                					                                		m_mass_stoch.append(f[starter+'ElossReco_'+reco+'Stoch_Reco_EM'].eLoss_1500)
                					                                		m_dedx_3.append(f[starter+'ElossReco_'+reco+'Stoch_Reco_EM'].eLoss_1500)
													m_nhe_3.append(f[starter+'ElossReco_'+reco+'Stoch_Reco_EM'].nHEstoch)
													m_nhe_stoch.append(f[starter+'ElossReco_'+reco+'Stoch_Reco_EM'].nHEstoch)
													m_mass_stoch2.append(f[starter+'ElossReco_'+reco+'Stoch_Reco2_EM'].eLoss_1500)
													m_dedx_4.append(f[starter+'ElossReco_'+reco+'Stoch_Reco2_EM'].eLoss_1500)
													m_nhe_4.append(f[starter+'ElossReco_'+reco+'Stoch_Reco2_EM'].nHEstoch)
													m_nhe_stoch2.append(f[starter+'ElossReco_'+reco+'Stoch_Reco2_EM'].nHEstoch)
                                                                					m_eng_3.append(np.log10(f[starter+'ElossReco_'+reco+'Stoch_Reco_EM'].primEnergyEstimate))
					                                                                m_dedx_n.append(np.log10(muonBundleEnergyLoss(1500.,Eguess,RO2zen,mass_guess)))
					                                                                m_nhe_n.append(nhe_m)
					                                                                m_eng_n.append(np.log10(Eguess))



print "MC",len(MCe)
print "IT",len(lMCe)
print "II",len(r1MCe)
print "3D",len(r2MCe)


file = open(txtdir+"_S125all.txt","w")
for i in np.arange(0,len(lo1S125nl),1): 
	file.write("L01\t"+str(lo1S125nl[i])+"\n") 
for i in np.arange(0,len(ro2S125nl),1): 
	file.write("R02\t"+str(ro2S125nl[i])+"\n") 
file.close() 

file = open(txtdir+"_recoZen.txt","w")
for i in np.arange(0,len(lo1zen),1): 
	file.write("L01\t"+str(lo1zen[i])+"\t"+str(lweight[i])+"\n") 
for i in np.arange(0,len(ro1zen),1): 
	file.write("R01\t"+str(ro1zen[i])+"\t"+str(r1weight[i])+"\n") 
for i in np.arange(0,len(ro2zen),1): 
	file.write("R02\t"+str(ro2zen[i])+"\t"+str(r2weight[i])+"\n") 
file.close() 







s125_bins = np.linspace(0,5,binN)
pylab.figure()
plt.hist2d(trueX, trueY, bins=75, norm=LogNorm(),weights=weight)
plt.colorbar()
pylab.xlabel("X [m]")
pylab.ylabel("Y [m]")
pylab.title("True")
pylab.ylim([-2000,2000])
pylab.xlim([-2000,2000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_hitLOCAL_true.png")
pylab.close()

pylab.figure()
plt.hist2d(lo1x, lo1y, bins=75, norm=LogNorm(),weights=lweight)
plt.colorbar()
pylab.xlabel("X [m]")
pylab.ylabel("Y [m]")
pylab.title("Laputop")
pylab.ylim([-2000,2000])
pylab.xlim([-2000,2000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_hitLOCAL_it.png")
pylab.close()



pylab.figure()
if (apply_qcuts == False) and (typer == "G2"):
	plt.hist2d(ro2x, ro2y, bins=1000, norm=LogNorm(),weights=r2weight)
else:
	plt.hist2d(ro2x, ro2y, bins=75, norm=LogNorm(),weights=r2weight)
plt.colorbar()
pylab.xlabel("X [m]")
pylab.ylabel("Y [m]")
pylab.title("Combo")
pylab.ylim([-2000,2000])
pylab.xlim([-2000,2000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_hitLOCAL_comb.png")
pylab.close()

pylab.figure()
plt.hist2d(ro1x, ro1y, bins=75, norm=LogNorm(),weights=r1weight)
plt.colorbar()
pylab.xlabel("X [m]")
pylab.ylabel("Y [m]")
pylab.title("InIce")
pylab.ylim([-2000,2000])
pylab.xlim([-2000,2000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_hitLOCAL_ii.png")
pylab.close()

print "Resolutions"
AR_bins =  np.linspace(-2,6,200)
l1ARx, l1ARy =  Resolution(eng_bins, binN, lMCe, lo1AR, lweight, AR_bins)
r1ARx, r1ARy =  Resolution(eng_bins, binN, r1MCe, ro1AR, r1weight, AR_bins)
r2ARx, r2ARy =  Resolution(eng_bins, binN, r2MCe, ro2AR, r2weight, AR_bins)
pylab.figure()
plt.plot(r2ARx, r2ARy,linewidth=1.5,drawstyle='steps',color = 'r')
plt.plot(r1ARx, r1ARy,linewidth=1.5,drawstyle='steps',color = 'b')
plt.plot(l1ARx, l1ARy,linewidth=1.5,drawstyle='steps',color = 'g')
#pylab.legend(["3-D","II-only","IT-only"],loc=2)
pylab.ylabel(r"Angular Resolution ($\circ$)")
pylab.xlabel(r"log$_{10}$(E[GeV])")
pylab.ylim([0,3])
pylab.xlim([6,9.5])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_AngResoProf.png")
pylab.close()
file = open(txtdir+"_AngResoProfvE.txt","w")
for i in np.arange(0,len(l1ARx),1): 
	file.write("L01\t"+str(l1ARx[i])+"\t"+str(l1ARy[i])+"\n") 
for i in np.arange(0,len(r1ARx),1): 
	file.write("R01\t"+str(r1ARx[i])+"\t"+str(r1ARy[i])+"\n") 
for i in np.arange(0,len(r2ARx),1): 
	file.write("R02\t"+str(r2ARx[i])+"\t"+str(r2ARy[i])+"\n") 
file.close() 

CR_bins =  np.linspace(0.,20.,200)
l1CRTx, l1CRTy =  Resolution(eng_bins, binN, lMCe, lo1CRt, lweight, CR_bins)
r1CRTx, r1CRTy =  Resolution(eng_bins, binN, r1MCe, ro1CRt, r1weight, CR_bins)
r2CRTx, r2CRTy =  Resolution(eng_bins, binN, r2MCe, ro2CRt, r2weight, CR_bins)
pylab.figure()
plt.plot(r2CRTx, r2CRTy,linewidth=1.5,drawstyle='steps',color = 'r')
plt.plot(r1CRTx, r1CRTy,linewidth=1.5,drawstyle='steps',color = 'b')
plt.plot(l1CRTx, l1CRTy,linewidth=1.5,drawstyle='steps',color = 'g')
#pylab.legend(["3-D","II-only","IT-only"],loc=2)
pylab.ylabel("Top Core Resolution (m)")
pylab.xlabel(r"log$_{10}$(E[GeV])")
pylab.xlim([6,9.5])
pylab.ylim([0,30])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_TopCoreResoProf.png")
pylab.close()
file = open(txtdir+"_TopCoreResoProfvE.txt","w")
for i in np.arange(0,len(l1CRTx),1): 
	file.write("L01\t"+str(l1CRTx[i])+"\t"+str(l1CRTy[i])+"\n") 
for i in np.arange(0,len(r1CRTx),1): 
	file.write("R01\t"+str(r1CRTx[i])+"\t"+str(r1CRTy[i])+"\n") 
for i in np.arange(0,len(r2CRTx),1): 
	file.write("R02\t"+str(r2CRTx[i])+"\t"+str(r2CRTy[i])+"\n") 
file.close() 


l1CRBx, l1CRBy =  Resolution(eng_bins, binN, lMCe, lo1CRb, lweight, CR_bins)
r1CRBx, r1CRBy =  Resolution(eng_bins, binN, r1MCe, ro1CRb, r1weight, CR_bins)
r2CRBx, r2CRBy =  Resolution(eng_bins, binN, r2MCe, ro2CRb, r2weight, CR_bins)
pylab.figure()
plt.plot(r2CRBx, r2CRBy, linewidth=1.5,drawstyle='steps',color = 'r')
plt.plot(r1CRBx, r1CRBy, linewidth=1.5,drawstyle='steps',color = 'b')
plt.plot(l1CRBx, l1CRBy, linewidth=1.5,drawstyle='steps',color = 'g')
#pylab.legend(["3-D","II-only","IT-only"],loc=2)
pylab.ylabel("Bottom Core Resolution (m)")
pylab.xlabel(r"log$_{10}$(E[GeV])")
pylab.xlim([6,9.5])
pylab.ylim([0,50])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_BotCoreResoProf.png")
file = open(txtdir+"_BotCoreResoProfvE.txt","w")
for i in np.arange(0,len(l1CRBx),1): 
	file.write("L01\t"+str(l1CRBx[i])+"\t"+str(l1CRBy[i])+"\n") 
for i in np.arange(0,len(r1CRBx),1): 
	file.write("R01\t"+str(r1CRBx[i])+"\t"+str(r1CRBy[i])+"\n") 
for i in np.arange(0,len(r2CRBx),1): 
	file.write("R02\t"+str(r2CRBx[i])+"\t"+str(r2CRBy[i])+"\n") 
file.close() 






















print "IT Params Histos"
beta_bins = np.linspace(0, 7,binN)
lo1B_ystep, lo1B_almost_xstep, crap = plt.hist(lo1beta, beta_bins,weights=lweight)
ro2B_ystep, ro2B_almost_xstep, crap = plt.hist(ro2beta, beta_bins,weights=r2weight)
lo1B_xstep=[]
ro1B_xstep=[]
ro2B_xstep=[]
for i in np.arange(0,binN-1,1):
        lo1B_xstep.append((lo1B_almost_xstep[i]+lo1B_almost_xstep[i+1])/2.)
        ro2B_xstep.append((ro2B_almost_xstep[i]+ro2B_almost_xstep[i+1])/2.)
pylab.figure()
fig, ax = plt.subplots()
textstr = '\n'.join((
    r'IT $\mu=%.2f$' % (np.mean(lo1beta), ),
    r'IT $\sigma=%.2f$' % (np.std(lo1beta), ),
    r'IT $\mathrm{count}=%.2f$' % (len(lo1beta),),
    r'RB $\mu=%.2f$' % (np.mean(ro2beta), ),
    r'RB $\sigma=%.2f$' % (np.std(ro2beta), ),
    r'RB $\mathrm{count}=%.2f$' % (len(ro2beta),)))
ax.text(0.80, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top')
plt.plot(ro2B_xstep, ro2B_ystep,linewidth=1.5, drawstyle='steps',color = 'r')
plt.plot(lo1B_xstep, lo1B_ystep,linewidth=1.5, linestyle='--',drawstyle='steps',color = 'g')
pylab.xlim([0,7])
pylab.ylabel("Rate [1/s]")
pylab.xlabel(r"$\beta$")
plt.grid(True,which="both",ls="-")
if typer == "G2":
	pylab.ylim([0,1*(10**-12)])
else:
	pylab.ylim([0,1*(10**-11)])
pylab.savefig(figdir+"_hist_beta.png")
pylab.close()


print "Geomtery Histos"
limit = 100
small_limit = 50
zlimit = 25.
small_zlimit = 5
ZbinN = 150

x_bins = np.linspace(-1.*limit,limit,binN)
lo1X_ystep, lo1X_almost_xstep, crap = plt.hist(tlo1xd, x_bins,weights=lweight)
ro1X_ystep, ro1X_almost_xstep, crap = plt.hist(tro1xd, x_bins,weights=r1weight)
ro2X_ystep, ro2X_almost_xstep, crap = plt.hist(tro2xd, x_bins,weights=r2weight)
lo1X_xstep=[]
ro1X_xstep=[]
ro2X_xstep=[]
for i in np.arange(0,binN-1,1):
        lo1X_xstep.append((lo1X_almost_xstep[i]+lo1X_almost_xstep[i+1])/2.)
        ro1X_xstep.append((ro1X_almost_xstep[i]+ro1X_almost_xstep[i+1])/2.)
        ro2X_xstep.append((ro2X_almost_xstep[i]+ro2X_almost_xstep[i+1])/2.)
pylab.figure()
fig, ax = plt.subplots()
textstr = '\n'.join((
    r'IT $\mu=%.2f$' % (np.mean(tlo1xd), ),
    r'IT $\sigma=%.2f$' % (np.std(tlo1xd), ),
    r'IT $\mathrm{count}=%.2f$' % (len(tlo1xd),),
    r'II $\mu=%.2f$' % (np.mean(tro1xd), ),
    r'II $\sigma=%.2f$' % (np.std(tro1xd), ),
    r'II $\mathrm{count}=%.2f$' % (len(tro1xd),),
    r'RB $\mu=%.2f$' % (np.mean(tro2xd), ),
    r'RB $\sigma=%.2f$' % (np.std(tro2xd), ),
    r'RB $\mathrm{count}=%.2f$' % (len(tro2xd),)))
ax.text(0.80, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top')
plt.plot(ro2X_xstep, ro2X_ystep,linewidth=1.5, drawstyle='steps',color = 'r')
plt.plot(ro1X_xstep, ro1X_ystep,linewidth=1.5, linestyle=':',drawstyle='steps',color = 'b')
plt.plot(lo1X_xstep, lo1X_ystep,linewidth=1.5, linestyle='--',drawstyle='steps',color = 'g')
pylab.legend(["Combined",cii_type,"Laputop"],loc=2)
pylab.xlim([-limit,limit])
pylab.ylabel("Rate [1/s]")
pylab.xlabel("(True - Reco) X [m]")
#pylab.yscale('log')
if typer == "G2":
	if apply_qcuts == True:
		pylab.ylim([0,1*(10**-12)])
		pylab.xlim([-50,50])
	if apply_qcuts == False:
		pylab.ylim([0,1*(10**-12)])
		pylab.xlim([-50,50])
else:
	pylab.ylim([0,1*(10**-12)])
	pylab.xlim([-50,50])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_hist_X_top.png")
pylab.close()

x_bins = np.linspace(-1.*small_limit,small_limit,binN)
lo1X_ystep, lo1X_almost_xstep, crap = plt.hist(tlo1xd, x_bins,weights=lweight)
ro1X_ystep, ro1X_almost_xstep, crap = plt.hist(tro1xd, x_bins,weights=r1weight)
ro2X_ystep, ro2X_almost_xstep, crap = plt.hist(tro2xd, x_bins,weights=r2weight)
lo1X_xstep=[]
ro1X_xstep=[]
ro2X_xstep=[]
for i in np.arange(0,binN-1,1):
        lo1X_xstep.append((lo1X_almost_xstep[i]+lo1X_almost_xstep[i+1])/2.)
        ro1X_xstep.append((ro1X_almost_xstep[i]+ro1X_almost_xstep[i+1])/2.)
        ro2X_xstep.append((ro2X_almost_xstep[i]+ro2X_almost_xstep[i+1])/2.)
pylab.figure()
fig, ax = plt.subplots()
textstr = '\n'.join((
    r'IT $\mu=%.2f$' % (np.mean(tlo1xd), ),
    r'IT $\sigma=%.2f$' % (np.std(tlo1xd), ),
    r'IT $\mathrm{count}=%.2f$' % (len(tlo1xd),),
    r'II $\mu=%.2f$' % (np.mean(tro1xd), ),
    r'II $\sigma=%.2f$' % (np.std(tro1xd), ),
    r'II $\mathrm{count}=%.2f$' % (len(tro1xd),),
    r'RB $\mu=%.2f$' % (np.mean(tro2xd), ),
    r'RB $\sigma=%.2f$' % (np.std(tro2xd), ),
    r'RB $\mathrm{count}=%.2f$' % (len(tro2xd),)))
ax.text(0.80, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top')
plt.plot(ro2X_xstep, ro2X_ystep,linewidth=1.5, drawstyle='steps',color = 'r')
plt.plot(ro1X_xstep, ro1X_ystep,linewidth=1.5, linestyle=':',drawstyle='steps',color = 'b')
plt.plot(lo1X_xstep, lo1X_ystep,linewidth=1.5, linestyle='--',drawstyle='steps',color = 'g')
pylab.legend(["3D","II-only","IT-only"],loc=2)
pylab.ylabel("Rate [1/s]")
pylab.xlabel("(True - Reco) X [m]")
#pylab.yscale('log')
pylab.xlim([-25,25])
plt.grid(True,which="both",ls="-")
if typer == "G2":
	if apply_qcuts == True:
		pylab.ylim([0,1*(10**-12)])
		pylab.xlim([-50,50])
	if apply_qcuts == False:
		pylab.ylim([0,2*(10**-12)])
		pylab.xlim([-50,50])
else:
	pylab.ylim([0,1*(10**-12)])
	pylab.xlim([-50,50])
pylab.savefig(figdir+"_hist_X_top_small.png")
pylab.close()
pylab.figure()
fig, ax = plt.subplots()
textstr = '\n'.join((
    r'II $\mu=%.2f$' % (np.mean(tro1xd), ),
    r'II $\sigma=%.2f$' % (np.std(tro1xd), ),
    r'II $\mathrm{count}=%.2f$' % (len(tro1xd),),
    r'RB $\mu=%.2f$' % (np.mean(tro2xd), ),
    r'RB $\sigma=%.2f$' % (np.std(tro2xd), ),
    r'RB $\mathrm{count}=%.2f$' % (len(tro2xd),)))
ax.text(0.80, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top')
plt.plot(ro2X_xstep, ro2X_ystep,linewidth=1.5, drawstyle='steps',color = 'r')
plt.plot(ro1X_xstep, ro1X_ystep,linewidth=1.5, linestyle=':',drawstyle='steps',color = 'b')
pylab.legend(["3D","II-only"],loc=2)
pylab.ylabel("Rate [1/s]")
pylab.xlabel("(True - Reco) X [m]")
#pylab.yscale('log')
pylab.xlim([-25,25])
plt.grid(True,which="both",ls="-")
"""
if typer == "G2":
	if apply_qcuts == True:
		pylab.ylim([0,1*(10**-12)])
		pylab.xlim([-50,50])
	if apply_qcuts == False:
		pylab.ylim([0,2*(10**-12)])
		pylab.xlim([-50,50])
else:
	pylab.ylim([0,1*(10**-12)])
	pylab.xlim([-50,50])
"""
pylab.savefig(figdir+"_hist_X_top_small_g2.png")
pylab.close()



























zen_bins = np.linspace(0,90,40)
trueZen_ystep, trueZen_almost_xstep, crap = plt.hist(truezen, zen_bins,weights=weight)
trueZen_xstep=[]
for i in np.arange(0,40-1,1):
        trueZen_xstep.append((trueZen_almost_xstep[i]+trueZen_almost_xstep[i+1])/2.)
pylab.figure()
fig, ax = plt.subplots()
plt.plot(trueZen_xstep, trueZen_ystep,linewidth=1.5,drawstyle='steps',color = 'k')
pylab.ylabel("Rate [1/s]")
pylab.xlabel("(True - Reco) Zenith [deg]")
pylab.yscale('log')
#pylab.ylim([0,1*(10**-12)])
#pylab.xlim([-20,20])
plt.grid(True,which="both",ls="-")
#if typer == "G2":
#	pylab.ylim([0,2*(10**-13)])
#else:
#	pylab.ylim([0,5*(10**-13)])
pylab.savefig(figdir+"_hist_trueZen.png")
pylab.close()
file = open(txtdir+"_trueZen.txt","w")
for i in np.arange(0,len(trueZen_xstep),1): 
	file.write("R02\t"+str(trueZen_xstep[i])+"\t"+str(trueZen_ystep[i])+"\n") 
file.close() 

zen_bins = np.linspace(-1.*zlimit,zlimit,ZbinN)
lo1Zen_ystep, lo1Zen_almost_xstep, crap = plt.hist(lo1z, zen_bins,weights=lweight)
ro1Zen_ystep, ro1Zen_almost_xstep, crap = plt.hist(ro1z, zen_bins,weights=r1weight)
ro2Zen_ystep, ro2Zen_almost_xstep, crap = plt.hist(ro2z, zen_bins,weights=r2weight)
lo1Zen_xstep=[]
ro1Zen_xstep=[]
ro2Zen_xstep=[]
for i in np.arange(0,ZbinN-1,1):
        lo1Zen_xstep.append((lo1Zen_almost_xstep[i]+lo1Zen_almost_xstep[i+1])/2.)
        ro1Zen_xstep.append((ro1Zen_almost_xstep[i]+ro1Zen_almost_xstep[i+1])/2.)
        ro2Zen_xstep.append((ro2Zen_almost_xstep[i]+ro2Zen_almost_xstep[i+1])/2.)
pylab.figure()
fig, ax = plt.subplots()
textstr = '\n'.join((
    r'IT $\mu=%.2f$' % (np.mean(lo1z), ),
    r'IT $\sigma=%.2f$' % (np.std(lo1z), ),
    r'IT $\mathrm{count}=%.2f$' % (len(lo1z),),
    r'II $\mu=%.2f$' % (np.mean(ro1z), ),
    r'II $\sigma=%.2f$' % (np.std(ro1z), ),
    r'II $\mathrm{count}=%.2f$' % (len(ro1z),),
    r'RB $\mu=%.2f$' % (np.mean(ro2z), ),
    r'RB $\sigma=%.2f$' % (np.std(ro2z), ),
    r'RB $\mathrm{count}=%.2f$' % (len(ro2z),)))
ax.text(0.80, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top')
plt.plot(ro2Zen_xstep, ro2Zen_ystep,linewidth=1.5, drawstyle='steps',color = 'r')
plt.plot(ro1Zen_xstep, ro1Zen_ystep,linewidth=1.5, linestyle=':',drawstyle='steps',color = 'b')
plt.plot(lo1Zen_xstep, lo1Zen_ystep,linewidth=1.5, linestyle='--',drawstyle='steps',color = 'g')
pylab.legend(["Combined",cii_type,"Laputop"],loc=2)
pylab.ylabel("Rate [1/s]")
pylab.xlabel("(True - Reco) Zenith [deg]")
#pylab.yscale('log')
pylab.ylim([0,1*(10**-12)])
pylab.xlim([-20,20])
plt.grid(True,which="both",ls="-")
if typer == "G2":
	pylab.ylim([0,1*(10**-12)])
else:
	pylab.ylim([0,1*(10**-12)])
pylab.savefig(figdir+"_hist_Zen.png")
pylab.close()



szen_bins = np.linspace(-1.*small_zlimit,small_zlimit,limit)
lo1Zen_ystep, lo1Zen_almost_xstep, crap = plt.hist(lo1z, szen_bins,weights=lweight)
ro1Zen_ystep, ro1Zen_almost_xstep, crap = plt.hist(ro1z, szen_bins,weights=r1weight)
ro2Zen_ystep, ro2Zen_almost_xstep, crap = plt.hist(ro2z, szen_bins,weights=r2weight)
lo1Zen_xstep=[]
ro1Zen_xstep=[]
ro2Zen_xstep=[]
for i in np.arange(0,limit-1,1):
        lo1Zen_xstep.append((lo1Zen_almost_xstep[i]+lo1Zen_almost_xstep[i+1])/2.)
        ro1Zen_xstep.append((ro1Zen_almost_xstep[i]+ro1Zen_almost_xstep[i+1])/2.)
        ro2Zen_xstep.append((ro2Zen_almost_xstep[i]+ro2Zen_almost_xstep[i+1])/2.)
pylab.figure()
fig, ax = plt.subplots()
textstr = '\n'.join((
    r'IT $\mu=%.2f$' % (np.mean(lo1z), ),
    r'IT $\sigma=%.2f$' % (np.std(lo1z), ),
    r'IT $\mathrm{count}=%.2f$' % (len(lo1z),),
    r'II $\mu=%.2f$' % (np.mean(ro1z), ),
    r'II $\sigma=%.2f$' % (np.std(ro1z), ),
    r'II $\mathrm{count}=%.2f$' % (len(ro1z),),
    r'RB $\mu=%.2f$' % (np.mean(ro2z), ),
    r'RB $\sigma=%.2f$' % (np.std(ro2z), ),
    r'RB $\mathrm{count}=%.2f$' % (len(ro2z),)))
ax.text(0.80, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top')
plt.plot(ro2Zen_xstep, ro2Zen_ystep,linewidth=1.5, drawstyle='steps',color = 'r')
plt.plot(ro1Zen_xstep, ro1Zen_ystep,linewidth=1.5, linestyle=':',drawstyle='steps',color = 'b')
plt.plot(lo1Zen_xstep, lo1Zen_ystep,linewidth=1.5, linestyle='--',drawstyle='steps',color = 'g')
pylab.legend(["3D","II-only","IT-only"],loc=2)
pylab.ylabel("Rate [1/s]")
pylab.xlabel("(True - Reco) Zenith [deg]")
#pylab.yscale('log')
pylab.ylim([0,1*(10**-12)])
pylab.xlim([-2.5,2.5])
plt.grid(True,which="both",ls="-")
if typer == "G2":
	pylab.ylim([0,1*(10**-12)])
else:
	pylab.ylim([0,1*(10**-12)])
pylab.savefig(figdir+"_hist_Zen_small.png")
pylab.close()
pylab.figure()
fig, ax = plt.subplots()
textstr = '\n'.join((
    r'II $\mu=%.2f$' % (np.mean(ro1z), ),
    r'II $\sigma=%.2f$' % (np.std(ro1z), ),
    r'II $\mathrm{count}=%.2f$' % (len(ro1z),),
    r'RB $\mu=%.2f$' % (np.mean(ro2z), ),
    r'RB $\sigma=%.2f$' % (np.std(ro2z), ),
    r'RB $\mathrm{count}=%.2f$' % (len(ro2z),)))
ax.text(0.80, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top')
plt.plot(ro2Zen_xstep, ro2Zen_ystep,linewidth=1.5, drawstyle='steps',color = 'r')
plt.plot(ro1Zen_xstep, ro1Zen_ystep,linewidth=1.5, linestyle=':',drawstyle='steps',color = 'b')
pylab.legend(["3D","II-only"],loc=2)
pylab.ylabel("Rate [1/s]")
pylab.xlabel("(True - Reco) Zenith [deg]")
#pylab.yscale('log')
pylab.ylim([0,1*(10**-12)])
pylab.xlim([-2.5,2.5])
plt.grid(True,which="both",ls="-")
"""
if typer == "G2":
	pylab.ylim([0,1*(10**-12)])
else:
	pylab.ylim([0,1*(10**-12)])
"""
pylab.savefig(figdir+"_hist_Zen_small_g2.png")
pylab.close()












rad_bins = np.linspace(0,1500,binN)
l1Rx, l1Rxer, l1Ry, l1Ryer =  Profiled(rad_bins, binN, l1MCr, lo1r, lweight)
r1Rx, r1Rxer, r1Ry, r1Ryer =  Profiled(rad_bins, binN, r1MCr, ro1r, r1weight)
r2Rx, r2Rxer, r2Ry, r2Ryer =  Profiled(rad_bins, binN, r2MCr, ro2r, r2weight)
pylab.figure()
plt.errorbar(r2Rx, r2Ry, yerr=r2Ryer,linewidth=1.5, linestyle='-',ecolor='red',fmt='r',capsize=5)
plt.errorbar(l1Rx, l1Ry, yerr=l1Ryer,linewidth=1.5, linestyle='--',ecolor='green',fmt='g',capsize=5)
plt.errorbar(r1Rx, r1Ry, yerr=r1Ryer,linewidth=1.5, linestyle=':',ecolor='blue',fmt='b',capsize=5)
pylab.legend(["Combined","Laputop","InIce"],loc=2)
pylab.xlabel("True Radius from Icetop Core [m]")
pylab.ylabel("Reco Radius from Icetop Core [m]")
pylab.xlim([0,1600])
pylab.ylim([0,1600])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_compRvE.png")
pylab.close()

print "IT Params Profiles"
s125 = np.arange(0,5,0.2)

l1Bx, l1Bxer, l1By, l1Byer =  Profiled(s125_bins, binN, lo1S125, lo1beta, lweight)
r2Bx, r2Bxer, r2By, r2Byer =  Profiled(s125_bins, binN, ro2S125, ro2beta, r2weight)
pylab.figure()
plt.hist2d(ro2S125, ro2beta, bins=75, norm=LogNorm(),weights=r2weight)
plt.errorbar(r2Bx, r2By, yerr=r2Byer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$\beta$")
pylab.title("Combo")
pylab.xlim([0,5])
pylab.ylim([0,10])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_ro2BetavS125.png")
pylab.close()
pylab.figure()
plt.hist2d(lo1S125, lo1beta, bins=75, norm=LogNorm(),weights=lweight)
plt.errorbar(l1Bx, l1By, yerr=l1Byer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$\beta$")
pylab.title("Laputop")
pylab.xlim([0,5])
pylab.ylim([0,10])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_lo1BetavS125.png")
pylab.close()
pylab.figure()
plt.errorbar(r2Bx, r2By, yerr=r2Byer, fmt='r-',capsize=5)
plt.errorbar(l1Bx, l1By, yerr=l1Byer, fmt='g-',capsize=5)
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$\beta$")
pylab.xlim([0,5])
pylab.ylim([0,10])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_compBetavS125.png")
pylab.close()
# test here to write file on Beta
file = open(txtdir+"_BetavS125.txt","w")
for i in np.arange(0,len(l1Bx),1): 
	 file.write("L01\t"+str(l1Bx[i])+"\t"+str(l1By[i])+"\t"+str(l1Byer[i])+"\n") 
for i in np.arange(0,len(r2Bx),1): 
	file.write("R02\t"+str(r2Bx[i])+"\t"+str(r2By[i])+"\t"+str(r2Byer[i])+"\n") 
file.close() 


l1Bx, l1Bxer, l1By, l1Byer =  Profiled(eng_bins, binN, lMCe, lo1beta, lweight)
r2Bx, r2Bxer, r2By, r2Byer =  Profiled(eng_bins, binN, r2MCe, ro2beta, r2weight)
pylab.figure()
plt.hist2d(r2MCe, ro2beta, bins=75, norm=LogNorm(),weights=r2weight)
plt.errorbar(r2Bx, r2By, yerr=r2Byer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$\beta$")
pylab.title("Combo")
pylab.ylim([0,10])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_ro2BetavE.png")
pylab.close()
pylab.figure()
plt.hist2d(lMCe, lo1beta, bins=75, norm=LogNorm(),weights=lweight)
plt.errorbar(l1Bx, l1By, yerr=l1Byer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$\beta$")
pylab.title("Laputop")
pylab.ylim([0,10])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_lo1BetavE.png")
pylab.close()
pylab.figure()
plt.errorbar(r2Bx, r2By, yerr=r2Byer, fmt='r-',capsize=5)
plt.errorbar(l1Bx, l1By, yerr=l1Byer, fmt='g-',capsize=5)
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$\beta$")
pylab.ylim([0,10])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_compBetavE.png")
pylab.close()
# test here to write file on Beta
file = open(txtdir+"_BetavE.txt","w")
for i in np.arange(0,len(l1Bx),1): 
	 file.write("L01\t"+str(l1Bx[i])+"\t"+str(l1By[i])+"\t"+str(l1Byer[i])+"\n") 
for i in np.arange(0,len(r2Bx),1): 
	file.write("R02\t"+str(r2Bx[i])+"\t"+str(r2By[i])+"\t"+str(r2Byer[i])+"\n") 
file.close() 






l1SRx, l1SRxer, l1SRy, l1SRyer =  Profiled(eng_bins, binN, lMCe, lo1S125, lweight)
r2SRx, r2SRxer, r2SRy, r2SRyer =  Profiled(eng_bins, binN, r2MCe, ro2S125, r2weight)
pylab.figure()
plt.hist2d(r2MCe, ro2S125, bins=75, norm=LogNorm(),weights=r2weight)
plt.errorbar(r2SRx, r2SRy, yerr=r2SRyer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$\log_{10}(S_{125}/[VEM])$")
pylab.title("Combo")
#pylab.ylim([-1,4])
pylab.ylim([-1,5])
plt.grid(True,which="both",ls="-")
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_ro2S125vE.png")
pylab.close()
pylab.figure()
plt.hist2d(lMCe, lo1S125, bins=75, norm=LogNorm(),weights=lweight)
plt.errorbar(l1SRx, l1SRy, yerr=l1SRyer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$\log_{10}(S_{125}/[VEM])$")
pylab.title("Laputop")
pylab.ylim([-1,4])
#pylab.ylim([0,10])
plt.grid(True,which="both",ls="-")
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_lo1S125vE.png")
pylab.close()
pylab.figure()
plt.errorbar(r2SRx, r2SRy, yerr=r2SRyer, fmt='r-',capsize=5)
plt.errorbar(l1SRx, l1SRy, yerr=l1SRyer, fmt='g-',capsize=5)
#pylab.legend(["Combined","Laputop"],loc=2)
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$\log_{10}(S_{125}/[VEM])$")
#pylab.ylim([0,10])
#pylab.ylim([-1,6])
plt.grid(True,which="both",ls="-")
pylab.ylim([-1,4])
pylab.xlim([6,9.5])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_compS125vE.png")
pylab.close()
# test here to write file on S125
file = open(txtdir+"_logS125vE.txt","w")
for i in np.arange(0,len(l1SRx),1): 
	file.write("L01\t"+str(l1SRx[i])+"\t"+str(l1SRy[i])+"\t"+str(l1SRyer[i])+"\n") 
for i in np.arange(0,len(r2SRx),1): 
	file.write("R02\t"+str(r2SRx[i])+"\t"+str(r2SRy[i])+"\t"+str(r2SRyer[i])+"\n") 
file.close() 
l1SRx, l1SRxer, l1SRy, l1SRyer =  Profiled(eng_bins, binN, lMCe, lo1S125nl, lweight)
r2SRx, r2SRxer, r2SRy, r2SRyer =  Profiled(eng_bins, binN, r2MCe, ro2S125nl, r2weight)
file = open(txtdir+"_S125vE.txt","w")
for i in np.arange(0,len(l1SRx),1): 
	file.write("L01\t"+str(l1SRx[i])+"\t"+str(l1SRy[i])+"\t"+str(l1SRyer[i])+"\n") 
for i in np.arange(0,len(r2SRx),1): 
	file.write("R02\t"+str(r2SRx[i])+"\t"+str(r2SRy[i])+"\t"+str(r2SRyer[i])+"\n") 
file.close() 













r2Ax, r2Axer, r2Ay, r2Ayer =  Profiled(eng_bins, binN, r2MCe, ro2amp, r2weight)
pylab.figure()
plt.errorbar(r2Ax, r2Ay, yerr=r2Ayer, fmt='ro',capsize=5)
plt.hist2d(r2MCe, ro2amp, bins=200, norm=LogNorm(),weights=r2weight)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$c_{t}[ns/m^{2}$")
pylab.ylim([0,0.0025])
#plt.grid(True,which="both",ls="-")
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_ro2AmpvE.png")
pylab.close()
# test here to write file on Amp
file = open(txtdir+"_AmpvE.txt","w")
for i in np.arange(0,len(r2Ax),1): 
	file.write("R02\t"+str(r2Ax[i])+"\t"+str(r2Ay[i])+"\t"+str(r2Ayer[i])+"\n") 
file.close() 


s125 = np.arange(0,5,0.2)

r2Bx, r2Bxer, r2By, r2Byer =  Profiled(s125_bins, binN, ro2S125, ro2amp, r2weight)
pylab.figure()
plt.hist2d(ro2S125, ro2amp, bins=75, norm=LogNorm(),weights=r2weight)
plt.errorbar(r2Bx, r2By, yerr=r2Byer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$c_{t}[ns/m^{2}$")
pylab.title("Combo")
pylab.ylim([0,10])
pylab.xlim([0,5])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_ro2AMPvS125.png")
pylab.close()
# test here to write file on Beta
file = open(txtdir+"_AMPvS125.txt","w")
for i in np.arange(0,len(r2Bx),1): 
	file.write("R02\t"+str(r2Bx[i])+"\t"+str(r2By[i])+"\t"+str(r2Byer[i])+"\n") 
file.close() 














print "II Params Profiles"
r215x, r215xer, r215y, r215yer =  Profiled(eng_bins, binN, m_r2MCe, m_mass_stoch, m_r2weight)
r115x, r115xer, r115y, r115yer =  Profiled(eng_bins, binN, o_r1MCe, o_mass_stoch, o_r1weight)
pylab.figure()
plt.hist2d(m_r2MCe, m_mass_stoch, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r215x, r215y, yerr=r215yer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$\frac{dE}{dX}(X)|_{X=1500m}[GeV/m]$")
pylab.title("Combo")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,10000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_1500_stoch.png")
pylab.close()
pylab.figure()
plt.hist2d(o_r1MCe, o_mass_stoch, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r115x, r115y, yerr=r115yer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$\frac{dE}{dX}(X)|_{X=1500m}[GeV/m]$")
pylab.title("InIce")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,10000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_lo1_1500_stoch.png")
pylab.close()
pylab.figure()
plt.errorbar(r215x, r215y, yerr=r215yer, fmt='r-',capsize=5)
plt.errorbar(r115x, r115y, yerr=r115yer, fmt='b-',capsize=5)
pylab.legend(["Combined","InIce"],loc=2)
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$\frac{dE}{dX}(X)|_{X=1500m}[GeV/m]$")
#pylab.ylim([2.5,4.5])
pylab.ylim([1,10000])
pylab.yscale('log')
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_comp_1500_stoch.png")
pylab.close()
file = open(txtdir+"_Stoch1500vE.txt","w")
for i in np.arange(0,len(r115x),1): 
	 file.write("R01\t"+str(r115x[i])+"\t"+str(r115y[i])+"\t"+str(r115yer[i])+"\n") 
for i in np.arange(0,len(r215x),1): 
	 file.write("R02\t"+str(r215x[i])+"\t"+str(r215y[i])+"\t"+str(r215yer[i])+"\n") 
file.close() 



r2NHx, r2NHxer, r2NHy, r2NHyer =  Profiled(eng_bins, binN, m_r2MCe, m_nhe_stoch, m_r2weight)
r1NHx, r1NHxer, r1NHy, r1NHyer =  Profiled(eng_bins, binN, o_r1MCe, o_nhe_stoch, o_r1weight)
pylab.figure()
plt.hist2d(m_r2MCe, m_nhe_stoch, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r2NHx, r2NHy, yerr=r2NHyer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$No. of HE Stochastic Hits$")
pylab.title("Combo")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,16])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_NHEvE_stoch.png")
pylab.close()
pylab.figure()
plt.hist2d(o_r1MCe, o_nhe_stoch, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r1NHx, r1NHy, yerr=r1NHyer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$No. of HE Stochastic Hits$")
pylab.title("InIce")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,16])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_lo1_NHEvE_stoch.png")
pylab.close()
pylab.figure()
plt.errorbar(r2NHx, r2NHy, yerr=r2NHyer, fmt='r-',capsize=5)
plt.errorbar(r1NHx, r1NHy, yerr=r1NHyer, fmt='b-',capsize=5)
pylab.legend(["Combined","InIce"],loc=2)
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$No. of HE Stochastic Hits$")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,16])
#pylab.yscale('log')
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_comp_NHEvE_stoch.png")
pylab.close()
file = open(txtdir+"_NHEvE_stoch.txt","w")
for i in np.arange(0,len(r1NHx),1): 
	 file.write("R01\t"+str(r1NHx[i])+"\t"+str(r1NHy[i])+"\t"+str(r1NHyer[i])+"\n") 
for i in np.arange(0,len(r2NHx),1): 
	 file.write("R02\t"+str(r2NHx[i])+"\t"+str(r2NHy[i])+"\t"+str(r2NHyer[i])+"\n") 
file.close() 






r215x, r215xer, r215y, r215yer =  Profiled(eng_bins, binN, m_r2MCe, m_mass_stoch2, m_r2weight)
r115x, r115xer, r115y, r115yer =  Profiled(eng_bins, binN, o_r1MCe, o_mass_stoch2, o_r1weight)
pylab.figure()
plt.hist2d(m_r2MCe, m_mass_stoch2, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r215x, r215y, yerr=r215yer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$\frac{dE}{dX}(X)|_{X=1500m}[GeV/m]$")
pylab.title("Combo")
#pylab.ylim([2.5,4.5])
plt.grid(True,which="both",ls="-")
pylab.ylim([0,10000])
pylab.savefig(figdir+"_r02_1500vE_stoch2.png")
pylab.close()
pylab.figure()
plt.hist2d(o_r1MCe, o_mass_stoch2, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r115x, r115y, yerr=r115yer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$\frac{dE}{dX}(X)|_{X=1500m}[GeV/m]$")
pylab.title("InIce")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,10000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_lo1_1500vE_stoch2.png")
pylab.close()
pylab.figure()
plt.errorbar(r215x, r215y, yerr=r215yer, fmt='r-',capsize=5)
plt.errorbar(r115x, r115y, yerr=r115yer, fmt='b-',capsize=5)
pylab.legend(["Combined","InIce"],loc=2)
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$\frac{dE}{dX}(X)|_{X=1500m}[GeV/m]$")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,10000])
pylab.yscale('log')
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_comp_1500vE_stoch2.png")
pylab.close()
file = open(txtdir+"_1500vE_stoch2.txt","w")
for i in np.arange(0,len(r115x),1): 
	 file.write("R01\t"+str(r115x[i])+"\t"+str(r115y[i])+"\t"+str(r115yer[i])+"\n") 
for i in np.arange(0,len(r215x),1): 
	 file.write("R02\t"+str(r215x[i])+"\t"+str(r215y[i])+"\t"+str(r215yer[i])+"\n") 
file.close() 


r2NHx, r2NHxer, r2NHy, r2NHyer =  Profiled(eng_bins, binN, m_r2MCe, m_nhe_stoch2, m_r2weight)
r1NHx, r1NHxer, r1NHy, r1NHyer =  Profiled(eng_bins, binN, o_r1MCe, o_nhe_stoch2, o_r1weight)
pylab.figure()
plt.hist2d(m_r2MCe, m_nhe_stoch2, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r2NHx, r2NHy, yerr=r2NHyer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$No. of HE Stochastic Hits$")
pylab.title("Combo")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,5])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_NHEvE_stoch2.png")
pylab.close()
pylab.figure()
plt.hist2d(o_r1MCe, o_nhe_stoch2, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r1NHx, r1NHy, yerr=r1NHyer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.ylabel(r"$No. of HE Stochastic Hits$")
pylab.title("InIce")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,5])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_ro1_NHEvE_stoch2.png")
pylab.close()
file = open(txtdir+"_NHEvE_stoch2.txt","w")

for i in np.arange(0,len(r1NHx),1): 
	 file.write("R01\t"+str(r1NHx[i])+"\t"+str(r1NHy[i])+"\t"+str(r1NHyer[i])+"\n") 
for i in np.arange(0,len(r2NHx),1): 
	 file.write("R02\t"+str(r2NHx[i])+"\t"+str(r2NHy[i])+"\t"+str(r2NHyer[i])+"\n") 
file.close()



"""

r215x, r215xer, r215y, r215yer =  Profiled(s125_bins, binN, ro2S125, m_mass_stoch2, m_r2weight)
r115x, r115xer, r115y, r115yer =  Profiled(s125_bins, binN, lo1S125, o_mass_stoch2, o_r1weight)
pylab.figure()
plt.hist2d(ro2S125, m_mass_stoch2, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r215x, r215y, yerr=r215yer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$\frac{dE}{dX}(X)|_{X=1500m}[GeV/m]$")
pylab.title("Combo")
#pylab.ylim([2.5,4.5])
pylab.xlim([0,5])
pylab.ylim([0,10000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_1500_stoch2.png")
pylab.close()
pylab.figure()
plt.hist2d(lo1S125, o_mass_stoch2, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r115x, r115y, yerr=r115yer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$\frac{dE}{dX}(X)|_{X=1500m}[GeV/m]$")
pylab.title("InIce")
#pylab.ylim([2.5,4.5])
pylab.xlim([0,5])
pylab.ylim([0,10000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_lo1_1500vS125_stoch2.png")
pylab.close()
pylab.figure()
plt.errorbar(r215x, r215y, yerr=r215yer, fmt='r-',capsize=5)
plt.errorbar(r115x, r115y, yerr=r115yer, fmt='b-',capsize=5)
pylab.legend(["Combined","InIce"],loc=2)
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$\frac{dE}{dX}(X)|_{X=1500m}[GeV/m]$")
#pylab.ylim([2.5,4.5])
pylab.xlim([0,5])
pylab.ylim([1,10000])
pylab.yscale('log')
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_comp_1500vS125_stoch2.png")
pylab.close()
file = open(txtdir+"_Stoch1500vS125.txt","w")
for i in np.arange(0,len(r115x),1): 
	 file.write("R01\t"+str(r115x[i])+"\t"+str(r115y[i])+"\t"+str(r115yer[i])+"\n") 
for i in np.arange(0,len(r215x),1): 
	 file.write("R02\t"+str(r215x[i])+"\t"+str(r215y[i])+"\t"+str(r215yer[i])+"\n") 
file.close() 

r2NHx, r2NHxer, r2NHy, r2NHyer =  Profiled(s125_bins, binN, ro2S125, m_nhe_stoch2, m_r2weight)
r1NHx, r1NHxer, r1NHy, r1NHyer =  Profiled(s125_bins, binN, lo1S125, o_nhe_stoch2, o_r1weight)
pylab.figure()
plt.hist2d(ro2S125, m_nhe_stoch2, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r2NHx, r2NHy, yerr=r2NHyer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$No. of HE Stochastic Hits$")
pylab.title("Combo")
pylab.xlim([0,5])
#pylab.ylim([2.5,4.5])
pylab.ylim([0,16])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_NHEvES125_stoch2.png")
pylab.close()
pylab.figure()
plt.hist2d(lo1S125, o_nhe_stoch2, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r1NHx, r1NHy, yerr=r1NHyer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$No. of HE Stochastic Hits$")
pylab.title("InIce")
pylab.xlim([0,5])
#pylab.ylim([2.5,4.5])
pylab.ylim([0,16])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_lo1_NHEvS125_stoch2.png")
pylab.close()
pylab.figure()
plt.errorbar(r2NHx, r2NHy, yerr=r2NHyer, fmt='r-',capsize=5)
plt.errorbar(r1NHx, r1NHy, yerr=r1NHyer, fmt='b-',capsize=5)
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$No. of HE Stochastic Hits$")
pylab.xlim([0,5])
#pylab.ylim([2.5,4.5])
pylab.ylim([0,16])
#pylab.yscale('log')
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_comp_NHEvS125_stoch2.png")
pylab.close()
file = open(txtdir+"_NHEvS125_stoch2.txt","w")
for i in np.arange(0,len(r1NHx),1): 
	 file.write("R01\t"+str(r1NHx[i])+"\t"+str(r1NHy[i])+"\t"+str(r1NHyer[i])+"\n") 
for i in np.arange(0,len(r2NHx),1): 
	 file.write("R02\t"+str(r2NHx[i])+"\t"+str(r2NHy[i])+"\t"+str(r2NHyer[i])+"\n") 
file.close() 































r215x, r215xer, r215y, r215yer =  Profiled(s125_bins, binN, ro2S125, m_mass_stoch, m_r2weight)
r115x, r115xer, r115y, r115yer =  Profiled(s125_bins, binN, lo1S125, o_mass_stoch, o_r1weight)
pylab.figure()
plt.hist2d(ro2S125, m_mass_stoch, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r215x, r215y, yerr=r215yer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$\frac{dE}{dX}(X)|_{X=1500m}[GeV/m]$")
pylab.title("Combo")
pylab.xlim([0,5])
#pylab.ylim([2.5,4.5])
pylab.ylim([0,10000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_1500_stoch.png")
pylab.close()
pylab.figure()
plt.hist2d(lo1S125, o_mass_stoch, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r115x, r115y, yerr=r115yer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$\frac{dE}{dX}(X)|_{X=1500m}[GeV/m]$")
pylab.title("InIce")
pylab.xlim([0,5])
#pylab.ylim([2.5,4.5])
pylab.ylim([0,10000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_lo1_1500vS125_stoch.png")
pylab.close()
pylab.figure()
plt.errorbar(r215x, r215y, yerr=r215yer, fmt='r-',capsize=5)
plt.errorbar(r115x, r115y, yerr=r115yer, fmt='b-',capsize=5)
pylab.legend(["Combined","InIce"],loc=2)
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$\frac{dE}{dX}(X)|_{X=1500m}[GeV/m]$")
pylab.xlim([0,5])
#pylab.ylim([2.5,4.5])
pylab.ylim([1,10000])
pylab.yscale('log')
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_comp_1500vS125_stoch.png")
pylab.close()
file = open(txtdir+"_Stoch1500vS125.txt","w")
for i in np.arange(0,len(r115x),1): 
	 file.write("R01\t"+str(r115x[i])+"\t"+str(r115y[i])+"\t"+str(r115yer[i])+"\n") 
for i in np.arange(0,len(r215x),1): 
	 file.write("R02\t"+str(r215x[i])+"\t"+str(r215y[i])+"\t"+str(r215yer[i])+"\n") 
file.close() 

r2NHx, r2NHxer, r2NHy, r2NHyer =  Profiled(s125_bins, binN, ro2S125, m_nhe_stoch, m_r2weight)
r1NHx, r1NHxer, r1NHy, r1NHyer =  Profiled(s125_bins, binN, lo1S125, o_nhe_stoch, o_r1weight)
pylab.figure()
plt.hist2d(ro2S125, m_nhe_stoch, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r2NHx, r2NHy, yerr=r2NHyer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$No. of HE Stochastic Hits$")
pylab.title("Combo")
#pylab.ylim([2.5,4.5])
pylab.xlim([0,5])
pylab.ylim([0,16])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_NHEvS125_stoch.png")
pylab.close()
pylab.figure()
plt.hist2d(lo1S125, o_nhe_stoch, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r1NHx, r1NHy, yerr=r1NHyer, fmt='ro',capsize=5)
plt.colorbar()
pylab.xlabel(r"$\log_{10}(E_{pri,true}/[GeV])$")
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.title("InIce")
#pylab.ylim([2.5,4.5])
pylab.xlim([0,5])
pylab.ylim([0,16])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_lo1_NHEvS125_stoch.png")
pylab.close()
pylab.figure()
plt.errorbar(r2NHx, r2NHy, yerr=r2NHyer, fmt='r-',capsize=5)
plt.errorbar(r1NHx, r1NHy, yerr=r1NHyer, fmt='b-',capsize=5)
#pylab.legend(["Combined","InIce"],loc=2)
pylab.xlabel(r"$\log_{10}(S_{ref}/[VEM])$")
pylab.ylabel(r"$No. of HE Stochastic Hits$")
#pylab.ylim([2.5,4.5])
pylab.xlim([0,5])
pylab.ylim([0,16])
#pylab.yscale('log')
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_comp_NHEvS125_stoch.png")
pylab.close()
file = open(txtdir+"_NHEvS125_stoch.txt","w")
for i in np.arange(0,len(r1NHx),1): 
	 file.write("R01\t"+str(r1NHx[i])+"\t"+str(r1NHy[i])+"\t"+str(r1NHyer[i])+"\n") 
for i in np.arange(0,len(r2NHx),1): 
	 file.write("R02\t"+str(r2NHx[i])+"\t"+str(r2NHy[i])+"\t"+str(r2NHyer[i])+"\n") 
file.close() 












"""





















r215x, r215xer, r215y, r215yer =  Profiled(eng_bins, binN, r2MCe, m_dedx_3, m_r2weight)
r115x, r115xer, r115y, r115yer =  Profiled(eng_bins, binN, r1MCe, o_dedx_3, o_r1weight)
r2n5x, r2n5xer, r2n5y, r2n5yer =  Profiled(eng_bins, binN, r2MCe, m_dedx_n, m_r2weight)
r1n5x, r1n5xer, r1n5y, r1n5yer =  Profiled(eng_bins, binN, r1MCe, o_dedx_n, o_r1weight)


print r2MCe
print m_dedx_3
print m_r2weight
pylab.figure()
plt.hist2d(r2MCe, m_dedx_3, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r215x, r215y, yerr=r215yer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
pylab.ylabel("dE/dX @ 1500m")
pylab.title("Combo")
#pylab.ylim([2.5,4.5])
#pylab.ylim([0,10000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_1500_3.png")
pylab.close()
pylab.figure()
plt.hist2d(r1MCe, o_dedx_3, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r115x, r115y, yerr=r115yer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
pylab.ylabel("dE/dX @ 1500m")
pylab.title("InIce")
#pylab.ylim([2.5,4.5])
#pylab.ylim([0,10000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_ro1_1500_3.png")
pylab.close()


pylab.figure()
plt.hist2d(r2MCe, m_dedx_n, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r2n5x, r2n5y, yerr=r2n5yer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
pylab.ylabel("dE/dX @ 1500m")
pylab.title("Combo")
#pylab.ylim([2.5,4.5])
#pylab.ylim([0,10000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_1500_n.png")
pylab.close()
pylab.figure()
plt.hist2d(r1MCe, o_dedx_n, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r1n5x, r1n5y, yerr=r1n5yer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
pylab.ylabel("dE/dX @ 1500m")
pylab.title("InIce")
#pylab.ylim([2.5,4.5])
#pylab.ylim([0,10000])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_ro1_1500_n.png")
pylab.close()








pylab.figure()
plt.errorbar(r215x, r215y, yerr=r215yer, fmt='r-')
plt.errorbar(r115x, r115y, yerr=r115yer, fmt='b-')
plt.errorbar(r2n5x, r2n5y, yerr=r2n5yer, fmt='r--')
plt.errorbar(r1n5x, r1n5y, yerr=r1n5yer, fmt='b--')
pylab.legend(["3D","II-only","Truth"],loc=2)
pylab.xlabel("log10(True Energy/[GeV])")
pylab.ylabel("dE/dX @ 1500m")
#pylab.ylim([2.5,4.5])
#pylab.ylim([1,10000])
#pylab.yscale('log')
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_comp_1500_3.png")
pylab.close()
file = open(txtdir+"_comp_1500_3N.txt","w")
for i in np.arange(0,len(r115x),1):
        file.write("R01\t"+str(r115x[i])+"\t"+str(r115y[i])+"\t"+str(r115yer[i])+"\n")
for i in np.arange(0,len(r215x),1):
        file.write("R02\t"+str(r215x[i])+"\t"+str(r215y[i])+"\t"+str(r215yer[i])+"\n")
file.close()

file = open(txtdir+"_comp_1500_3n.txt","w")
for i in np.arange(0,len(r1n5x),1):
        file.write("R01\t"+str(r1n5x[i])+"\t"+str(r1n5y[i])+"\t"+str(r1n5yer[i])+"\n")
for i in np.arange(0,len(r2n5x),1):
        file.write("R02\t"+str(r2n5x[i])+"\t"+str(r2n5y[i])+"\t"+str(r2n5yer[i])+"\n")
file.close()







r24Hx, r24Hxer, r24Hy, r24Hyer =  Profiled(eng_bins, binN, r2MCe, m_nhe_4, m_r2weight)
r14Hx, r14Hxer, r14Hy, r14Hyer =  Profiled(eng_bins, binN, r1MCe, o_nhe_4, o_r1weight)
r2NHx, r2NHxer, r2NHy, r2NHyer =  Profiled(eng_bins, binN, r2MCe, m_nhe_3, m_r2weight)
r1NHx, r1NHxer, r1NHy, r1NHyer =  Profiled(eng_bins, binN, r1MCe, o_nhe_3, o_r1weight)
r2nHx, r2nHxer, r2nHy, r2nHyer =  Profiled(eng_bins, binN, r2MCe, m_nhe_n, m_r2weight)
r1nHx, r1nHxer, r1nHy, r1nHyer =  Profiled(eng_bins, binN, r1MCe, o_nhe_n, o_r1weight)



pylab.figure()
plt.hist2d(r2MCe, m_nhe_4, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r24Hx, r24Hy, yerr=r24Hyer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
pylab.ylabel(r"$NHE_{strong}$")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,20])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_nhe_4.png")
pylab.close()
pylab.figure()
plt.hist2d(r1MCe, o_nhe_4, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r14Hx, r14Hy, yerr=r14Hyer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
pylab.ylabel(r"$NHE_{strong}$")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,20])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_ro1_nhe_4.png")
pylab.close()


pylab.figure()
plt.hist2d(r2MCe, m_nhe_3, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r2NHx, r2NHy, yerr=r2NHyer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
pylab.ylabel(r"$NHE_{std}$")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,20])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_nhe_3.png")
pylab.close()
pylab.figure()
plt.hist2d(r1MCe, o_nhe_3, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r1NHx, r1NHy, yerr=r1NHyer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
pylab.ylabel(r"$NHE_{std}$")
pylab.title("InIce")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,20])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_ro1_nhe_3.png")
pylab.close()





pylab.figure()
plt.hist2d(r2MCe, m_nhe_n, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r2nHx, r2nHy, yerr=r2nHyer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
pylab.ylabel(r"$NHE_{\delta E}$")
pylab.title("Combo")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,20])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_nhe_n.png")
pylab.close()
pylab.figure()
plt.hist2d(r1MCe, o_nhe_n, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r1nHx, r1nHy, yerr=r1nHyer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
pylab.ylabel(r"$NHE_{\delta E}$")
pylab.title("InIce")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,20])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_ro1_nhe_n.png")
pylab.close()









pylab.figure()
plt.errorbar(r24Hx, r24Hy, yerr=r24Hyer, fmt='r:')
plt.errorbar(r14Hx, r14Hy, yerr=r14Hyer, fmt='b:')
plt.errorbar(r2NHx, r2NHy, yerr=r2NHyer, fmt='r-')
plt.errorbar(r1NHx, r1NHy, yerr=r1NHyer, fmt='b-')
plt.errorbar(r2nHx, r2nHy, yerr=r2nHyer, fmt='r--')
plt.errorbar(r1nHx, r1nHy, yerr=r1nHyer, fmt='b--')
pylab.legend(["3D","II-only","Truth"],loc=2)
pylab.xlabel("log10(True Energy/[GeV])")
pylab.ylabel("NHE")
#pylab.ylim([2.5,4.5])
pylab.ylim([0,20])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_comp_nhe_3.png")
pylab.close()
file = open(txtdir+"_comp_nhe_34.txt","w")
for i in np.arange(0,len(r14Hx),1):
        file.write("R01\t"+str(r14Hx[i])+"\t"+str(r14Hy[i])+"\t"+str(r14Hyer[i])+"\n")
for i in np.arange(0,len(r24Hx),1):
        file.write("R02\t"+str(r24Hx[i])+"\t"+str(r24Hy[i])+"\t"+str(r24Hyer[i])+"\n")
file.close()

file = open(txtdir+"_comp_nhe_3N.txt","w")
for i in np.arange(0,len(r1NHx),1):
        file.write("R01\t"+str(r1NHx[i])+"\t"+str(r1NHy[i])+"\t"+str(r1NHyer[i])+"\n")
for i in np.arange(0,len(r2NHx),1):
        file.write("R02\t"+str(r2NHx[i])+"\t"+str(r2NHy[i])+"\t"+str(r2NHyer[i])+"\n")
file.close()

file = open(txtdir+"_comp_nhe_3n.txt","w")
for i in np.arange(0,len(r1nHx),1):
        file.write("R01\t"+str(r1nHx[i])+"\t"+str(r1nHy[i])+"\t"+str(r1nHyer[i])+"\n")
for i in np.arange(0,len(r2nHx),1):
        file.write("R02\t"+str(r2nHx[i])+"\t"+str(r2nHy[i])+"\t"+str(r2nHyer[i])+"\n")
file.close()


r2NEx, r2NExer, r2NEy, r2NEyer =  Profiled(eng_bins, binN, r2MCe, m_eng_3, m_r2weight)
r1NEx, r1NExer, r1NEy, r1NEyer =  Profiled(eng_bins, binN, r1MCe, o_eng_3, o_r1weight)
r2nEx, r2nExer, r2nEy, r2nEyer =  Profiled(eng_bins, binN, r2MCe, m_eng_n, m_r2weight)
r1nEx, r1nExer, r1nEy, r1nEyer =  Profiled(eng_bins, binN, r1MCe, o_eng_n, o_r1weight)




pylab.figure()
plt.hist2d(r2MCe, m_eng_3, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r2NEx, r2NEy, yerr=r2NEyer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
#pylab.ylabel("NHE")
pylab.title("Combo")
#pylab.yscale('log')
pylab.ylim([5.5,10.])
pylab.xlim([5.5,10.])
#pylab.ylim([0,16])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_eng_3.png")
pylab.close()
pylab.figure()
plt.hist2d(r1MCe, o_eng_3, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r1NEx, r1NEy, yerr=r1NEyer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
#pylab.yscale('log')
#pylab.ylabel("NHE")
pylab.title("InIce")
pylab.ylim([5.5,10.])
pylab.xlim([5.5,10.])
#pylab.ylim([2.5,4.5])
#pylab.ylim([0,16])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_ro1_eng_3.png")
pylab.close()





pylab.figure()
plt.hist2d(r2MCe, m_eng_n, bins=75, norm=LogNorm(),weights=m_r2weight)
plt.errorbar(r2nEx, r2nEy, yerr=r2nEyer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
#pylab.ylabel("NHE")
pylab.title("Combo")
#pylab.yscale('log')
#pylab.ylim([2.5,4.5])
#pylab.ylim([0,16])
pylab.ylim([5.5,10.])
pylab.xlim([5.5,10.])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_r02_eng_n.png")
pylab.close()
pylab.figure()
plt.hist2d(r1MCe, o_eng_n, bins=75, norm=LogNorm(),weights=o_r1weight)
plt.errorbar(r1nEx, r1nEy, yerr=r1nEyer, fmt='ro')
plt.colorbar()
pylab.xlabel("log10(True Energy/[GeV])")
#pylab.ylabel("NHE")
#pylab.yscale('log')
pylab.title("InIce")
#pylab.ylim([2.5,4.5])
#pylab.ylim([0,16])
pylab.ylim([5.5,10.])
pylab.xlim([5.5,10.])
plt.grid(True,which="both",ls="-")
#pylab.yscale('log')
pylab.savefig(figdir+"_ro1_eng_n.png")
pylab.close()






pylab.figure()
plt.errorbar(r2NEx, r2NEy, yerr=r2NEyer, fmt='r-')
plt.errorbar(r1NEx, r1NEy, yerr=r1NEyer, fmt='b-')
plt.errorbar(r2nEx, r2nEy, yerr=r2nEyer, fmt='r--')
plt.errorbar(r1nEx, r1nEy, yerr=r1nEyer, fmt='b--')
pylab.legend(["3D","II-only","Truth"],loc=2)
pylab.xlabel("log10(True Energy/[GeV])")
#pylab.ylabel("NHE")
#pylab.ylim([2.5,4.5])
#pylab.yscale('log')
#pylab.ylim([0,16])
##pylab.yscale('log')
pylab.ylim([5.5,10.])
pylab.xlim([5.5,10.])
plt.grid(True,which="both",ls="-")
pylab.savefig(figdir+"_comp_eng_3.png")
pylab.close()
file = open(txtdir+"_comp_eng_3N.txt","w")
for i in np.arange(0,len(r1NEx),1):
        file.write("R01\t"+str(r1NEx[i])+"\t"+str(r1NEy[i])+"\t"+str(r1NEyer[i])+"\n")
for i in np.arange(0,len(r2NEx),1):
        file.write("R02\t"+str(r2NEx[i])+"\t"+str(r2NEy[i])+"\t"+str(r2NEyer[i])+"\n")
file.close()

file = open(txtdir+"_comp_eng_3n.txt","w")
for i in np.arange(0,len(r1nEx),1):
        file.write("R01\t"+str(r1nEx[i])+"\t"+str(r1nEy[i])+"\t"+str(r1nEyer[i])+"\n")
for i in np.arange(0,len(r2nEx),1):
        file.write("R02\t"+str(r2nEx[i])+"\t"+str(r2nEy[i])+"\t"+str(r2nEyer[i])+"\n")
file.close()









