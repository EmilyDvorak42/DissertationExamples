#include <rock_bottom/interface/I3RbLikelihoodBase.h>

const double SAT_LG = 90000.;// Upper bound for LG in PE

void I3RbLikelihoodBase::ConstructIceTop() {
  fUseSaturated = true;
  fUseSilent = true;
  fMinSignal = 0.7;
}

void I3RbLikelihoodBase::ConfigureIceTop() {
  log_trace("Configuring likelihood (%s)", GetName().c_str());
  log_trace("IceTopPulses1 %s",  fPulsesName1.c_str());
  log_trace("IceTopPulses2 %s",  fPulsesName2.c_str());
}


void I3RbLikelihoodBase::SetIceTopGeometry( const I3Geometry &geometry ) {
  log_trace("Setting IceTop geometry in likelihood (%s)", GetName().c_str());

  fStations.clear();
  for (I3StationGeoMap::const_iterator stationIt = geometry.stationgeo.begin();
       stationIt != geometry.stationgeo.end(); ++stationIt) {
    const TankKey tank_a = TankKey(stationIt->first, TankKey::TankA);
    if (std::find(fBadTanks.begin(), fBadTanks.end(), tank_a) == fBadTanks.end()) {
      fStations[tank_a] = stationIt->second[TankKey::TankA];
      log_trace("String %d, Tank A: (%f, %f, %f)", stationIt->first,
                fStations[tank_a].position.GetX(), fStations[tank_a].position.GetY(), fStations[tank_a].position.GetZ()
               );
    }

    const TankKey tank_b = TankKey(stationIt->first, TankKey::TankB);
    if (std::find(fBadTanks.begin(), fBadTanks.end(), tank_b) == fBadTanks.end()) {
      fStations[tank_b] = stationIt->second[TankKey::TankB];
      log_trace("String %d, Tank B: (%f, %f, %f)", stationIt->first,
                fStations[tank_b].position.GetX(), fStations[tank_b].position.GetY(), fStations[tank_b].position.GetZ()
               );
    }
  }
}


void I3RbLikelihoodBase::SetIceTopEvent( const I3Frame &frame ) {
  log_trace("Setting event in likelihood (%s)", GetName().c_str());
  // this is the very first thing (it is used right after inside GetPulses and SetGeometry).
  
  // something is wrong with the dataclasses here. fix this! 
  if (frame.Has(fBadDetectorsName)) {
    I3VectorTankKeyConstPtr temp = frame.Get<I3VectorTankKeyConstPtr>(fBadDetectorsName);
    if (temp) {
      fBadTanks = *frame.Get<I3VectorTankKeyConstPtr>(fBadDetectorsName);
    } else {
      fBadTanks.clear();
    }
  } else {
    fBadTanks.clear();
  }

  if (frame.Has("I3Geometry")) {
    const I3Geometry& geo = frame.Get<I3Geometry>("I3Geometry");
    SetIceTopGeometry(geo);
  }

  fCalibration = frame.Get<I3CalibrationConstPtr>();
  fStatus = frame.Get<I3DetectorStatusConstPtr>();

  if (frame.Has(fPulsesName1)) {
    fPulseSeries1 = GetIceTopPulses(frame, fPulsesName1);
    fPulseSeriesDOMs1 = GetOMPosition(frame, fPulsesName1);
    fSaturatedSeries1 = GetIceTopSaturatedPulses(frame, fPulsesName1);
  } else {
    log_debug("No Pulses1 in Frame! (%s)", fPulsesName1.c_str());
    fPulseSeries1.clear();
    fPulseSeriesDOMs1.clear();
    fSaturatedSeries1.clear();
  }

  if (frame.Has(fPulsesName2)) {
    fPulseSeries2 = GetIceTopPulses(frame, fPulsesName2);
    fPulseSeriesDOMs2 = GetOMPosition(frame, fPulsesName2);
    fSaturatedSeries2 = GetIceTopSaturatedPulses(frame, fPulsesName2);
  } else {
    log_debug("No Pulses2 in Frame! (%s)", fPulsesName2.c_str());
    fPulseSeries2.clear();
    fPulseSeriesDOMs2.clear();
    fSaturatedSeries2.clear();
  }

  //fSaturatedSeries = MergeIceTopPulses(frame, fSaturatedSeries1, fSaturatedSeries2);
  // only saturated HLCs for now. should be fine though...
  fSaturatedSeries = fSaturatedSeries1;
  fSaturatedDOMs = GetOMPosition(frame, fPulsesName1);

  // Definition of "silent" used here: a pulse in the geometry with no pulse and that is not a bad tank.
  log_debug("adding silent tanks");
  const std::map<OMKey, I3DOMStatus> &status_map = fStatus->domStatus;

  fSilentTanks.clear();
  fSilentSnow.clear();
  fSilentDOMs.clear();
  std::ostringstream silent;
  for (std::map<TankKey, I3TankGeo>::iterator stationIt = fStations.begin();
       stationIt != fStations.end(); ++stationIt) {
    const TankKey key = stationIt->first;
    const OMKey odd_om(key.string, (key.tank == TankKey::TankA ? 61 : 63));
    const OMKey even_om(key.string, (key.tank == TankKey::TankA ? 62 : 64));

    // no working OM in this tank (required)
    if (status_map.find(odd_om) == status_map.end() && status_map.find(even_om) == status_map.end()) {
      continue;
    }

    // no high-gain OM in this tank (required until one implements trigger probability for LG DOMs)
    if ( !(status_map.find(odd_om) != status_map.end() && status_map.find(odd_om)->second.domGainType == I3DOMStatus::High) &&
         !(status_map.find(even_om) != status_map.end() && status_map.find(even_om)->second.domGainType == I3DOMStatus::High) ) {
      continue;
    }
    if (std::find(fBadTanks.begin(), fBadTanks.end(), key) != fBadTanks.end()) {
      continue;
    }

    if (fPulseSeries1.find(odd_om) != fPulseSeries1.end() ||
        fPulseSeries1.find(even_om) != fPulseSeries1.end() ||
        fPulseSeries2.find(odd_om) != fPulseSeries2.end() ||
        fPulseSeries2.find(even_om) != fPulseSeries2.end() ||
        fSaturatedSeries.find(odd_om) != fSaturatedSeries.end() ||
        fSaturatedSeries.find(even_om) != fSaturatedSeries.end()) {
      continue;
    }
    for (I3Vector<OMKey>::iterator omIt = stationIt->second.omKeyList_.begin();
         omIt != stationIt->second.omKeyList_.end(); ++omIt) {
      if (fPulseSeries1.find(*omIt) == fPulseSeries1.end() &&
          fPulseSeries2.find(*omIt) == fPulseSeries2.end() &&
          fSaturatedSeries.find(*omIt) == fSaturatedSeries.end() &&
          std::find(fSilentTanks.begin(), fSilentTanks.end(), key) == fSilentTanks.end()) {
        if (fPulseSeries1.size() > 0) {
          unsigned int omcheck = 61;
          if ((odd_om.GetOM() == omcheck) && (odd_om.GetString() != 39)) {
            const I3Geometry &geometry = frame.Get<I3Geometry>();
            I3StationGeoMap smap = geometry.stationgeo;
            double avgdepth = 0;
            I3StationGeoMap::const_iterator siter = smap.find(odd_om.GetString());
            if (siter == smap.end()) {
              log_fatal("Station %d doesn't exist in StationGeoMap!", odd_om.GetString());
            }
            // Get the depths of both tanks and average them
            const I3TankGeo& tankGeo0 = siter->second.at(0);
            const I3TankGeo& tankGeo1 = siter->second.at(1);
            avgdepth = 0.5 * (tankGeo0.snowheight + tankGeo1.snowheight);
            // Actually fill the internal inputdata container with NOT HIT tanks
            //log_info("odd %u %u", odd_om.GetString(),odd_om.GetOM());
            tankPulse no_pulse;
            no_pulse.omkey = odd_om;
            no_pulse.x = 0.5 * ((tankGeo0.position).GetX() + (tankGeo1.position).GetX());
            no_pulse.y = 0.5 * ((tankGeo0.position).GetY() + (tankGeo1.position).GetY());
            no_pulse.z = 0.5 * ((tankGeo0.position).GetZ() + (tankGeo1.position).GetZ());
            no_pulse.t = NAN;
            no_pulse.width = NAN;
            no_pulse.logvem = NAN;
            no_pulse.snowdepth = avgdepth;
            no_pulse.usepulsetime = false;
            fSilentSnow.push_back(avgdepth);
            fSilentDOMs.push_back(I3Position(no_pulse.x, no_pulse.y, no_pulse.z));
            fSilentTanks.push_back(key);// WHERE I NEED TO FIX AVERAGE SNOW
            silent << "(" << key.string << ", " << (key.tank == TankKey::TankA ? "A" : "B") << ") ";
          }
        } else {
          fSilentTanks.push_back(key);
          silent << "(" << key.string << ", " << (key.tank == TankKey::TankA ? "A" : "B") << ") ";
        }
      }
    }
  }
  log_debug_stream("Silent tanks: " << silent.str());
}

I3RecoPulseSeriesMap I3RbLikelihoodBase::GetIceTopPulses(
  const I3Frame& frame, 
  std::string name) const {
  
  /*
    This method does the following to all pulse series maps:
      - remove tanks that are in fBadTanks list.
      - Add the charge of all pulses for each OM and put them as the first and only pulse in the pulse series.
   */

  const I3Calibration &calibration = frame.Get<I3Calibration>(); // for saturation
  const std::map<OMKey, I3VEMCalibration> &vemcal_map = calibration.vemCal;
  const I3Geometry &geometry = frame.Get<I3Geometry>();
  const I3OMGeoMap& om_map = geometry.omgeo;
  I3RecoPulseSeriesMapConstPtr ptr;
  if (frame.Has(name)) {
    ptr = frame.Get<I3RecoPulseSeriesMapConstPtr>(name);
    if (!ptr) {
      I3RecoPulseSeriesMapMaskConstPtr mask = frame.Get<I3RecoPulseSeriesMapMaskConstPtr>(name);
      if (mask) ptr = mask->Apply(frame);
    }
  }
  if (!ptr)
    return I3RecoPulseSeriesMap();

  I3RecoPulseSeriesMap result = *ptr;
  I3RecoPulseSeriesMap::iterator do_not_use = result.begin();
  while (do_not_use != result.end()) {
    I3RecoPulseSeriesMap::iterator pIt = do_not_use++;
    TankKey tankKey(pIt->first);
    if (std::find(fBadTanks.begin(), fBadTanks.end(), tankKey) != fBadTanks.end()) {
      result.erase(pIt);
      continue;
    }
    OMKey dom_key = pIt->first;
    I3VEMCalibration vemCalib = vemcal_map.find(dom_key)->second;
    double pe_per_vem = vemCalib.pePerVEM / vemCalib.corrFactor;
    const double fSoftwareThreshold = -1.;// Upper bound for LG in PE (WHY -1?)
    double hg_sat = vemCalib.hglgCrossOver / pe_per_vem;
    double lg_sat = (SAT_LG / pe_per_vem);
    I3OMGeo om = om_map.find(dom_key)->second;
    double signal = 0;
    bool keeper = false;
    for (I3RecoPulseSeries::iterator it = pIt->second.begin();
         it != pIt->second.end(); ++it) {
      if ((it->GetCharge() > fSoftwareThreshold) &&
          (it->GetCharge() <= lg_sat) &&
          (it->GetTime() == it->GetTime()) ) {
        signal += it->GetCharge();
        keeper = true;
      } 
    }
    if (keeper == true) {
      pIt->second.resize(1);
      pIt->second[0].SetCharge(signal);
    } else {
      result.erase(pIt);
    }
    /*
    *this is where i adding the second the second charge and time

    //for (I3RecoPulseSeriesMap::const_iterator pIt2 = fPulseSeries1.begin();
    for (I3RecoPulseSeriesMap::iterator pIt2 = result.begin();
     pIt2 != result.end(); ++pIt2) {
       //const TankKey tankKey2(pIt2->first);
       const OMKey om1 = pIt->first;
       const OMKey om2 = pIt2->first;
       if (om2.GetString() == om1.GetString()){
	 if (om2.GetOM() != om1.GetOM()){
    	    for (I3RecoPulseSeries::iterator it2 = pIt2->second.begin();
              it2 != pIt2->second.end(); ++it2) {
	        double signal2 = it2->GetCharge();
            	pIt->second[0].SetCharge2(signal2);
	    }
	 }
       }
    }   

    */
  }
  
  return result;
}



I3RecoPulseSeriesMap  I3RbLikelihoodBase::GetIceTopSaturatedPulses(
  const I3Frame& frame, 
  std::string name) {

  /*
    This method does the following to all pulse series maps:
      - remove tanks that are in fBadTanks list.
      - Add the charge of all pulses for each OM and put them as the first and only pulse in the pulse series.
   */

  const I3Calibration &calibration = frame.Get<I3Calibration>(); // for saturation
  const std::map<OMKey, I3VEMCalibration> &vemcal_map = calibration.vemCal;
  const I3DetectorStatus &status = frame.Get<I3DetectorStatus>();
  const std::map<OMKey, I3DOMStatus> &status_map = status.domStatus;
  const I3Geometry &geometry = frame.Get<I3Geometry>();
  const I3OMGeoMap& om_map = geometry.omgeo;
  I3RecoPulseSeriesMapConstPtr ptr;
  if (frame.Has(name)) {
    ptr = frame.Get<I3RecoPulseSeriesMapConstPtr>(name);
    if (!ptr) {
      I3RecoPulseSeriesMapMaskConstPtr mask = frame.Get<I3RecoPulseSeriesMapMaskConstPtr>(name);
      if (mask)
        ptr = mask->Apply(frame);
    }
  }
  if (!ptr)
    return I3RecoPulseSeriesMap();

  I3RecoPulseSeriesMap result = *ptr;
  I3RecoPulseSeriesMap::iterator do_not_use = result.begin();
  while (do_not_use != result.end()) {
    I3RecoPulseSeriesMap::iterator pIt = do_not_use++;
    OMKey dom_key = pIt->first;
    I3OMGeo om = om_map.find(dom_key)->second;
    const TankKey tankKey(dom_key);
    if (std::find(fBadTanks.begin(), fBadTanks.end(), tankKey) != fBadTanks.end()) {
      result.erase(pIt);
      continue;
    }
    const I3DOMStatus::DOMGain gain = status_map.find(pIt->first)->second.domGainType;
    const I3VEMCalibration& vemCalib = vemcal_map.find(pIt->first)->second;
    const double pe_per_vem = vemCalib.pePerVEM / vemCalib.corrFactor;
    const double lg_sat = SAT_LG / pe_per_vem;
    double signal = 0;
    bool keeper = false;
    for (I3RecoPulseSeries::iterator it = pIt->second.begin();
         it != pIt->second.end(); ++it) {
      // check if it os high-gain and 'saturated'
      if (gain == I3DOMStatus::Low &&
          it->GetCharge() == it->GetCharge() &&
          it->GetTime() == it->GetTime() &&
          it->GetCharge() > lg_sat ) {
        signal += it->GetCharge();
        keeper = true;
      }
      // check if it is low-gain and saturated
      // this actually flags high-gain saturated DOMs (that had no low-gain corresponding signal)
      // as bad and therefore excludes them from the likelihood.
      // this effectively removes tank 39A always since it only has a high-gain DOM.
      else if (gain == I3DOMStatus::High &&
               it->GetCharge() != it->GetCharge() &&
               it->GetTime() == it->GetTime()) {
        if (std::find(fBadTanks.begin(), fBadTanks.end(), tankKey) == fBadTanks.end()) {
          fBadTanks.push_back(tankKey);
        }
      }
    }
    if (keeper == true) {
      pIt->second.resize(1);
      pIt->second[0].SetCharge(signal);
    } else {
      result.erase(pIt);
    }
  }
  return result;
}


I3RecoPulseSeriesMap I3RbLikelihoodBase::MergeIceTopPulses(
  const I3Frame& frame, 
  I3RecoPulseSeriesMap pulses1, 
  I3RecoPulseSeriesMap pulses2) const {
  
  // Merges two pulse series
  
  I3RecoPulseSeriesMap newMap;
  newMap.clear();
  I3RecoPulseSeriesMap::iterator do_not_use1 = pulses1.begin();
  while (do_not_use1 != pulses1.end()) {
    I3RecoPulseSeriesMap::iterator pIt1 = do_not_use1++;
    newMap[pIt1->first] = pIt1->second;
  }
  I3RecoPulseSeriesMap::iterator do_not_use2 = pulses2.begin();
  while (do_not_use2 != pulses2.end()) {
    I3RecoPulseSeriesMap::iterator pIt2 = do_not_use2++;
    newMap[pIt2->first] = pIt2->second;
  }
  return newMap;
}


I3VectorI3Position I3RbLikelihoodBase::GetOMPosition(
  const I3Frame& frame, 
  std::string name) const {
  
  //    Grabs OM position instead of Tank Position
  
  const I3Geometry &geometry = frame.Get<I3Geometry>();
  const I3OMGeoMap& om_map = geometry.omgeo;
  I3Position pos;
  I3VectorI3Position vec_pos;
  I3RecoPulseSeriesMapConstPtr ptr;
  if (frame.Has(name)) {
    ptr = frame.Get<I3RecoPulseSeriesMapConstPtr>(name);
    if (!ptr) {
      I3RecoPulseSeriesMapMaskConstPtr mask = frame.Get<I3RecoPulseSeriesMapMaskConstPtr>(name);
      if (mask) ptr = mask->Apply(frame);
    }
  }
  if (!ptr)
    return vec_pos;
    
  I3RecoPulseSeriesMap result = *ptr;
  for (I3RecoPulseSeriesMap::iterator pIt = result.begin();
       pIt != result.end(); ++pIt) {
    OMKey dom_key = pIt->first;
    I3OMGeo om = om_map.find(dom_key)->second;
    pos = om.position;
    vec_pos.push_back(pos);
  }
  return vec_pos;
}
