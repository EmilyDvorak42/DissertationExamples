#include <rock_bottom/interface/I3RbTimingLikelihood.h>

double I3RbTimingLikelihood::GetScintLogLikelihood(const I3EventHypothesis &ehypo) {
  fSignalModel->SetParameters(ehypo);
  I3ParameterMapPtr ldf_parameters = boost::dynamic_pointer_cast<I3ParameterMap>(ehypo.nonstd);
  ldf_parameters->SetParameterByName("Dcurve", 50.0);
  ldf_parameters->SetParameterByName("Ncurve", 15.0);

  double scint_llh = 0;
  double scint_chi2_time = 0;
  //log_info("chi2 A %f",chi2_time);

  double ndoffer = 0;
  int num = 0;

  for (I3RecoPulseSeriesMap::const_iterator pIt = fPulseSeries1.begin();
       pIt != fPulseSeries1.end(); ++pIt) {
    const OMKey om = pIt->first;
    std::map<OMKey, I3OMGeo>::iterator geo = fScintOMGeo.find(om);



    // OMs for scintillators are 0-7
    num += 1;
    if (om.GetOM() >= 8) {
      log_info("Didn't find the OMKey (%i,%i) in I3Geometry", om.GetString(), om.GetOM());
    }
    if (geo == fScintOMGeo.end()) {
      log_fatal_stream("Scintillator %s is not in station map!" << om);
    }


    I3Position posit;
    posit = geo->second.position;

    double local_delta_t = rock_bottom::GetDistToPlane(*ehypo.particle, posit, pIt->second[0].GetTime());
    //double local_station_r = rock_bottom::GetDistToAxis(*ehypo.particle, posit);
    
    I3RockBall ball;
    ball.SetDeltaT(local_delta_t);
    ball.SetPosition(&posit);

    scint_llh += -1.*fSignalModel->TimingLLH(ball, ehypo);

    // For the moment there is no VEM calib for scintillators
    //~ const I3VEMCalibration vemCalib = fCalibration->vemCal.find(pIt->first)->second;
    scint_chi2_time += fSignalModel->CalcChi2(ball, ehypo, pIt->second[0].GetTime());
    ndoffer += 1;

  }

  double llh = 0;
  llh = scint_llh;
  //log_info("chi2 B %f",chi2_time);
  ldf_parameters->SetParameterByName("Chi2_time", scint_chi2_time);
  ldf_parameters->SetParameterByName("ndof_time", ndoffer);
  ldf_parameters->SetParameterByName("ndof", ndoffer+ldf_parameters->GetParameterByName("ndof"));
  ldf_parameters->SetParameterByName("llh_time", llh);

  return llh;
}

unsigned int I3RbTimingLikelihood::GetScintMultiplicity() {
  return fPulseSeries1.size();// + fSilentScintillators.size();
}
