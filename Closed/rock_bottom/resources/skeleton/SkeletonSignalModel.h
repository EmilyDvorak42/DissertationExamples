//This file should go in rock_bottom/public/rock_bottom/models/mydet/

/*
* \version $Revision: 173671 $
* Last changed by $LastChangedBy: acoleman $ on $LastChangedDate: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
*/

#ifndef __I3SkeletonSignalModel_h_
#define __I3SkeletonSignalModel_h_

static const char CVSId__I3SkeletonSignalModel[] =
  "$Id: SkeletonSignalModel.h 173671 2019-06-03 17:59:13Z acoleman $";


#include <dataclasses/physics/I3Particle.h>
#include <dataclasses/I3Position.h>
#include <dataclasses/I3Vector.h>
#include <string>

#include <rock_bottom/interface/I3RbSignalModel.h>
#include <rock_bottom/interface/I3TopLDFService.h>
#include <rock_bottom/interface/I3TopFunction.h>

#include <cmath>


class I3SkeletonSignalModel: public I3RbSignalModel {
 public:
  I3SkeletonSignalModel(const std::string &name);
  I3SkeletonSignalModel(const I3Context &c);

  virtual ~I3SkeletonSignalModel() {}

  virtual void Configure();

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

  virtual double GetSignalProbability(
    const I3RockBall& ball,
    const I3EventHypothesis& hypo,
    double signal) const;

  virtual double GetSignalLogProbability(
    const I3RockBall& ball,
    const I3EventHypothesis& hypo,
    double signal) const;

  virtual double CalcChi2(
    const I3RockBall& ball,
    const I3EventHypothesis& hypo,
    double signal) const;

  virtual double GetSignalVariance(
    const I3RockBall& ball) const;

  virtual double TimingLLH(
    const I3RockBall& ball,
    const I3EventHypothesis &hypo,
    const double rho) const;

  virtual I3ParameterMapPtr GuessParameters(const I3Particle& axis,
      I3RecoPulseSeriesMapConstPtr hlcs,
      I3RecoPulseSeriesMapConstPtr slcs) const;

 protected:

  I3Vector<std::string> parameter_names_;
  I3Vector<double> default_parameters_;

 private:

  I3TopLDFServicePtr fLDF;
  I3TopFunctionPtr fLTP;

  double core_radius_;

  SET_LOGGER( "I3SkeletonSignalModel" );

}; // class I3SkeletonSignalModel

I3_POINTER_TYPEDEFS(I3SkeletonSignalModel);

#endif
