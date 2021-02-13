#include <rock_bottom/interface/I3RbLikelihoodBase.h>

void I3RbLikelihoodBase::ConstructRadio() {
}

void I3RbLikelihoodBase::ConfigureRadio() {
}

void I3RbLikelihoodBase::SetRadioGeometry(const I3Geometry &geometry) {
  //Radio doesn't use I3Geometry
  //Nothing to do! :(
}

void I3RbLikelihoodBase::SetRadioEvent(const I3Frame &frame) {
  if (frame.Has("I3RadGeometry")) {
    fRadGeo.clear();
    fRadGeo = frame.Get<I3RadGeometryConstPtr>("I3RadGeometry")->radgeo;
  } else {
    log_fatal("Did not find the Radio Geometry!");
  }

  if (frame.Has(fPulsesName1)) {
    fAntennaDataMap = *(frame.Get<I3AntennaDataMapConstPtr>(fPulsesName1.c_str()));
  } else {
    log_debug("No Radio Traces in Frame. (%s)", fPulsesName1.c_str());
  }
}

I3RecoPulseSeriesMap I3RbLikelihoodBase::GetRadioPulses(const I3Frame& frame, std::string name) const {
  I3RecoPulseSeriesMap a;
  return a;
}