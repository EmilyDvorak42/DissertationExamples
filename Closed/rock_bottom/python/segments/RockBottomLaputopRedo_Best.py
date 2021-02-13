#!/usr/bin/env python

from icecube import icetray


"""

Description

"""


@icetray.traysegment
def RockBottomLaputopRedo(tray, name = 'RockBottom', 
						HLCPulses = 'SRTCleanedHLCPulses', 
						#HLCPulses = icecube.icetop_Level3_scripts.icetop_globals.icetop_HLCseed_clean_hlc_pulses, 
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
	# curvy = rock_bottom.ldf.Curvy()
	laputop_ltp = rock_bottom.functions.I3LaputopTriggerProbability()

	tray.AddService('LaputopSignalModel', name+'_LaputopSignalModel',
					LDF=loglog,
					LTP=laputop_ltp,
					SnowService = SnowService,
					use_top_sigma = True
					)
	tray.AddService('GaussCurveModel', name+'_GaussCurveModel',
                        		CRV=loglog,
                        		use_top_sigma = True,
                        		SnowService = "SimpleSnow")

	
	""" Configure minimizer """

	tray.AddService("I3GulliverMinuitFactory", name+"_Minuit",
					MinuitPrintLevel = -2,
					FlatnessCheck = True,
					Algorithm = "SIMPLEX",
					MaxIterations = 2500,
					MinuitStrategy = 2,
					Tolerance = 0.01)
	
	
	""" Configure likelihoods """
				
	tray.AddService('I3RbLDFLikelihoodFactory', name+'_TopLLH',
					DetectorType=rock_bottom.IceTop,
					Model=name+'_LaputopSignalModel',
					HLCPulses=HLCPulses,
					SaturatedPulses='',
					IgnoreTanks='',
					UseSilent = True,
					Toprec = True,
					MinSignal = 0.7
					)
					
	tray.AddService('I3CurveLikelihoodFactory', name+'_CurveLLH',
					Model=name+'_GaussCurveModel',
					HLCPulses=HLCPulses,
					SaturatedPulses='',
					IgnoreTanks='',
					Toprec = True,
					MinSignal = 0.7
					)
	
				
	""" Configure parametrizations """
	
	tray.AddService("I3ComboParametrizationFactory", name+"_TopParams_Step1",
					StepX=10.0*I3Units.m,
					StepY=10.0*I3Units.m,
					StepLogE=0.1,
					RelativeBoundsX=[-200.*I3Units.ns,+200.*I3Units.ns],
					RelativeBoundsY=[-200.*I3Units.ns,+200.*I3Units.ns],
					BoundsLogE=[1,11],
					# Boundslog10S125=[-3.,8.],
					BoundsBeta=[2.9,3.1],
					# Steplog10S125=1.,
					StepBeta=0.6,
					)

	tray.AddService("I3ComboParametrizationFactory", name+"_TopParams_Step2",
					StepT=50.0*I3Units.ns,
					StepX=2.0*I3Units.m,
					StepY=2.0*I3Units.m,
					StepLogE=0.1,
					RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
					RelativeBoundsX=[-15.0*I3Units.m,+15.0*I3Units.m],
					RelativeBoundsY=[-15.0*I3Units.m,+15.0*I3Units.m],
					BoundsLogE=[1,11],
					# Boundslog10S125=[-3.,8.],
					BoundsBeta=[2.,4.],
					# Steplog10S125=0.045,
					StepBeta=0.15,
					)

	tray.AddService("I3ComboParametrizationFactory", name+"_TopParams_Step3",
					StepT=50.0*I3Units.ns,
					StepX=1.0*I3Units.m,
					StepY=1.0*I3Units.m,
					StepLogE=0.1,
					RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
					RelativeBoundsX=[-45.0*I3Units.m,+45.0*I3Units.m],
					RelativeBoundsY=[-45.0*I3Units.m,+45.0*I3Units.m],
					BoundsLogE=[1,11],
					# Boundslog10S125=[-3.,8.],
					BoundsBeta=[0.,10.],
					# Steplog10S125=0.045,
					StepBeta=0.15,
					)	
					
	""" Combine likelihoods """
	
	tray.AddService("I3EventLogLikelihoodCombinerFactory", name+"_TopOnlyCombo",
					InputLogLikelihoods = [name+"_TopLLH",name+"_CurveLLH"],
					Multiplicity = 'Sum',
					RelativeWeights = [1.,1.]
					)
				
	""" Configure 1st seed service """
	
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
		
	""" Do the 1st fit """
	tray.AddModule("I3SimpleFitter", name+'_Step1',
					SeedService = name+"_SimpleSeeder",
					Parametrization = name+"_TopParams_Step1",
					LogLikelihood = name+'_TopLLH',
					OutputName = OutputName+"_Step1",
					Minimizer = name+"_Minuit"
					) 	

	""" Configure 2nd seed service """
	tray.AddService("I3ComboSeedServiceFactory", name+"_Step2Seeder",
					FirstGuesses=[ name+'_Step1' ],
					HLCPulses = HLCPulses,
					SignalModel=name+'_LaputopSignalModel',
					Toprec = True,
					TimeShiftType="TFirst"
					)
		
	""" Do the 2nd fit """
	tray.AddModule("I3SimpleFitter", name+'_Step2',
					SeedService = name+"_Step2Seeder",
					Parametrization = name+"_TopParams_Step2",
					LogLikelihood = name+"_TopOnlyCombo",
					OutputName = OutputName+"_Step2",
					Minimizer = name+"_Minuit"
					) 	
					

	""" Configure 3rd seed service """
	tray.AddService("I3ComboSeedServiceFactory", name+"_Step3Seeder",
					FirstGuesses=[ name+'_Step2' ],
					HLCPulses = HLCPulses,
					SignalModel=name+'_LaputopSignalModel',
					Toprec = True,
					TimeShiftType="TFirst"
					)
		
	""" Do the 3rd fit """
	tray.AddModule("I3SimpleFitter", name+'_Step3',
					SeedService = name+"_Step3Seeder",
					Parametrization = name+"_TopParams_Step3",
					LogLikelihood = name+"_TopOnlyCombo",
					OutputName = OutputName+"_Step3",
					Minimizer = name+"_Minuit"
					) 	
					


