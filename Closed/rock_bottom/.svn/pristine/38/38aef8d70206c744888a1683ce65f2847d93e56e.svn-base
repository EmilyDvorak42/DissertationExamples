#!/usr/bin/env python

from icecube import icetray


"""

Description

"""


@icetray.traysegment
def RockBottomTwoLDF(tray, name = 'RockBottom',
					SLCPulses = 'SRTCleanedSLCPulses',
					HLCPulses = 'SRTCleanedHLCPulses',
					NIterations = 1,
					emLDF = 'dlp',
					OutputName = 'RockBottomTwoLDF',
					SnowService = 'SimpleSnow'
					):
					
	from icecube import dataclasses, gulliver, gulliver_modules, lilliput, rock_bottom, phys_services
	from icecube.icetray import I3Units
	import math, sys, numpy
	from icecube.rock_bottom.modules.WriteSeed import WriteSeed
	
	pi = numpy.pi	
	
	
	""" Configure signal models """
	
	if emLDF == 'dlp':
		ldf = rock_bottom.ldf.LogLog()
	elif emLDF == 'nkg':
		ldf = rock_bottom.ldf.NKG()
	else:
		print('Sorry, unknown e.m. LDF...')
		print('exit')
		sys.exit()
		
	muonldf = rock_bottom.ldf.MuonLDF()
	curvy = rock_bottom.ldf.Curvy()
	laputop_ltp = rock_bottom.functions.I3LaputopTriggerProbability()
	
	tray.AddService('LaputopSignalModel', name+'_LaputopSignalModel',
					LDF=loglog,
					LTP=laputop_ltp,
					SnowService = SnowService,
					use_top_sigma = True
					)

	tray.AddService('TwoLDFSignalModel', name+'_TwoLDFSignalModel',
					TankResponseTablesDir = '/home/jgonzalez/tank_response',
					SnowService = SnowService,
					ZenithDependence = True,
					emLDF = ldf,
					muLDF = muonldf)
	
	
	""" Configure minimizer """

	tray.AddService("I3GulliverMinuitFactory", name+"_Minuit",
					MinuitPrintLevel = -2,
					FlatnessCheck = True,
					Algorithm = "SIMPLEX",
					MaxIterations = 2500,
					MinuitStrategy = 2,
					Tolerance = 0.01)
	
	
	""" Configure likelihoods """
				
	tray.AddService('I3TopLDFLikelihoodFactory', name+'_TwoLDFLLH',
					Model=name+'_TwoLDFSignalModel',
					HLCPulses=HLCPulses,
					SLCPulses=SLCPulses,
					SaturatedPulses='',
					IgnoreTanks='',
					UseSilent = True,
					UseSLCPulses = True,
					MinSignal = 0.7
					)
					
	tray.AddService('I3CurveLikelihoodFactory', name+'_CurveLLH',
					Model=name+'_LaputopSignalModel',
					#Model='TwoLDFSignalModel',
					HLCPulses=HLCPulses,
					SaturatedPulses='',
					IgnoreTanks='',
					Toprec = True,
					MinSignal = 0.7
					)
	
					
	""" Configure seed service """
	
	tray.AddModule(WriteSeed, name+'_WriteSeed',
				ShowerCOG='ShowerCOG',
				ShowerPlane='ShowerPlane',
				OutputName=name+'_SimpleSeed'
				)
				
	tray.AddService("I3ComboSeedServiceFactory", name+"_SimpleSeeder",
					FirstGuesses=[ name+'_SimpleSeed' ],
					HLCPulses = HLCPulses,
					SLCPulses = SLCPulses,
					SignalModel=name+'_TwoLDFSignalModel',
					Beta = 2.6,
					RhoMu = 1.0,
					TimeShiftType="TFirst"
					)
				
				
	""" Configure parametrizations """
	
	tray.AddService("I3ComboParametrizationFactory", name+"_TwoLDFParams",
					StepT=5.0*I3Units.ns,
					StepX=1.0*I3Units.m,
					StepY=1.0*I3Units.m,
					StepZ=1.0*I3Units.m,
					StepZenith=0.01*I3Units.radian,
					StepAzimuth=0.02*I3Units.radian,
					StepLogE=0.1,
					RelativeBoundsT=[-400.*I3Units.ns,+400.*I3Units.ns],
					BoundsZenith=[0.0*I3Units.radian,+0.5*pi*I3Units.radian],
					BoundsAzimuth=[0.0*I3Units.radian,+2.*pi*I3Units.radian],
					RelativeBoundsX=[-200.0*I3Units.m,+200.0*I3Units.m],
					RelativeBoundsY=[-200.0*I3Units.m,+200.0*I3Units.m],
					RelativeBoundsZ=[-20.0*I3Units.m,+20.0*I3Units.m],
					BoundsLogE=[1,11],
					Boundslog10S125=[-1.,6.],
					BoundsBeta=[0.,10.],
					BoundsRhoMu=[0.0,10.],
					Steplog10S125=0.045,
					StepBeta=0.1,
					StepRhoMu=0.01
					)
					
					
	""" Combine likelihoods """
	
	tray.AddService("I3EventLogLikelihoodCombinerFactory", name+"_TwoLDFCombo",
					InputLogLikelihoods = [name+"_TwoLDFLLH",name+"_CurveLLH"],
					Multiplicity = 'Sum',
					RelativeWeights = [1.,1.]
					)
				

	""" Do the fits """
		
	if NIterations==1:
		tray.AddModule("I3SimpleFitter", name+'_TwoLDF',
						SeedService = name+"_SimpleSeeder",
						Parametrization = name+"_TwoLDFParams",
						LogLikelihood = name+"_TwoLDFCombo",
						OutputName = OutputName,
						Minimizer = name+"_Minuit"
						) 
	else:
		tray.AddModule("I3IterativeFitter", name+"_TwoLDF",
						SeedService=name+"_InIceSeeder",
						Parametrization=name+"_TwoLDFParams",
						LogLikelihood=name+"_TwoLDFCombo", 
						Minimizer=name+"_Minuit",
						OutputName=OutputName,
						RandomService="SOBOL",
						NIterations=NIterations
						)	
					

