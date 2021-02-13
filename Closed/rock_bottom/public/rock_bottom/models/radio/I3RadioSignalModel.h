/**
 * copyright  (C) 2019
 *
 * The Icecube Collaboration
 *
 * $Id: I3RadioSignalModel.h 173671 2019-06-03 17:59:13Z acoleman $
 *
 * \file I3RadioSignalModel.h
 *
 * \author Alan Coleman
 * \date 17 May 2019
 * \version $Revision: 173671 $
 * Last changed by $LastChangedBy: acoleman $ on $LastChangedDate: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 */

#ifndef __I3RadioSignalModel_h_
#define __I3RadioSignalModel_h_

static const char CVSId__I3RadioSignalModel[] =
  "$Id: I3RadioSignalModel.h 173671 2019-06-03 17:59:13Z acoleman $";


#include <dataclasses/physics/I3Particle.h>
#include <dataclasses/I3Position.h>
#include <dataclasses/I3Vector.h>
#include <string>

#include <rock_bottom/interface/I3RbSignalModel.h>
#include <rock_bottom/interface/I3RbLDFService.h>
//#include <rock_bottom/interface/I3TopFunction.h>

#include <cmath>

class I3RadioSignalModel: public I3RbSignalModel {
 public:
  I3RadioSignalModel(const std::string &name);
  I3RadioSignalModel(const I3Context &c);

  virtual ~I3RadioSignalModel() {}

  virtual void Configure();

  // These are the main methods (one can use the other, you decide wich)

  virtual double GetSignalCumulativeProbability(
    const I3RockBall& ball,
    const I3EventHypothesis& hypo,
    double signal) const;

  virtual double GetSignalLogCumulativeProbability(
    const I3RockBall& ball,
    const I3EventHypothesis& hypo,
    double signal) const;

  virtual double GetSignalMean(
    const I3RockBall& ball) const;

  virtual double GetLogSignalMean(
    const I3RockBall& ball) const;

  virtual double GetHitProbability(
    const I3RockBall& ball) const;
    
  virtual double GetSignalVariance(
    const I3RockBall& ball) const;

  virtual I3ParameterMapPtr GuessParameters(const I3Particle& axis,
      I3RecoPulseSeriesMapConstPtr hlcs,
      I3RecoPulseSeriesMapConstPtr slcs) const;

 protected:

  I3Vector<std::string> parameter_names_;
  I3Vector<double> default_parameters_;

 private:

  I3RbLDFServicePtr fLDF;
  //I3TopFunctionPtr fLTP;

  SET_LOGGER( "I3RadioSignalModel" );

}; // class I3RadioSignalModel

I3_POINTER_TYPEDEFS(I3RadioSignalModel);

#endif // __I3RadioSignalModel_h_
// Configure (x)emacs for this file ...
// Local Variables:
// mode:c++
// compile-command: "make -C .. -k"
// End:
