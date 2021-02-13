#!/usr/bin/env python
import os
import sys

import math
import numpy as np
from math import exp, expm1
from I3Tray import *
from icecube.icetray import I3Units
from icecube import icetray, dataio, dataclasses, recclasses
from icecube.icetray import I3Units
from icecube.icetray.i3logging import log_info, log_warn, log_debug
import matplotlib
matplotlib.use('agg')

###********************************************************************
### 		COG and plane front calculations based on toprec
###********************************************************************

class ScintSeed(icetray.I3Module):
	def __init__(self, context):
		icetray.I3Module.__init__(self, context)
		#self.AddParameter("FilenameList", "List of files to read", fFileList);
		self.AddParameter("FilenameList","Input files", None)
		self.AddParameter("Frameobject","Frame object you want to pass to module", "ScintillatorPulses")
		self.AddParameter("Framename", "where to put the collected values", None)
		self.AddOutBox("OutBox")
	def Configure(self):
		self.infiles = self.GetParameter("FilenameList")
		self.objects = self.GetParameter("Frameobject")
		self.names = self.GetParameter("Framename")
	def Physics(self, frame):
		charges_scint=dataclasses.I3RecoPulseSeriesMap.from_frame(frame,self.objects)
		strings = np.asarray([i.string for i in charges_scint.keys()])
		oms = np.asarray([i.om for i in charges_scint.keys()])
		geometry = frame['ScintillatorArrayGeometry'] 
		# ~ print geometry.omgeo
		pos_x = np.asarray([geometry.omgeo[icetray.OMKey(strings[i],oms[i])].position.x for i in range(0,len(strings))])
		pos_y = np.asarray([geometry.omgeo[icetray.OMKey(strings[i],oms[i])].position.y for i in range(0,len(strings))])
		pos_z = np.asarray([geometry.omgeo[icetray.OMKey(strings[i],oms[i])].position.z for i in range(0,len(strings))])
		all_scint = [p for dom, pulses in charges_scint for p in pulses]
		pulse = np.asarray([p.charge for p in all_scint])
		time = np.asarray([p.time for p in all_scint])
		# ~ time_min = min(time0)
		# ~ time = np.asarray([s-time_min for s in time0])
		## *************************************************************
		##				Means weighted
		## *************************************************************
		mean_x = 0.
		mean_y = 0.
		mean_z = 0.
		mean_t = 0.
		mean_t0 = 0.
		weightsum = 0.
		COG = dataclasses.I3Particle()
		if len(pulse)!=0: 
			for t in range(0,len(strings)):
				weight0 = pulse[t]
				weightsum += weight0
				mean_x += pos_x[t]*weight0
				mean_y += pos_y[t]*weight0
				mean_z += pos_z[t]*weight0
				mean_t += time[t]*weight0

			mean_x /= weightsum
			mean_y /= weightsum
			mean_z /= weightsum
			mean_t /= weightsum	

		sigma = 5.*icetray.I3Units.ns
		weight = 1./sigma/sigma
		suma=[0.,0.,0.]
		signal=0.
		Sxx = 0.
		Sxy = 0.
		Syy = 0.
		Stx = 0.
		Sty = 0.

		if len(pulse)!=0:
			for d in range(0,(len(strings))):
				vec = np.array([pos_x[d],pos_y[d],pos_z[d]])
				vec = vec*math.sqrt(pulse[d])                         
				suma  += vec
				signal += math.sqrt(pulse[d])
				Sxx = Sxx + (pos_x[d]-mean_x)*(pos_x[d]-mean_x)*weight
				Sxy = Sxy + (pos_x[d]-mean_x)*(pos_y[d]-mean_y)*weight
				Syy = Syy + (pos_y[d]-mean_y)*(pos_y[d]-mean_y)*weight
				Stx = Stx + (time[d]-mean_t)*(pos_x[d]-mean_x)*weight
				Sty = Sty + (time[d]-mean_t)*(pos_y[d]-mean_y)*weight
			core = suma/signal
			print "Core from COG.....", core
			COG_x=core[0]
			COG_y=core[1]
			COG_z=core[2]
			
			## *********************************************************
			##				Matrix inversion
			## *********************************************************
			# ~ COG = dataclasses.I3Particle()
			nx=0.
			ny=0.
			phi=0.
			costh2=0.
			det = Sxx*Syy - Sxy*Sxy
			if math.fabs(det)<1E-4:
				nx=0.
				ny=0.
				phi=np.nan
				costh2=np.nan
				azimuth = np.nan
				time_core = np.nan
				print log_debug('Setting nan azimuth seed')
				COG.fit_status=dataclasses.I3Particle.FailedToConverge	
			else:	
				nx = dataclasses.I3Constants.c*(Stx * Syy - Sty * Sxy) / det
				ny = dataclasses.I3Constants.c*(Sty * Sxx - Stx * Sxy) / det
				costh2 = 1. - nx * nx - ny * ny;
				phi = math.atan2(ny, nx);
				azimuth = math.fmod((math.pi+phi),(2*math.pi))
				time_core = mean_t #- (nx*mean_x)/dataclasses.I3Constants.c-(ny*mean_y)/dataclasses.I3Constants.c
				print "Time of core: ", mean_t, time_core
				#~ print log_info('Setting proper azimuth seed')
				print "Setting proper azimuth seed"
				COG.fit_status=dataclasses.I3Particle.OK
			if costh2 >= 0.:
				theta = math.acos(-1*math.sqrt(costh2))
				zenith=math.pi-theta
				#~ print log_info('Setting proper zenith seed')
				print "Setting proper zenith seed"
				COG.fit_status=dataclasses.I3Particle.OK
			else:
				theta = np.nan
				zenith = np.nan
				print log_debug('Setting nan zenith seed')
				COG.fit_status=dataclasses.I3Particle.FailedToConverge

			chi2 = np.nan
			
			## *********************************************************
			##				Write output
			## *********************************************************
			
			COG.pos = dataclasses.I3Position(COG_x,COG_y,COG_z)
			COG.dir=dataclasses.I3Direction(zenith, azimuth)
			print "DirNX: ", COG.dir.x, "DirNY: ", COG.dir.y
			COG.time = time_core #mean_t
			COG.shape = dataclasses.I3Particle.ParticleShape.Primary
			frame['Shower'+self.names]= COG
			self.PushFrame(frame)    
		else:
			print "No pulses in frame"
			COG.pos = dataclasses.I3Position(np.nan,np.nan,np.nan)
			COG.dir=dataclasses.I3Direction(np.nan, np.nan)
			COG.time = np.nan
			COG.shape = dataclasses.I3Particle.ParticleShape.Primary
			COG.fit_status=dataclasses.I3Particle.FailedToConverge
			frame['Shower'+self.names]= COG
			self.PushFrame(frame)  
				
