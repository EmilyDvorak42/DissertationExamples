/**
 * copyright  (C) 2012
 *
 * The Icecube Collaboration
 *
 * $Id: I3FrontScintModel.h 173671 2019-06-03 17:59:13Z acoleman $
 *
 * \file I3FrontScintModel.h
 *
 * \author Javier Gonzalez
 * \date 19 Nov 2012
 * \version $Revision: 173671 $
 * Last changed by $LastChangedBy: acoleman $ on $LastChangedDate: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 */

#ifndef __I3FrontScintModel_h_
#define __I3FrontScintModel_h_

static const char CVSId__I3FrontScintModel[] =
  "$Id: I3FrontScintModel.h 173671 2019-06-03 17:59:13Z acoleman $";

#include <rock_bottom/interface/I3RbSignalModel.h>


class I3FrontScintModel: public I3RbSignalModel {
 public:
  I3FrontScintModel(const std::string &name);
  I3FrontScintModel(const I3Context &c);

  virtual ~I3FrontScintModel() {}

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
    double signal) const
  { return std::exp(GetSignalLogProbability(ball, hypo, signal)); }

  virtual double GetSignalLogProbability(
    const I3RockBall& ball,
    const I3EventHypothesis& hypo,
    double signal) const;

  virtual double GetSignalVariance(
    const I3RockBall& ball) const;

  virtual double CalcChi2(
    const I3RockBall& ball,
    const I3EventHypothesis& hypo,
    double signal) const;

  virtual I3ParameterMapPtr GuessParameters(
    const I3Particle& axis,
    I3RecoPulseSeriesMapConstPtr hlcs,
    I3RecoPulseSeriesMapConstPtr slcs) const;

  virtual double TimingLLH(
    const I3RockBall& ball,
    const I3EventHypothesis &hypo) const;

 protected:
  const I3Configuration& GetConfiguration() const { return I3RbSignalModel::GetConfiguration(); }

  I3Vector<std::string> parameter_names_;
  I3Vector<double> default_parameters_;

 private:

  // I3RbLDFServicePtr fCRV;
  //I3TopFunctionPtr fLTP;

  SET_LOGGER( "I3FrontScintModel" );

}; // class I3FrontScintModel

I3_POINTER_TYPEDEFS(I3FrontScintModel);

#endif // __I3FrontScintModel_h_
// Configure (x)emacs for this file ...
// Local Variables:
// mode:c++
// compile-command: "make -C .. -k"
// End:
