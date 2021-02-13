#ifndef _rock_bottom_I3RbTimingLikelihood_h_
#define _rock_bottom_I3RbTimingLikelihood_h_

#include <rock_bottom/interface/I3RbLikelihoodBase.h>

class I3RbTimingLikelihood: public I3RbLikelihoodBase {

 public:

  I3RbTimingLikelihood(const I3Context &c);
  ~I3RbTimingLikelihood(){}

  //Declare the wrapper functions for each of the detector types
  //When you add a detector, you must declare what happens for each of these functions
#define DECLARE_WRAPPED(detType)\
  virtual double Get##detType##LogLikelihood(const I3EventHypothesis &ehypo);\
  virtual unsigned int Get##detType##Multiplicity();\

  DECLARE_WRAPPED(IceTop);
  DECLARE_WRAPPED(Scint);
  DECLARE_WRAPPED(Radio);
  //Add new detectors here//

#undef DECLARE_WRAPPED

  SET_LOGGER("RockBottom");
};

I3_POINTER_TYPEDEFS(I3RbTimingLikelihood);

#endif