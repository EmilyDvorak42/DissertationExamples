/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3FrontScintModel.cxx 173801 2019-06-06 16:30:34Z agnieszka.leszczynska $
 *
 * \file I3FrontScintModel.cxx
 *
 * \author Javier Gonzalez
 * \date 28 Jan 2013
 * \version $Revision: 173801 $
 * Last changed by $LastChangedBy: agnieszka.leszczynska $ on $LastChangedDate: 2019-06-06 11:30:34 -0500 (Thu, 06 Jun 2019) $
 */

static const char CVSId[] =
  "$Id: I3FrontScintModel.cxx 173801 2019-06-06 16:30:34Z agnieszka.leszczynska $";

#include <rock_bottom/models/scint/I3FrontScintModel.h>
#include <rock_bottom/I3RbUtilities.h>
#include <icetray/I3SingleServiceFactory.h>

typedef I3SingleServiceFactory<I3FrontScintModel, I3RbSignalModel> FrontScintModel;
I3_SERVICE_FACTORY(FrontScintModel);

using std::string;
using std::pow;
using std::exp;
using std::log10;
using std::log;

I3FrontScintModel::I3FrontScintModel(const I3Context &c):
  I3RbSignalModel(c),
  parameter_names_(rock_bottom::GetNParameters()),
  default_parameters_(rock_bottom::GetNParameters()) {

  rock_bottom::FillParameterNames(parameter_names_);

}


I3FrontScintModel::I3FrontScintModel(const std::string &name):
  I3RbSignalModel(name),
  parameter_names_(rock_bottom::GetNParameters()),
  default_parameters_(rock_bottom::GetNParameters()) {

}


void I3FrontScintModel::Configure() {
  log_info("Configuring signal model (%s)", GetName().c_str());
}

double I3FrontScintModel::GetSignalCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  // Not Used, Just Declared
  return 0;
}

double I3FrontScintModel::GetSignalLogCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  // Not Used, Just Declared
  return 0;
}

double I3FrontScintModel::GetSignalMean(
  const I3RockBall& ball) const {
  return pow(10., GetLogSignalMean(ball));
}

double I3FrontScintModel::GetLogSignalMean(
  const I3RockBall& ball) const {
  // Not Used, Just Declared
  return 0;
}

double I3FrontScintModel::GetHitProbability(
  const I3RockBall& ball) const {
  // Not Used, Just Declared
  return 0;
}

double I3FrontScintModel::GetSignalLogProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  // Not Used, Just Declared
  return 0;
}

double I3FrontScintModel::GetSignalVariance(
  const I3RockBall& ball) const {

  const I3Position pos = *(ball.GetPosition());
  const double rho = rock_bottom::GetDistToAxis(*particle_, pos);

  const double sigma_t =  5.44 - 6.74e-2 * rho + 7.93e-4 * rho * rho; // from Agnieszka

  return pow(sigma_t, 2.);
}

double I3FrontScintModel::CalcChi2(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  const double time = signal;

  const I3Position pos = *(ball.GetPosition());

  // Need to fix this
  I3ParticlePtr my_part = hypo.particle;
  const double deltaT = rock_bottom::GetDistToPlane(*particle_, pos, time);
  const double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  I3ParameterMapPtr ldf_parameters = boost::dynamic_pointer_cast<I3ParameterMap>(hypo.nonstd);
  const double local_curv = ldf_parameters->GetParameterByName("Ncurve") * (exp(-rho * rho / (ldf_parameters->GetParameterByName("Dcurve") * ldf_parameters->GetParameterByName("Dcurve"))) - 1.) - ldf_parameters->GetParameterByName("Amp") * rho * rho;
  const double local_sigma_t = sqrt(GetSignalVariance(ball));
  const double local_delta_t = (deltaT - local_curv) / local_sigma_t;

  double time_chi2 = local_delta_t*local_delta_t;

  return time_chi2;
}


I3ParameterMapPtr I3FrontScintModel::GuessParameters(
  const I3Particle& axis,
  I3RecoPulseSeriesMapConstPtr hlcs,
  I3RecoPulseSeriesMapConstPtr slcs) const {

  double log_charge = 0;
  int pulses = 0;
  if (hlcs) {
    for (I3RecoPulseSeriesMap::const_iterator pIt = hlcs->begin();
         pIt != hlcs->end(); ++pIt) {
      for (I3RecoPulseSeries::const_iterator it = pIt->second.begin();
           it != pIt->second.end(); ++it) {
        log_charge += log10(it->GetCharge());
        pulses += 1;
      }
    }
  }
  if (slcs) {
    for (I3RecoPulseSeriesMap::const_iterator pIt = slcs->begin();
         pIt != slcs->end(); ++pIt) {
      for (I3RecoPulseSeries::const_iterator it = pIt->second.begin();
           it != pIt->second.end(); ++it) {
        log_charge += log10(it->GetCharge());
        pulses += 1;
      }
    }
  }

  log_charge /= pulses;

  I3Vector<double> parameters = default_parameters_;
  // These parameters will be changed...
  parameters[0] = 4.;
  parameters[1] = 2.;
  parameters[5] = 200.;
  parameters[18] = 0.30264;
  parameters[19] = 50.;
  parameters[20] = 15.;

  log_trace("Guessing parameters");
  for (unsigned int i = 0; i != parameters.size(); ++i) {
    log_trace("   - par_[%d] = %f", i, parameters[i]);
  }

  return I3ParameterMapPtr(new I3ParameterMap("FrontScintModel", parameters, parameter_names_));
}


double
I3FrontScintModel::TimingLLH(
  const I3RockBall& ball,
  const I3EventHypothesis &hypo) const {

  const double deltaT = ball.GetDeltaT();
  const I3Position pos = *(ball.GetPosition());
  const double rho = rock_bottom::GetDistToAxis(*particle_, pos);

  I3ParticlePtr my_part = hypo.particle;
  I3ParameterMapPtr ldf_parameters = boost::dynamic_pointer_cast<I3ParameterMap>(hypo.nonstd);
  double local_curv = ldf_parameters->GetParameterByName("Ncurve") * (exp(-rho * rho / (ldf_parameters->GetParameterByName("Dcurve") * ldf_parameters->GetParameterByName("Dcurve"))) - 1.) - ldf_parameters->GetParameterByName("Amp") * rho * rho;

  const double local_sigma_t = sqrt(GetSignalVariance(ball));
  double local_delta_t = (deltaT - local_curv) / local_sigma_t;
  return local_delta_t*local_delta_t / 2. + log(2.*M_PI*local_sigma_t);
}
