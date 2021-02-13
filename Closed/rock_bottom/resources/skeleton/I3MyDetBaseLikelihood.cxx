//This file should go in rock_bottom/private/rock_bottom/interface/mydet/

#include <rock_bottom/interface/I3RbLikelihoodBase.h>

void I3RbLikelihoodBase::ConstructMyDet() {
  //Add whatever you would normally call in a constructor here
  //For instance AddParameter(...) if such a parameter does not already exist
}

void I3RbLikelihoodBase::ConfigureMyDet() {
  //Add whatever you would normally call in a Configure() here
  //For instance GetParameter(...) if such a call doesn't exist in I3RbLikelihoodBase
}

void I3RbLikelihoodBase::SetMyDetGeometry(const I3Geometry &geometry) {
  //You can load stuff from the geometry in here
}

void I3RbLikelihoodBase::SetMyDetEvent(const I3Frame &frame) {
  //Get stuff from the frame, organize your pulses, etc
  if (frame.Has(fPulsesName1)) {
    fPulseSeries1.clear();
    fPulseSeries1 = GetMyDetPulses(frame, fPulsesName1);
  } else {
    log_error("No Pulses1 in Frame! (%s)", fPulsesName1.c_str());
  }
}

I3RecoPulseSeriesMap I3RbLikelihoodBase::GetMyDetPulses(const I3Frame& frame, std::string name) const {
  I3RecoPulseSeriesMap dummy;
  return dummy;
}
