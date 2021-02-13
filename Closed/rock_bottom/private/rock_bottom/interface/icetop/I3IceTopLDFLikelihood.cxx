/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3IceTopLDFLikelihood.cxx 173853 2019-06-07 22:16:19Z dsoldin $
 *
 * \file I3TopLDFLikelihood.cxx
 *
 * \author Javier Gonzalez
 * \date 20 Nov 2012
 * \version $Revision: 173853 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-07 17:16:19 -0500 (Fri, 07 Jun 2019) $
 */

#include <rock_bottom/interface/I3RbLDFLikelihood.h>
#include <rock_bottom/interface/I3RockBall.h>
#include <gulliver/I3EventHypothesis.h>
#include <dataclasses/geometry/I3Geometry.h>
#include <icetray/I3SingleServiceFactory.h>
#include <rock_bottom/snowservices/tankPulse.h>
#include <dataclasses/TankKey.h>

#include <dataclasses/calibration/I3Calibration.h>
#include <dataclasses/status/I3DOMStatus.h>
#include <math.h>
#include <boost/limits.hpp>

using namespace std;

#ifndef DBL_MIN
#ifdef  __DBL_MIN__
#define DBL_MIN __DBL_MIN__
#endif
#endif

const double SAT_LG = 90000.;// Upper bound for LG in PE

double
I3RbLDFLikelihood::GetIceTopLogLikelihood( const I3EventHypothesis &ehypo )
{

  fSignalModel->SetParameters(ehypo);
  log_trace("starting likelihood calculation");
  I3ParameterMapPtr ldf_parameters = boost::dynamic_pointer_cast<I3ParameterMap>(ehypo.nonstd);
  if (ldf_parameters) {
    //ldf_parameters->SetParameterByName("r_ref", 225.0);
    log_debug("log-likelihood params: [%f, %f, %f]", ldf_parameters->GetParameterByName("Log10_S125"), 
      ldf_parameters->GetParameterByName("Beta"), ldf_parameters->GetParameterByName("RhoMu"));
  }

  /*
    The likelihood is a product of four terms:
      1.- HLCs
      2.- SLCs
      3.- Saturated tanks
      4.- Silent tanks

      The likelihood factor that corresponds to silent stations can,
      in principle, depend on things other than the signal (it can
      depend on the EM/muon ratio, the zenith angle and so on. For the
      time being it depends only on signal. That might change. Also,
      the variance of signals slightly above threshold should be
      smaller, but in this case they should some how include the
      trigger probability. Don't know how to do that now.
  */
  
  double chi2_ldf = 0;
  double ndoffer = 0;
  double ldf_free_params = 2;
  
  // HLCs
  log_trace("HLC likelihood");
  //log_info("HLC PULSES SIZE %i", int(fPulseSeries1.size()));
  double hlc_llh = 0;
  int hlc_num = 0;
  for (I3RecoPulseSeriesMap::const_iterator pIt = fPulseSeries1.begin();
       pIt != fPulseSeries1.end(); ++pIt) {
    const TankKey tankKey(pIt->first);
    const OMKey om = pIt->first;
    std::map<TankKey, I3TankGeo>::iterator geo = fStations.find(tankKey);
    //I3Position posit = fPulseSeriesDOMs1[hlc_num];
    I3Position posit = geo->second.position;;
    hlc_num++;
    if (om.GetOM() <= 60){
	    log_info("Didn't find the OMKey (%i,%i) in I3Geometry", om.GetString(), om.GetOM());
    }
    if (geo == fStations.end()) {
      log_fatal_stream("Tank %s is not in station map!" << tankKey);
    }
    const double signal = pIt->second[0].GetCharge();
    const I3VEMCalibration vemCalib = fCalibration->vemCal.find(pIt->first)->second;
    I3RockBall hlc_rockball;
    hlc_rockball.SetTankGeo(&geo->second);
    hlc_rockball.SetVEMCalibration(&vemCalib);
    hlc_rockball.SetPosition(&posit);
    hlc_rockball.SetSaturatedStatus(false);
    if (signal > fMinSignal){
    	hlc_llh += fSignalModel->GetSignalLogProbability(hlc_rockball, ehypo, signal);
    	chi2_ldf += fSignalModel->CalcChi2(hlc_rockball, ehypo, signal);
    	ndoffer += 1;
    } 
  	else {
  		hlc_llh += fSignalModel->GetSignalLogCumulativeProbability(hlc_rockball, ehypo, fMinSignal);
  	}
  }
  //log_info("HLCs %f",hlc_llh)
  // SLCs
  log_trace("SLC likelihood");
  //log_info("SLC PULSES SIZE %i", int(fPulseSeries2.size()));
  double slc_llh = 0;
  int slc_num = 0;
  for (I3RecoPulseSeriesMap::const_iterator pIt = fPulseSeries2.begin();
       pIt != fPulseSeries2.end(); ++pIt) {
    const TankKey tankKey(pIt->first);
    log_trace_stream("%s SLC" << tankKey);
    std::map<TankKey, I3TankGeo>::iterator geo = fStations.find(tankKey);
    I3Position posit = fPulseSeriesDOMs2[slc_num];
    slc_num++;
    if (geo == fStations.end()) {
      log_fatal_stream("Tank %s is not in station map!" << tankKey);
    }
    const double signal = pIt->second[0].GetCharge();
    const I3VEMCalibration vemCalib = fCalibration->vemCal.find(pIt->first)->second;
    I3RockBall slc_rockball;
    slc_rockball.SetTankGeo(&geo->second);
    slc_rockball.SetVEMCalibration(&vemCalib);
    slc_rockball.SetPosition(&posit);
    slc_rockball.SetSaturatedStatus(false);
    if (signal > fMinSignal){
      slc_llh += fSignalModel->GetSignalLogProbability(slc_rockball, ehypo, signal);
      chi2_ldf += fSignalModel->CalcChi2(slc_rockball, ehypo, signal);
      ndoffer += 1;
    } else {
      slc_llh += fSignalModel->GetSignalLogCumulativeProbability(slc_rockball, ehypo, fMinSignal);
    }
  }
  // assuming that we use SLCs only with muon twoLDF model
  // fix this!
  if (slc_llh !=0.0){
  	ldf_free_params = 3;
  }
  
  // Saturated
  log_trace("SATURATED likelihood");
  //log_info("SAT PULSES SIZE %i", int(fSaturatedSeries.size()));
  double sat_llh = 0;
  int sat_num = 0;	
  // Saturated (assuming only low-gain saturated)
  log_trace("saturated tank likelihood");
  for (I3RecoPulseSeriesMap::const_iterator pIt = fSaturatedSeries.begin();
       fUseSaturated && pIt != fSaturatedSeries.end(); ++pIt) {
    const TankKey tankKey(pIt->first);
    std::map<TankKey, I3TankGeo>::iterator geo = fStations.find(tankKey);
    //I3Position posit = fSaturatedDOMs[sat_num];
    I3Position posit = geo->second.position;
    sat_num++;
    log_trace_stream("%s saturated" << tankKey);
    if (geo == fStations.end()) {
      log_fatal_stream("Tank %s is not in station map!" << tankKey);
    }
    const I3VEMCalibration vemCalib = fCalibration->vemCal.find(pIt->first)->second;
    const double pe_per_vem = vemCalib.pePerVEM/vemCalib.corrFactor;
    const double signal = fLowGainSaturationThreshold/pe_per_vem;
    I3RockBall sat_rockball;
    sat_rockball.SetTankGeo(&geo->second);
    sat_rockball.SetVEMCalibration(&vemCalib);
    sat_rockball.SetPosition(&posit);
    sat_rockball.SetSaturatedStatus(true);
    sat_llh += fSignalModel->GetSignalLogCumulativeProbability(sat_rockball, ehypo, signal);
  }

  // Silent
  log_trace("SILENT likelihood");
  //log_info("SILENT PULSES SIZE %u", int(fSilentTanks.size()));
  double sil_llh = 0;
  int sil_num = 0;
  for (unsigned int i = 0; fUseSilent && i != fSilentTanks.size(); ++i) {
    std::map<TankKey, I3TankGeo>::iterator geo = fStations.find(fSilentTanks[i]);
    double snowdepth = fSilentSnow[sil_num];
    //I3Position posit = fSilentDOMs[sil_num];
    I3Position posit = geo->second.position;;
    sil_num++;    
    if (geo == fStations.end()) {
      log_fatal_stream("Tank %s is not in station map!" << fSilentTanks[i]);
    }
    const I3VEMCalibration vemCalib = fCalibration->vemCal.find(geo->second.omKeyList_[0])->second;
    I3RockBall sil_rockball;
    // We don't need this for silent stations, or?
    if (fMinSignal>0) {
    	sil_rockball.SetTankGeo(&geo->second);
    	sil_rockball.SetVEMCalibration(&vemCalib);
    	sil_rockball.SetPosition(&posit);
    	sil_rockball.SetSaturatedStatus(false);
    	double p = fSignalModel->GetSignalCumulativeProbability(sil_rockball, ehypo, fMinSignal);
        //log_info("NOPE A %f",p);
    	if (p == 1.0){
    		sil_llh += log(DBL_MIN);
    	} else {
    		sil_llh += log(1.-p);
    	}
    } else {
    	sil_rockball.SetTankGeo(&geo->second);
    	sil_rockball.SetVEMCalibration(&vemCalib);
    	sil_rockball.SetPosition(&posit);
	double local_p_hit = fSignalModel->GetHitProbability(sil_rockball);
        double local_station_nohit = (1.-pow(local_p_hit, 2.));
        //log_info("NOPE B %f",local_p_hit);

        if (local_station_nohit == 0.0){
		sil_llh += log(DBL_MIN); 
	} else { 
		sil_llh += log(local_station_nohit);
	}
    }
    /*
    sil_rockball.SetTankGeo(&geo->second);
    sil_rockball.SetVEMCalibration(&vemCalib);
    sil_rockball.SetPosition(&posit);
    sil_llh += log(1. - fSignalModel->GetHitProbability(sil_rockball));
    */
  }
  ldf_parameters->SetParameterByName("Chi2_ldf", chi2_ldf);
  ldf_parameters->SetParameterByName("ndof_ldf", ndoffer - ldf_free_params);
  ldf_parameters->SetParameterByName("ndof", ndoffer - ldf_free_params);
  const double llh = hlc_llh + slc_llh + sat_llh + sil_llh;
  ldf_parameters->SetParameterByName("llh_ldf",llh);
  /*
  log_info("log-likelihood (hlc + slc + sat + sil): %f + %f + %f + %f -> %f (%f)",
            hlc_llh,
            slc_llh,
            sat_llh,
            sil_llh,
            llh, llh);
  */
  log_trace("log-likelihood (hlc + slc + sat + sil): %f + %f + %f + %f -> %f (%f)",
            hlc_llh/(fPulseSeries1.size()?fPulseSeries1.size():1),
            slc_llh/(fPulseSeries2.size()?fPulseSeries2.size():1),
            sat_llh/(fSaturatedSeries.size()?fSaturatedSeries.size():1),
            sil_llh/(fSilentTanks.size()?fSilentTanks.size():1),
            llh/GetMultiplicity(), llh);

  return llh;
}


unsigned int I3RbLDFLikelihood::GetIceTopMultiplicity() {

  return fPulseSeries2.size() + fPulseSeries1.size() + fSaturatedSeries.size() + fSilentTanks.size(); // why silent tanks?
}
