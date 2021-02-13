/**
 * copyright  (C) 2019
 *
 * The Icecube Collaboration
 *
 * $Id: I3ScintLDFLikelihood.cxx 173798 2019-06-06 16:04:14Z agnieszka.leszczynska $
 *
 * \file I3ScintLDFLikelihood.cxx
 *
 * \author Alan Coleman
 * \date 17 May 2019
 * \version $Revision: 173798 $
 * Last changed by $LastChangedBy: agnieszka.leszczynska $ on $LastChangedDate: 2019-06-06 11:04:14 -0500 (Thu, 06 Jun 2019) $
 */

#include <rock_bottom/interface/I3RbLDFLikelihood.h>
#include <rock_bottom/snowservices/tankPulse.h>
#include <rock_bottom/I3RbUtilities.h>
#include <rock_bottom/interface/I3RockBall.h>

#include <icetray/I3SingleServiceFactory.h>
#include <gulliver/I3EventHypothesis.h>
#include <math.h>
#include <boost/limits.hpp>

using namespace std;

double I3RbLDFLikelihood::GetScintLogLikelihood(const I3EventHypothesis & ehypo) {
  fSignalModel->SetParameters(ehypo);
  log_trace("starting likelihood calculation");
  I3ParameterMapPtr ldf_parameters = boost::dynamic_pointer_cast<I3ParameterMap>(ehypo.nonstd);
  ldf_parameters->SetParameterByName("r_ref", 200.0);
  ldf_parameters->SetParameterByName("Kappa", 0.35);

  if (ldf_parameters) {
    log_trace("log-likelihood params: [%f, %f]", ldf_parameters->GetParameterByName("Log10_S125"),
              ldf_parameters->GetParameterByName("Beta"));
  }

  double chi2_ldf = 0;
  double nDOF = 0;
  double ldf_free_params = 2;
  const double core_radius 	= 5.;
  const double core_radius_2  = 800.;

  // Scintillator LLH //////////////////////////////////////////////////
  double scint_llh = 0;
  log_trace("Scintillator likelihood");
  log_debug("Scintillator PULSES SIZE %i", int(fPulseSeries1.size()));


  for (I3RecoPulseSeriesMap::const_iterator pIt = fPulseSeries1.begin();
       pIt != fPulseSeries1.end(); ++pIt) {
    const OMKey om = pIt->first;
    std::map<OMKey, I3OMGeo>::iterator geo = fScintOMGeo.find(om);
    I3Position posit = geo->second.position;
    if (om.GetOM() >= 8) {
      log_info("Didn't find the OMKey (%i,%i) in I3Geometry", om.GetString(), om.GetOM());
    }
    if (geo == fScintOMGeo.end()) {
      log_fatal_stream("Scintillator %s is not in geo map!" << om);
    }

    const double rho = rock_bottom::GetDistToAxis(*ehypo.particle, posit);
    const double signal = pIt->second[0].GetCharge();

	if ((signal >= fMinSignal) && (rho >= core_radius) && (rho <= core_radius_2) ) {
	  I3RockBall ball;
	  ball.SetPosition(&posit);
		
	  if (signal<=1000.){
		  scint_llh += fSignalModel->GetSignalLogProbability(ball, ehypo, signal); //TODO
	  }
	  else {
		  scint_llh += fSignalModel->GetSignalLogCumulativeProbability(ball, ehypo, signal); //TODO
	  }
	  chi2_ldf 	+= fSignalModel->CalcChi2(ball, ehypo, signal);
	  nDOF 		+= 1;  
	}
  }


  // Scintillator silent LLH ///////////////////////////////////////////
  double scint_sil_llh = 0;
  log_trace("SILENT likelihood SCINTILLATORS");
  log_debug("SILENT PULSES SIZE SCINTILLATORS %u", fSilentScint.size());

  for (unsigned int i = 0; fUseSilent && i != fSilentScint.size(); ++i) {
    std::map<OMKey, I3OMGeo>::iterator geo = fScintOMGeo.find(fSilentScint[i]);
    I3Position scint_sil_posit = geo->second.position;
    if (geo == fScintOMGeo.end()) {
      log_fatal_stream("Scintillator %s is not in station map!" << fSilentScint[i]);
    }

    const double rho0 = rock_bottom::GetDistToAxis(*ehypo.particle, scint_sil_posit);

    if ((rho0 >= core_radius) && (rho0 <= core_radius_2)) {
      I3RockBall ball;
      ball.SetPosition(&scint_sil_posit);
      const double p = 1. - fSignalModel->GetHitProbability(ball);
	if (p<std::numeric_limits<double>::min()){
		scint_sil_llh += log(std::numeric_limits<double>::min()); 
		}
	else{
		scint_sil_llh += log(p);
		} 
    }
  }



  ldf_parameters->SetParameterByName("Chi2_ldf", chi2_ldf);
  ldf_parameters->SetParameterByName("ndof_ldf", nDOF - ldf_free_params);
  ldf_parameters->SetParameterByName("ndof", nDOF - ldf_free_params);
  const double llh = scint_llh + scint_sil_llh;
  ldf_parameters->SetParameterByName("llh_ldf", llh);


  log_trace("log-likelihood (scint + sil): %f + %f -> %f (%f)",
            scint_llh / (fPulsesName1.size() ? fPulsesName1.size() : 1),
            scint_sil_llh / (fSilentScint.size() ? fSilentScint.size() : 1),
            llh / GetScintMultiplicity(), llh);

  return llh;
}

unsigned int I3RbLDFLikelihood::GetScintMultiplicity() {
  return fPulsesName1.size() + fSilentScint.size();
}
