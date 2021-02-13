/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3ScintSignalModel.cxx 173801 2019-06-06 16:30:34Z agnieszka.leszczynska $
 *
 * \file I3ScintSignalModel.cxx
 *
 * \author Javier Gonzalez
 * \date 28 Jan 2013
 * \version $Revision: 173801 $
 * Last changed by $LastChangedBy: agnieszka.leszczynska $ on $LastChangedDate: 2019-06-06 11:30:34 -0500 (Thu, 06 Jun 2019) $
 */

static const char CVSId[] =
  "$Id: I3ScintSignalModel.cxx 173801 2019-06-06 16:30:34Z agnieszka.leszczynska $";

#include <rock_bottom/models/scint/I3ScintSignalModel.h>
#include <rock_bottom/I3RbUtilities.h>
#include <icetray/I3SingleServiceFactory.h>
#include <boost/math/special_functions/gamma.hpp>

typedef I3SingleServiceFactory<I3ScintSignalModel, I3RbSignalModel> ScintSignalModel;
I3_SERVICE_FACTORY(ScintSignalModel);

using std::pow;
using std::exp;
using std::log;

I3ScintSignalModel::I3ScintSignalModel(const I3Context &c):
  I3RbSignalModel(c),
  parameter_names_(rock_bottom::GetNParameters()),
  default_parameters_(rock_bottom::GetNParameters()) {

  rock_bottom::FillParameterNames(parameter_names_);

  AddParameter("LDF", "LDF service to use", "");
}


I3ScintSignalModel::I3ScintSignalModel(const std::string &name):
  I3RbSignalModel(name),
  parameter_names_(rock_bottom::GetNParameters()),
  default_parameters_(rock_bottom::GetNParameters()) {

  rock_bottom::FillParameterNames(parameter_names_);

  AddParameter("LDF", "LDF service to use", "");
}


void I3ScintSignalModel::Configure() {
  log_info("Configuring signal model (%s)", GetName().c_str());

  GetParameter( "LDF",  fLDF);
}


double I3ScintSignalModel::GetSignalLogCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  // All signal < fMinSignal are treated as silent pulses?
  return log(GetSignalCumulativeProbability(ball, hypo, signal));
}


double I3ScintSignalModel::GetSignalCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  const I3Position pos = *(ball.GetPosition());

  const double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  double expectedSignal = fLDF->GetSignal(rho, 0, false, ldf_parameters_);
  const double sigma_sat = (0.5*(1./cos(particle_->GetDir().GetZenith()))+0.82)*sqrt(std::max(1000., expectedSignal));
  const double p_sat = 0.5*(erfc((1000.-expectedSignal)/(sqrt(2.)*sigma_sat)));
  return p_sat;
}

// Get log(signal) from the provided LDF, NKG or DLP
double I3ScintSignalModel::GetSignalMean(
  const I3RockBall& ball) const {
  /*
    The underlying model _assumes_ log-normal distributions.
    This would be the corresponding mean. That does not make it right.
  */

  return exp(GetLogSignalMean(ball));
}

double I3ScintSignalModel::GetLogSignalMean(
  const I3RockBall& ball) const {

  const I3Position pos = *(ball.GetPosition());

  const double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  return fLDF->GetLogSignal(rho, 0, false, ldf_parameters_);
}


// Get hit probability from the provided ERF function
double I3ScintSignalModel::GetHitProbability(
  const I3RockBall& ball) const {

  const I3Position pos = *(ball.GetPosition());

  const double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  const double expectedSignal = fLDF->GetSignal(rho, 0, false, ldf_parameters_);
  const double logSexp = log10(expectedSignal);

  const double a = 0.25;
  const double b = 0.38;
  const double c1 = 0.51;
  const double c2 = 0.81;

  return 1. - a * (1. + erf((b - logSexp) / c1)) * (1. + tanh((b - logSexp) / c2));
}


double I3ScintSignalModel::GetSignalProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  return exp(GetSignalLogProbability(ball, hypo, signal));
}

double I3ScintSignalModel::GetSignalLogProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  const I3Position pos = *(ball.GetPosition());

  const double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  double expectedSignal = fLDF->GetSignal(rho, 0, false, ldf_parameters_);
  double sigma = sqrt(GetSignalVariance(ball));

  // Positive Gaussian
  const double delta 	= (signal - expectedSignal) / sigma;
  const double llh		= -((delta * delta) / 2. + log(2.*M_PI*sigma));
  return llh;
}


double I3ScintSignalModel::GetSignalVariance(const I3RockBall& ball)
const {
  const I3Position pos = *(ball.GetPosition());
  const double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  const double zenith = particle_->GetDir().GetZenith();
  const double signal = fLDF->GetSignal(rho, zenith, false, ldf_parameters_);
  if (signal > 0.) {
	return pow((0.5 * (1. / cos(zenith)) + 0.82) * sqrt(signal), 2);
  } 
  else {
    return pow(1.4, 2);
  }
}

I3ParameterMapPtr I3ScintSignalModel::GuessParameters(const I3Particle& axis,
    I3RecoPulseSeriesMapConstPtr hlcs,
    I3RecoPulseSeriesMapConstPtr slcs) const {

  I3Vector<double> parameters = default_parameters_;

  parameters[0] = 5.0;
  parameters[1] = 2.;
  parameters[5] = 200.;
  parameters[18] = 0.3;
  parameters[19] = 50.;
  parameters[20] = 15.;

  log_trace("Guessing parameters");
  for (unsigned int i = 0; i != parameters.size(); ++i) {
    log_trace("   - par_[%d] = %f", i, parameters[i]);
  }

  return I3ParameterMapPtr(new I3ParameterMap("ScintSignalModel", parameters, parameter_names_));
}


double I3ScintSignalModel::CalcChi2(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  I3Position pos = *(ball.GetPosition());

  double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  double expectedSignal = fLDF->GetSignal(rho, 0, false, ldf_parameters_);

  //Cut on lateral distances, we will fit LDF from 15-500m for scintillators
  // Again hard-coded values...

  const double core_radius_ = 5.;
  const double core_radius_2 = 800.;
  double sigma = 0;

  if (rho >= core_radius_ && rho <= core_radius_2) {
    //sigma = fLDF->GetTopSigmaSignal(expectedSignal, rho);
    sigma = sqrt(GetSignalVariance(ball));
  } else {
    return 0.;
  }
  const double delta = (signal - expectedSignal) / sigma;
  const double chi2 = delta * delta;
  return chi2;

}


