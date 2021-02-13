#include <rock_bottom/interface/I3RbLikelihoodBase.h>

#include <dataclasses/I3MapOMKeyMask.h>

void I3RbLikelihoodBase::ConstructScint() {
  fMinSignal = 0.5;
  fUseSilent = true;
}

void I3RbLikelihoodBase::ConfigureScint() {
  log_trace("Configuring likelihood (%s)", GetName().c_str());
  log_trace("ScintillatorPulses %s",  fPulsesName1.c_str());
}

void I3RbLikelihoodBase::SetScintGeometry(const I3Geometry &geometryScint) {
  log_trace("Setting scintillator geometry in likelihood (%s)", GetName().c_str());
  fScintOMGeo.clear();

  for (I3OMGeoMap::const_iterator scintIt = geometryScint.omgeo.begin();
       scintIt != geometryScint.omgeo.end(); ++scintIt) {
    const OMKey scintkey = OMKey(scintIt->first);
    fScintOMGeo[scintkey] = scintIt->second;
  }
}

void I3RbLikelihoodBase::SetScintEvent(const I3Frame &frame) {
  log_trace("Setting event in likelihood (%s)", GetName().c_str());

  if (frame.Has("ScintillatorArrayGeometry")) {
    const I3Geometry& geo = frame.Get<I3Geometry>("ScintillatorArrayGeometry");
    SetScintGeometry(geo);
  } else {
    log_fatal("There is no ScintillatorArrayGeometry in the frame! Aborting.");
    return;
  }

  if (frame.Has(fPulsesName1)) {
    fPulseSeries1 = GetScintPulses(frame, fPulsesName1);
  } else {
    log_debug("No Scintillator Pulses in Frame. (%s)", fPulsesName1.c_str());
    fPulseSeries1.clear();
  }

  log_debug("adding silent scintillators");


  fSilentScint.clear();

  for (std::map<OMKey, I3OMGeo>::iterator scintIt = fScintOMGeo.begin();
       scintIt != fScintOMGeo.end(); ++scintIt) {
    const OMKey scintkey = scintIt->first;
    const I3OMGeo geo = scintIt->second;
    if (fPulseSeries1.find(scintkey) == fPulseSeries1.end() &&
        std::find(fSilentScint.begin(), fSilentScint.end(), scintkey) == fSilentScint.end()) {

      fSilentScint.push_back(scintkey);
    }
  }
}

I3RecoPulseSeriesMap
I3RbLikelihoodBase::GetScintPulses(const I3Frame& frame, std::string name)
const {
  /*
    This method does the following to all pulse series maps add
    the charge of all pulses for each OM and put them as the first
    and only pulse in the pulse series.
   */

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
    OMKey dom_key = pIt->first;
    double signal = 0;
    I3OMGeo om = om_map.find(dom_key)->second;
    bool keeper = false;
    for (I3RecoPulseSeries::iterator it = pIt->second.begin();
         it != pIt->second.end(); ++it) {
      if ((it->GetCharge() > fMinSignal) && (it->GetTime() == it->GetTime()) ) {
        keeper = true;
        signal += it->GetCharge();
      }
    }

    if (keeper == false) {
      result.erase(pIt);
    }
  }
  //log_info("ibefore fix %i",result.size());
  //~ log_info("Number of pulses.... %i",result.size());
  return result;
}

I3RecoPulseSeriesMap
I3RbLikelihoodBase::GetScintSaturatedPulses(const I3Frame& frame, std::string name)
//const
{

  I3RecoPulseSeriesMap a;
  return a;
}