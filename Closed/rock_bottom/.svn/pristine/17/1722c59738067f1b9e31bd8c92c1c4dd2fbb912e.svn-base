#include <rock_bottom/interface/I3RbLDFLikelihood.h>

using namespace std;

double I3RbLDFLikelihood::GetRadioLogLikelihood(const I3EventHypothesis &ehypo) {
  fSignalModel->SetParameters(ehypo);
  log_trace("Starting radio likelihood calculation");

  //Iterate through radio pulses
  for (I3AntennaDataMap::const_iterator it = fAntennaDataMap.begin();
       it != fAntennaDataMap.end(); it++) {
    const OMKey om = it->first;
    //Get the corresponding geometry for this key
    I3RadGeoMap::iterator radgeo = fRadGeo.find(om);
    if (radgeo == fRadGeo.end()) {
      log_fatal_stream("Radio %s is not in the RadGeoMap" << om);
    }

    const I3RadVectorD radVec = radgeo->second.position_;
    I3Position posit(radVec.GetX(), radVec.GetY(), radVec.GetZ());

  }

  return 0;
}

unsigned int I3RbLDFLikelihood::GetRadioMultiplicity() {
  return 1;
}