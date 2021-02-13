#include <rock_bottom/interface/I3RbTimingLikelihood.h>

double I3RbTimingLikelihood::GetIceTopLogLikelihood(const I3EventHypothesis &ehypo) {

  fSignalModel->SetParameters(ehypo);
  I3ParameterMapPtr ldf_parameters = boost::dynamic_pointer_cast<I3ParameterMap>(ehypo.nonstd);
  
  double chi2_time = 0;
  double ndoffer = 0;
  int num =0;
  
  // HLCs
  double hlc_llh = 0;
  for (I3RecoPulseSeriesMap::const_iterator pIt = fPulseSeries1.begin();
       pIt != fPulseSeries1.end(); ++pIt) {
    const TankKey tankKey(pIt->first);
    const OMKey om = pIt->first;
    std::map<TankKey, I3TankGeo>::iterator geo = fStations.find(tankKey);

    I3Position posit = geo->second.position;
    num+=1;
    if (om.GetOM() <= 60){
	    log_info("Didn't find the OMKey (%i,%i) in I3Geometry", om.GetString(), om.GetOM());
    }
    if (geo == fStations.end()) {
      log_fatal_stream("Tank %s is not in station map!" << tankKey);
    }



    double local_delta_t = rock_bottom::GetDistToPlane(*ehypo.particle, posit, pIt->second[0].GetTime());
    const double signal = pIt->second[0].GetCharge();
    //log_info("charged %f",signal);
    //this is where i adding the second the second charge and time
    double local_delta_t2 = 0.0;
    double signal2 = 0.0;
    for (I3RecoPulseSeriesMap::const_iterator pIt2 = fPulseSeries1.begin();
     pIt2 != fPulseSeries1.end(); ++pIt2) {
       //const TankKey tankKey2(pIt2->first);
       const OMKey om2 = pIt2->first;
       if (om2.GetString() == om.GetString()){
	 if (om2.GetOM() != om.GetOM()){
    	    for (I3RecoPulseSeries::const_iterator it2 = pIt2->second.begin();
              it2 != pIt2->second.end(); ++it2) {
	        //double signal2 = it2->GetCharge();
	        const TankKey tankKey2(pIt2->first);
	        std::map<TankKey, I3TankGeo>::iterator geo2 = fStations.find(tankKey2);
            	signal2 = pIt2->second[0].GetCharge();
    		I3Position posit2 = geo2->second.position;
	        local_delta_t2 = rock_bottom::GetDistToPlane(*ehypo.particle, posit2, pIt2->second[0].GetTime());
    		const double rho = rock_bottom::GetDistToAxis(*ehypo.particle, posit);
    		//double local_curv = ldf_parameters->GetParameterByName("Ncurve")*(exp(-rho*rho/(ldf_parameters->GetParameterByName("Dcurve")*ldf_parameters->GetParameterByName("Dcurve"))) - 1.) - ldf_parameters->GetParameterByName("Amp")*rho*rho;


    		I3RockBall hlc_rockball;
    		hlc_rockball.SetCharge(signal);
    		hlc_rockball.SetDeltaT(local_delta_t);
    		hlc_rockball.SetCharge2(signal2);
    		hlc_rockball.SetDeltaT2(local_delta_t2);
    		hlc_rockball.SetPosition(&posit);
    		hlc_llh += fSignalModel->TimingLLH(hlc_rockball, ehypo);		
		//log_info("llh %f",hlc_llh);
    		chi2_time += fSignalModel->CalcChi2(hlc_rockball, ehypo, pIt->second[0].GetTime());
    		ndoffer +=1;
	    }
	 }
       }
    }   
    /*
    const double rho = rock_bottom::GetDistToAxis(*ehypo.particle, posit);
    double local_curv = ldf_parameters->GetParameterByName("Ncurve")*(exp(-rho*rho/(ldf_parameters->GetParameterByName("Dcurve")*ldf_parameters->GetParameterByName("Dcurve"))) - 1.) - ldf_parameters->GetParameterByName("Amp")*rho*rho;


    I3RockBall hlc_rockball;
    hlc_rockball.SetCharge(signal);
    hlc_rockball.SetDeltaT(local_delta_t);
    hlc_rockball.SetCharge2(signal2);
    hlc_rockball.SetDeltaT2(local_delta_t2);
    hlc_rockball.SetPosition(&posit);

    hlc_llh += fSignalModel->TimingLLH(hlc_rockball, ehypo);		
    chi2_time += fSignalModel->CalcChi2(hlc_rockball, ehypo, pIt->second[0].GetTime());
    ndoffer +=1;
    */
  }

  // Saturated
  double snum =0;
  double sat_llh = 0;
  log_trace("saturated tank likelihood");
  for (I3RecoPulseSeriesMap::const_iterator pIt = fSaturatedSeries.begin();
       fUseSaturated && pIt != fSaturatedSeries.end(); ++pIt) {
    const TankKey tankKey(pIt->first);
    std::map<TankKey, I3TankGeo>::iterator geo = fStations.find(tankKey);
    I3Position sat_posit = geo->second.position;
    //I3Position sat_posit = fSaturatedDOMs[snum];
    snum++;
    log_trace_stream("%s saturated" << tankKey);
    if (geo == fStations.end()) {
      log_fatal_stream("Tank %s is not in station map!" << tankKey);
    }
    const I3VEMCalibration vemCalib = fCalibration->vemCal.find(pIt->first)->second;
    const double pe_per_vem = vemCalib.pePerVEM/vemCalib.corrFactor;
    //const double signal = fLowGainSaturationThreshold/pe_per_vem;
    const OMKey om = pIt->first;
    double local_delta_t = rock_bottom::GetDistToPlane(*ehypo.particle, sat_posit, pIt->second[0].GetTime());


    // NEED ACTUAL deltaT



    
    const double sat_signal = pIt->second[0].GetCharge();
    //log_info("charged %f",sat_signal);
    //this is where i adding the second the second charge and time
    double local_delta_t2 = 0.0;
    double sat_signal2 = 0.0;
    for (I3RecoPulseSeriesMap::const_iterator pIt2 = fSaturatedSeries.begin();
     pIt2 != fSaturatedSeries.end(); ++pIt2) {
       //const TankKey tankKey2(pIt2->first);
       const OMKey om2 = pIt2->first;
       if (om2.GetString() == om.GetString()){
	 if (om2.GetOM() != om.GetOM()){
    	    for (I3RecoPulseSeries::const_iterator it2 = pIt2->second.begin();
              it2 != pIt2->second.end(); ++it2) {
	        //double signal2 = it2->GetCharge();
	        const TankKey tankKey2(pIt2->first);
	        std::map<TankKey, I3TankGeo>::iterator geo2 = fStations.find(tankKey2);
    		I3Position sat_posit2 = geo2->second.position;
            	sat_signal2 = pIt2->second[0].GetCharge();
	        local_delta_t2 = rock_bottom::GetDistToPlane(*ehypo.particle, sat_posit2, pIt2->second[0].GetTime());
    		I3RockBall sat_rockball;
    		sat_rockball.SetDeltaT(local_delta_t);
    		sat_rockball.SetPosition(&sat_posit);
    		sat_rockball.SetCharge(sat_signal);
    		sat_rockball.SetCharge2(sat_signal2);
    		sat_rockball.SetDeltaT2(local_delta_t2);

    		sat_llh += fSignalModel->TimingLLH(sat_rockball,ehypo);		
    		chi2_time += fSignalModel->CalcChi2(sat_rockball, ehypo, pIt->second[0].GetTime());
    		ndoffer +=1;
	    }
	 }
       }
    }   
    /*
    I3RockBall sat_rockball;
    sat_rockball.SetDeltaT(local_delta_t);
    sat_rockball.SetPosition(&sat_posit);
    sat_rockball.SetCharge2(signal2);
    sat_rockball.SetDeltaT2(local_delta_t2);

    sat_llh += fSignalModel->TimingLLH(sat_rockball,ehypo);		
    chi2_time += fSignalModel->CalcChi2(sat_rockball, ehypo, pIt->second[0].GetTime());
    ndoffer +=1;
    */
  }

  double llh = 0;
  llh = hlc_llh + sat_llh;
  //log_info("log-likelihood (hlc + sat): %f + %f -> %f (%f)",
  log_debug("log-likelihood (hlc + sat): %f + %f -> %f (%f)",
            hlc_llh,
            sat_llh,
            llh, llh);
  ldf_parameters->SetParameterByName("Chi2_time",chi2_time);
  ldf_parameters->SetParameterByName("ndof_time",ndoffer);
  // only works correctly if LDF LLH is called before timing. This should be fixed at some point.
  ldf_parameters->SetParameterByName("ndof", ndoffer+ldf_parameters->GetParameterByName("ndof"));
  ldf_parameters->SetParameterByName("llh_time",llh);

  return llh;
}


unsigned int I3RbTimingLikelihood::GetIceTopMultiplicity() {

  return fPulseSeries1.size() + fSaturatedSeries.size();
}
