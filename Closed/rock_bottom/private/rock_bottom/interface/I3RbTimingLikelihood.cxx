#include <rock_bottom/interface/I3RbTimingLikelihood.h>

#include <icetray/I3SingleServiceFactory.h>

typedef I3SingleServiceFactory<I3RbTimingLikelihood, I3EventLogLikelihoodBase> I3RbTimingLikelihoodFactory;
I3_SERVICE_FACTORY(I3RbTimingLikelihoodFactory);

I3RbTimingLikelihood::I3RbTimingLikelihood(const I3Context &c):
  I3RbLikelihoodBase(c) {
}
