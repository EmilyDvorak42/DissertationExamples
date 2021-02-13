#include <rock_bottom/interface/I3RbLDFLikelihood.h>

#include <icetray/I3SingleServiceFactory.h>

typedef I3SingleServiceFactory<I3RbLDFLikelihood, I3EventLogLikelihoodBase> I3RbLDFLikelihoodFactory;
I3_SERVICE_FACTORY(I3RbLDFLikelihoodFactory);

I3RbLDFLikelihood::I3RbLDFLikelihood(const I3Context &c):
  I3RbLikelihoodBase(c) {
}

