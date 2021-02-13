#!/usr/bin/env python

from icecube import icetray


"""

Description

"""


@icetray.traysegment
def RockBottomLaputopRedo(tray, name = 'RockBottom', 
						HLCPulses = 'SRTCleanedHLCPulses', 
						OutputName = 'RockBottomLaputopRedo',
						SnowService = 'SimpleSnow'
						):
						
	from icecube import dataclasses, gulliver, gulliver_modules, lilliput, rock_bottom, phys_services
	from icecube.icetray import I3Units
	import math, sys, numpy
	from icecube.rock_bottom.modules.WriteSeed import WriteSeed
	
	pi = numpy.pi	
		       		
		       		
	""" Configure Laputop signal model """
	
	loglog = rock_bottom.ldf.LogLog()
	curvy = rock_bottom.ldf.Curvy()
	laputop_ltp = rock_bottom.functions.I3LaputopTriggerProbability()

	tray.AddService('LaputopSignalModel', name+'_LaputopSignalModel',
					LDF=loglog,
					LTP=laputop_ltp,
					SnowService = SnowService,
					use_top_sigma = True
					)
	
	
	""" Configure minimizer """

	tray.AddService("I3GulliverMinuitFactory", name+"_Minuit",
					MinuitPrintLevel = -2,
					FlatnessCheck = True,
					Algorithm = "SIMPLEX",
					MaxIterations = 2500,
					MinuitStrategy = 2,
					Tolerance = 0.01)
	
	
	""" Configure likelihoods """
				
	tray.AddService('I3TopLDFLikelihoodFactory', name+'_TopLLH',
					Model=name+'_LaputopSignalModel',
					HLCPulses=HLCPulses,
					SaturatedPulses='',
					IgnoreTanks='',
					UseSilent = True,
					MinSignal = 0.7
					)
					
	tray.AddService('I3CurveLikelihoodFactory', name+'_CurveLLH',
					Model=name+'_LaputopSignalModel',
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
					SignalModel=name+'_LaputopSignalModel',
					Beta = 2.6,
					RhoMu = 1.0,
					TimeShiftType="TFirst"
					)
				
				
	""" Configure parametrizations """
	
	tray.AddService("I3ComboParametrizationFactory", name+"_TopParams",
					StepT=5.0*I3Units.ns,
					StepX=1.0*I3Units.m,
					StepY=1.0*I3Units.m,
					StepLogE=0.1,
					StepZenith=0.01*I3Units.radian,
					StepAzimuth=0.02*I3Units.radian,
					RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
					BoundsZenith=[0.0*I3Units.radian,+0.5*pi*I3Units.radian],
					BoundsAzimuth=[0.0*I3Units.radian,+2.*pi*I3Units.radian],
					RelativeBoundsX=[-45.0*I3Units.m,+45.0*I3Units.m],
					RelativeBoundsY=[-45.0*I3Units.m,+45.0*I3Units.m],
					BoundsLogE=[1,11],
					Boundslog10S125=[-1.,6.],
					BoundsBeta=[0.,10.],
					Steplog10S125=0.045,
					StepBeta=0.1,
					)
					
	tray.AddService("I3ComboParametrizationFactory", name+"_TopParams_FixDir",
					StepT=5.0*I3Units.ns,
					StepX=1.0*I3Units.m,
					StepY=1.0*I3Units.m,
					StepLogE=0.1,
					RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
					RelativeBoundsX=[-45.0*I3Units.m,+45.0*I3Units.m],
					RelativeBoundsY=[-45.0*I3Units.m,+45.0*I3Units.m],
					BoundsLogE=[1,11],
					Boundslog10S125=[-1.,6.],
					BoundsBeta=[0.,10.],
					Steplog10S125=0.045,
					StepBeta=0.1,
					)
					
					
	""" Combine likelihoods """
	
	tray.AddService("I3EventLogLikelihoodCombinerFactory", name+"_TopOnlyCombo",
					InputLogLikelihoods = [name+"_TopLLH",name+"_CurveLLH"],
					Multiplicity = 'Sum',
					RelativeWeights = [1.,1.]
					)
				

	""" Do the fits """
		
	tray.AddModule("I3SimpleFitter", name+'_TopOnly',
					SeedService = name+"_SimpleSeeder",
					Parametrization = name+"_TopParams",
					LogLikelihood = name+"_TopOnlyCombo",
					OutputName = OutputName,
					Minimizer = name+"_Minuit"
					) 	
					

