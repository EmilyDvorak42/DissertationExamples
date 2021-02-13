import os, sys
from icecube import icetray

""" 

Tray segment to run the RockBottom air shower reconstruction 
with two LDFs and curvature fit, using IceTop and in-ice detector 
information. 

Inputs:

	* SLCPulses: 		(cleaned) IceTop SLC pulse series
	* HLCPulses: 		(cleaned) IceTop HLC pulse series
	* IgnoreTanks:		IceTop tanks to ignore
	* InIcePulses: 		(cleaned) in-ice pulse series
	* Seed: 			first guess reconstruction (any I3Particle)
	* InIceLLH: 		LLH description for in-ice, e.g. 'SPEAll', 
						'SPEqAll', 'SPE1st'(default), 'MPE', 'MPEAll'
	* LDF: 				electromagnetic LDF, e.g. 'dlp' (default), 
						'nkg', 'lagutin'
	* Fitter:	 		select fitter, e.g. 'simple' (default), 'iterative', 'paraboloid'
	* NIterations:		number of iterations for iterative fitting, 
						if =1 -> individual steps, else IterativeFitter
	* ZenithDependence: enable zenith dependent muon LDF (default: True)
	* FlexiCurvature: 	enable flexible curvature fit (default: False)
	* FixCore:			fix core position for two LDF fit, not available with 
						Fitter='iterative' (default: False)		
	* OutputName: 		name of output I3Particle 
						(fit parameters stored in OutputName+'Params')
	
	
"""


@icetray.traysegment
def RockBottomTwoLDFCoinc(tray, name = 'RockBottomTwoLDFCoincSegment',
							SLCPulses = 'SRTCleanedSLCPulses',
							HLCPulses = 'SRTCleanedHLCPulses',
							IgnoreTanks = '',
							InIcePulses = 'SRTCoincPulses',
							Seed = 'CoincMuonReco_SPEFit2',
							InIceLLH = 'SPE1st',
							LDF = 'dlp',
							Fitter = 'simple',
							NIterations = 1.,
							ZenithDependence = True,
							FlexiCurvature = False,
							FixCore = False,
							OutputName = 'RockBottomTwoLDFCoinc'
							):
						
	from icecube import dataclasses, gulliver, gulliver_modules, lilliput, rock_bottom, phys_services
	from icecube.icetray import I3Units
	
	
	""" Configure simple snow service """
	
	tray.AddService('I3SimpleSnowCorrectionServiceFactory', name+'_SimpleSnow',
					Lambda= 2.1
		       		)
		       		
	
	""" Configure signal model """
	
	if LDF =='nkg':
		ldf = rock_bottom.ldf.NKG()
		BetaStep = 0.15
		BetaStep1 = 0.2
		BetaStep2 = 0.1
		BetaStep3 = 0.15
	elif LDF == 'lagutin':
		ldf = rock_bottom.ldf.Lagutin()
		BetaStep = 0.15
		BetaStep1 = 0.2
		BetaStep2 = 0.1
		BetaStep3 = 0.15
	else:
		ldf = rock_bottom.ldf.LogLog()
		BetaStep = 0.15
		BetaStep1 = 0.6
		BetaStep2 = 0.2
		BetaStep3 = 0.15
		
	dlp = rock_bottom.ldf.LogLog()
	muonldf = rock_bottom.ldf.MuonLDF()
	
	tankresponse_dir = os.environ['I3_SRC'] + '/rock_bottom/resources/data/tank_response/'

	tray.AddService('LaputopSignalModel', name+'_TopLDFSignalModel',
					LDF=dlp,
					SnowService = name+'_SimpleSnow'
					)
					
	tray.AddService('TwoLDFSignalModel', name+'_TwoLDFSignalModel',
					TankResponseTablesDir = tankresponse_dir,
					ZenithDependence = ZenithDependence,
					emLDF = ldf,
					muLDF = muonldf,
					SnowService = name+'_SimpleSnow'
					)
					
	tray.AddService('GaussCurveModel', name+'_GaussCurveModel')
	
	
	""" Configure minimizer """

	tray.AddService('I3GulliverMinuitFactory', name+'_Minuit',
					MinuitPrintLevel = -2,
					FlatnessCheck = True,
					Algorithm = 'SIMPLEX',
					MaxIterations = 2500,
					MinuitStrategy = 2,
					Tolerance = 0.01
					)
	
	
	""" Configure likelihoods """
	
	tray.AddService('I3RbLDFLikelihoodFactory', name+'_TopLDFLLH',
	        DetectorType = rock_bottom.IceTop,
					Model=name+'_TopLDFSignalModel',
					Pulses1=HLCPulses,
					UseSaturated=True,
					IgnoreDetectors=IgnoreTanks,
					UseSilent = True,
					MinSignal = 0.7
					)
				
	tray.AddService('I3RbLDFLikelihoodFactory', name+'_TwoLDFLLH',
	        DetectorType = rock_bottom.IceTop,
					Model=name+'_TwoLDFSignalModel',
					Pulses1=HLCPulses,
					Pulses2=SLCPulses,
					UseSaturated=True,
					IgnoreDetectors=IgnoreTanks,
					UseSilent = True,
					MinSignal = 0.7
					)
				
	tray.AddService('I3RbTimingLikelihoodFactory', name+'_CurveLLH',
	        DetectorType = rock_bottom.IceTop,
					Model=name+'_GaussCurveModel',
					Pulses1=HLCPulses,
					UseSaturated=True,
					IgnoreDetectors=IgnoreTanks,
					MinSignal = 0.7,
					)
	
	tray.AddService('I3GulliverIPDFPandelFactory', name+'_InIceLLH',
					InputReadout=InIcePulses,
					EventType='InfiniteMuon',
					Likelihood=InIceLLH,
					PEProb='GaussConvolutedFastApproximation',
					JitterTime=4.0 * I3Units.ns,
					NoiseProbability=10. * I3Units.hertz
					)
					
		
				
	""" Configure parametrizations """
	
	tray.AddService('I3ComboParametrizationFactory', name+'_TopLDFParams',
					StepT=50.0*I3Units.ns,
					StepX=1.0*I3Units.m,
					StepY=1.0*I3Units.m,
					StepNX=0.1,
					StepNY=0.1,
					RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
					RelativeBoundsX=[-15.0*I3Units.m,+15.0*I3Units.m],
					RelativeBoundsY=[-15.0*I3Units.m,+15.0*I3Units.m],
					#RelativeBoundsNX=[-0.1,+0.1],
					#RelativeBoundsNY=[-0.1,+0.1],
					BoundsNX=[-1.,+1.],
					BoundsNY=[-1.,+1.],
					BoundsLog10_S125=[-1.,6.],
					BoundsBeta=[0., 6.],
					Steplog10_S125=0.045,
					StepBeta=0.15
					)
								
	tray.AddService('I3ComboParametrizationFactory', name+'_TwoLDFParams_RhoMu',
					StepT=50.0*I3Units.ns,
					StepX=1.0*I3Units.m,
					StepY=1.0*I3Units.m,
					StepZ=1.0*I3Units.m,
					StepNX=0.1,
					StepNY=0.1,
					RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
					RelativeBoundsNX=[-1.,+1.],
					RelativeBoundsNY=[-1.,+1.],
					RelativeBoundsX=[-45.0*I3Units.m,+45.0*I3Units.m],
					RelativeBoundsY=[-45.0*I3Units.m,+45.0*I3Units.m],
					RelativeBoundsZ=[-15.0*I3Units.m,+15.0*I3Units.m],
					BoundsRhoMu=[0.0, 20.],
					StepRhoMu=0.05,
					)
					
					
	tray.AddService('I3ComboParametrizationFactory', name+'_TwoLDFParams_RhoMu0',
					BoundsLog10_S125=[-1.,6.],
					#RelativeBoundsLog10_S125=[-1., +1.],
					BoundsBeta=[0., 6.],
					#RelativeBoundsBeta=[-1., +1.],
					BoundsRhoMu=[0.0, 20.],
					Steplog10_S125=0.045,
					StepBeta=BetaStep,
					StepRhoMu=0.05,
					)
				
	tray.AddService('I3ComboParametrizationFactory', name+'_TwoLDFParams1',
					StepT=50.0*I3Units.ns,
					StepNX=0.1,
					StepNY=0.1,
					RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
					RelativeBoundsNX=[-1.,+1.],
					RelativeBoundsNY=[-1.,+1.],
					RelativeBoundsLog10_S125=[-1., +1.],
					RelativeBoundsBeta=[-1., +1.],
					BoundsRhoMu=[0.0, 3.],
					Steplog10_S125=0.45,
					StepBeta=BetaStep1,
					StepRhoMu=0.1
					)
					
	tray.AddService('I3ComboParametrizationFactory', name+'_TwoLDFParams2',
					StepT=50.0*I3Units.ns,
					StepX=1.0*I3Units.m,
					StepY=1.0*I3Units.m,
					StepZ=1.0*I3Units.m,
					#StepNX=0.1,
					#StepNY=0.1,
					RelativeBoundsT=[-100.*I3Units.ns,+100.*I3Units.ns],
					RelativeBoundsX=[-200.0*I3Units.m,+200.0*I3Units.m],
					RelativeBoundsY=[-200.0*I3Units.m,+200.0*I3Units.m],
					RelativeBoundsZ=[-100.0*I3Units.m,+100.0*I3Units.m],
					#RelativeBoundsNX=[-0.2,+0.2],
					#RelativeBoundsNY=[-0.2,+0.2],
					RelativeBoundsLog10_S125=[-1 ,+1],
					RelativeBoundsBeta=[-1, +1],
					BoundsRhoMu=[0.0, 10.],
					Steplog10_S125=0.045,
					StepBeta=BetaStep2,
					StepRhoMu=0.15
					)
	
	if FlexiCurvature:					
		tray.AddService('I3ComboParametrizationFactory', name+'_TwoLDFParams3',
						StepT=50.0*I3Units.ns,
						StepX=1.0*I3Units.m,
						StepY=1.0*I3Units.m,
						StepZ=1.0*I3Units.m,
						StepNX=0.1,
						StepNY=0.1,
						RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
						RelativeBoundsX=[-45.0*I3Units.m,+45.0*I3Units.m],
						RelativeBoundsY=[-45.0*I3Units.m,+45.0*I3Units.m],
						RelativeBoundsZ=[-15.0*I3Units.m,+15.0*I3Units.m],
						RelativeBoundsNX=[-0.2,+0.2],
						RelativeBoundsNY=[-0.2,+0.2],
						RelativeBoundsLog10_S125=[-1., +1.],
						RelativeBoundsBeta=[-1, +1],
						BoundsRhoMu=[0.0, 20.],
						Steplog10_S125=0.045,
						StepBeta=BetaStep3,
						StepRhoMu=0.05,
						StepAmp=0.0001,
						BoundsAmp=[0.000001,0.01],
						)
						
		tray.AddService('I3ComboParametrizationFactory', name+'_TwoLDFParams',
						StepT=50.0*I3Units.ns,
						StepX=1.0*I3Units.m,
						StepY=1.0*I3Units.m,
						StepZ=1.0*I3Units.m,
						StepNX=0.1,
						StepNY=0.1,
						RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
						RelativeBoundsNX=[-1.,+1.],
						RelativeBoundsNY=[-1.,+1.],
						RelativeBoundsX=[-45.0*I3Units.m,+45.0*I3Units.m],
						RelativeBoundsY=[-45.0*I3Units.m,+45.0*I3Units.m],
						RelativeBoundsZ=[-15.0*I3Units.m,+15.0*I3Units.m],
						RelativeBoundsLog10_S125=[-1., +1.],
						RelativeBoundsBeta=[-1., +1.],
						BoundsRhoMu=[0.0, 20.],
						Steplog10_S125=0.045,
						StepBeta=BetaStep,
						StepRhoMu=0.05,
						StepAmp=0.0001,
						BoundsAmp=[0.000001,0.01],
						)
						
		tray.AddService('I3ComboParametrizationFactory', name+'_TwoLDFParams_noCore',
						StepT=50.0*I3Units.ns,
						StepNX=0.1,
						StepNY=0.1,
						RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
						RelativeBoundsNX=[-1.,+1.],
						RelativeBoundsNY=[-1.,+1.],
						RelativeBoundsLog10_S125=[-1., +1.],
						RelativeBoundsBeta=[-1., +1.],
						BoundsRhoMu=[0.0, 20.],
						Steplog10_S125=0.045,
						StepBeta=BetaStep,
						StepRhoMu=0.05,
						StepAmp=0.0001,
						BoundsAmp=[0.000001,0.01],
						)
						
	else:
		tray.AddService('I3ComboParametrizationFactory', name+'_TwoLDFParams3',
						StepT=50.0*I3Units.ns,
						StepX=1.0*I3Units.m,
						StepY=1.0*I3Units.m,
						StepZ=1.0*I3Units.m,
						StepNX=0.1,
						StepNY=0.1,
						RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
						RelativeBoundsX=[-45.0*I3Units.m,+45.0*I3Units.m],
						RelativeBoundsY=[-45.0*I3Units.m,+45.0*I3Units.m],
						RelativeBoundsZ=[-15.0*I3Units.m,+15.0*I3Units.m],
						RelativeBoundsNX=[-0.2,+0.2],
						RelativeBoundsNY=[-0.2,+0.2],
						RelativeBoundsLog10_S125=[-1., +1.],
						RelativeBoundsBeta=[-1., +1.],
						BoundsRhoMu=[0.0, 20.],
						Steplog10_S125=0.045,
						StepBeta=BetaStep3,
						StepRhoMu=0.05
						)
						
		tray.AddService('I3ComboParametrizationFactory', name+'_TwoLDFParams',
						StepT=50.0*I3Units.ns,
						StepX=1.0*I3Units.m,
						StepY=1.0*I3Units.m,
						StepZ=1.0*I3Units.m,
						StepNX=0.1,
						StepNY=0.1,
						RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
						RelativeBoundsNX=[-1.,+1.],
						RelativeBoundsNY=[-1.,+1.],
						RelativeBoundsX=[-45.0*I3Units.m,+45.0*I3Units.m],
						RelativeBoundsY=[-45.0*I3Units.m,+45.0*I3Units.m],
						RelativeBoundsZ=[-15.0*I3Units.m,+15.0*I3Units.m],
						RelativeBoundsLog10_S125=[-1., +1.],
						RelativeBoundsBeta=[-1., +1.],
						BoundsRhoMu=[0.0, 20.],
						Steplog10_S125=0.045,
						StepBeta=BetaStep,
						StepRhoMu=0.05,
						)
						
		tray.AddService('I3ComboParametrizationFactory', name+'_TwoLDFParams_noCore',
						StepT=50.0*I3Units.ns,
						StepNX=0.1,
						StepNY=0.1,
						RelativeBoundsT=[-200.*I3Units.ns,+200.*I3Units.ns],
						RelativeBoundsNX=[-1.,+1.],
						RelativeBoundsNY=[-1.,+1.],
						RelativeBoundsLog10_S125=[-1., +1.],
						RelativeBoundsBeta=[-1., +1.],
						BoundsRhoMu=[0.0, 20.],
						Steplog10_S125=0.045,
						StepBeta=BetaStep,
						StepRhoMu=0.05,
						)
					
					
	""" Combine likelihoods """
	
	tray.AddService('I3EventLogLikelihoodCombinerFactory', name+'_TopLDFCombo',
					InputLogLikelihoods = [name+'_TopLDFLLH',name+'_CurveLLH',name+'_InIceLLH'],
					Multiplicity = 'Sum',
					RelativeWeights = [1.,1.,1.]
					)
					
	tray.AddService('I3EventLogLikelihoodCombinerFactory', name+'_TwoLDFCombo',
					InputLogLikelihoods = [name+'_TwoLDFLLH',name+'_CurveLLH',name+'_InIceLLH'],
					Multiplicity = 'Sum',
					RelativeWeights = [1.,1.,1.]
					)
					
	tray.AddService('I3EventLogLikelihoodCombinerFactory', name+'_TwoLDFCombo_noCurv',
					InputLogLikelihoods = [name+'_TwoLDFLLH',name+'_InIceLLH'],
					Multiplicity = 'Sum',
					RelativeWeights = [1.,1.]
					)
	

	""" Configure seed service """
	
	tray.AddService("I3ComboSeedServiceFactory", name+"_TopComboSeeder",
					InputReadout=InIcePulses,
					FirstGuesses=[ Seed ],
					HLCPulses = HLCPulses,
					SignalModel=name+'_TopLDFSignalModel',
					Beta = 2.6,
					TimeShiftType="TFirst",
					Toprec = True
					)
					
	
	""" Do single LDF fit as seed """
	
	tray.AddModule('I3SimpleFitter', name+'_TopLDF',
					SeedService = name+'_TopComboSeeder',
					Parametrization = name+'_TopLDFParams',
					LogLikelihood = name+'_TopLDFCombo',
					OutputName = OutputName+'0',
					Minimizer = name+'_Minuit'
					) 
	
	tray.AddService('I3ComboSeedServiceFactory', name+'_ComboSeeder',
					InputReadout=InIcePulses,
					FirstGuesses=[ OutputName+'0' ],
					HLCPulses = HLCPulses,
					SLCPulses = SLCPulses,
					SignalModel=name+'_TwoLDFSignalModel',
					RhoMu = 1.0,
					TimeShiftType='TFirst'
					)
					
					
	""" Do the two LDF fit(s) """
					
	tray.AddModule('I3SimpleFitter', name+'_TwoLDF_RhoMu',
					SeedService = name+'_ComboSeeder',
					Parametrization = name+'_TwoLDFParams_RhoMu',
					LogLikelihood = name+'_TwoLDFCombo',
					OutputName = OutputName+'RhoMu',
					Minimizer = name+'_Minuit'
					) 
						
	tray.AddModule('I3SimpleFitter', name+'_TwoLDF_RhoMu0',
					SeedService = name+'_ComboSeeder',
					Parametrization = name+'_TwoLDFParams_RhoMu0',
					LogLikelihood = name+'_TwoLDFCombo_noCurv',
					OutputName = OutputName+'RhoMu0',
					Minimizer = name+'_Minuit'
					) 
		
	
	if Fitter=='iterative':	
		
		""" iterative """
		
		if NIterations==1:
			tray.AddModule('I3SimpleFitter', name+'_TwoLDF1',
							SeedService = name+'_ComboSeeder',
							Parametrization = name+'_TwoLDFParams1',
							LogLikelihood = name+'_TwoLDFCombo',
							OutputName = OutputName+'1',
							Minimizer = name+'_Minuit'
							) 
						
			tray.AddService('I3ComboSeedServiceFactory', name+'_ComboSeeder2',
							InputReadout=InIcePulses,
							FirstGuesses=[ OutputName+'1' ],
							HLCPulses = HLCPulses,
							SLCPulses = SLCPulses,
							SignalModel=name+'_TwoLDFSignalModel',
							TimeShiftType='TFirst'
							)
		
			tray.AddModule('I3SimpleFitter', name+'_TwoLDF2',
							SeedService = name+'_ComboSeeder2',
							Parametrization = name+'_TwoLDFParams2',
							LogLikelihood = name+'_TwoLDFCombo_noCurv',
							OutputName = OutputName+'2',
							Minimizer = name+'_Minuit'
							) 
							
			tray.AddService('I3ComboSeedServiceFactory', name+'_ComboSeeder3',
							InputReadout=InIcePulses,
							FirstGuesses=[ OutputName+'2' ],
							HLCPulses = HLCPulses,
							SLCPulses = SLCPulses,
							SignalModel=name+'_TwoLDFSignalModel',
							TimeShiftType='TFirst'
							)
						
			tray.AddModule('I3SimpleFitter', name+'_TwoLDF3',
							SeedService = name+'_ComboSeeder3',
							Parametrization = name+'_TwoLDFParams3',
							LogLikelihood = name+'_TwoLDFCombo',
							OutputName = OutputName+'3',
							Minimizer = name+'_Minuit'
							) 
			
			tray.AddModule('I3SimpleFitter', name+'_TwoLDFOut',
							SeedService = name+'_ComboSeeder2',
							Parametrization = name+'_TwoLDFParams3',
							LogLikelihood = name+'_TwoLDFCombo',
							OutputName = OutputName,
							Minimizer = name+'_Minuit'
							) 
			"""						
			tray.AddModule("Delete", name+'_IterationCleanup', 
							Keys=[ OutputName+'1', OutputName+'2' ]
							)
			"""	
		else:
			if FixCore:
				tray.AddModule("I3IterativeFitter", name+"_TwoLDF",
								SeedService=name+"_ComboSeeder",
								Parametrization=name+"_TwoLDFParams_noCore",
								LogLikelihood=name+"_TwoLDFCombo", 
								Minimizer=name+"_Minuit",
								OutputName=OutputName,
								RandomService="SOBOL",
								NIterations=NIterations
								) 
			else:
				tray.AddModule("I3IterativeFitter", name+"_TwoLDF",
								SeedService=name+"_ComboSeeder",
								Parametrization=name+"_TwoLDFParams",
								LogLikelihood=name+"_TwoLDFCombo", 
								Minimizer=name+"_Minuit",
								OutputName=OutputName,
								RandomService="SOBOL",
								NIterations=NIterations
								) 
				 
		
	elif Fitter=='paraboloid':
		
		""" paraboloid """
	
		tray.AddModule("I3ParaboloidFitter", name+'_TwoLDFParaboloid',
						SeedService = name+'_ComboSeeder',
						LogLikelihood = name+'_TwoLDFCombo',
						MaxMissingGridPoints = 1,
						VertexStepSize = 5.*I3Units.m,
						ZenithReach = 2.*I3Units.degree,
						AzimuthReach = 2.*I3Units.degree,
						GridpointVertexCorrection = name+'_ComboSeeder',
						Minimizer = name+'_Minuit',
						NumberOfSamplingPoints = 8,
						NumberOfSteps = 3,
						MCTruthName = '',#'I3MCTree',
						OutputName = OutputName
						)
					
	else:	
	
		""" simple """
		
		if FixCore:
			tray.AddModule('I3SimpleFitter', name+'_TwoLDF',
							SeedService = name+'_ComboSeeder',
							Parametrization = name+'_TwoLDFParams_noCore',
							LogLikelihood = name+'_TwoLDFCombo',
							OutputName = OutputName,
							Minimizer = name+'_Minuit'
							)
		else:
			tray.AddModule('I3SimpleFitter', name+'_TwoLDF',
							SeedService = name+'_ComboSeeder',
							Parametrization = name+'_TwoLDFParams',
							LogLikelihood = name+'_TwoLDFCombo',
							OutputName = OutputName,
							Minimizer = name+'_Minuit'
							) 
		

	"""						
		
	tray.AddModule("Delete", name+'_FinalCleanup', 
					Keys=[ OutputName+'1', OutputName+'2' ]
					)
	"""	
	