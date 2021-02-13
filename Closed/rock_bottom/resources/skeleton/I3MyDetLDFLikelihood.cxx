//This file should go in rock_bottom/private/rock_bottom/interface/mydet/

#include <rock_bottom/interface/I3RbLDFLikelihood.h>

using namespace std;

double I3RbLDFLikelihood::GetMyDetLogLikelihood(const I3EventHypothesis &ehypo) {
  //Do whatever calculations you need in order to return the event loglikelihood

  fSignalModel->SetParameters(ehypo);
  log_trace("Starting mydet likelihood calculation");

  return 0;
}

unsigned int I3RbLDFLikelihood::GetMyDetMultiplicity() {
  return 0;
}
