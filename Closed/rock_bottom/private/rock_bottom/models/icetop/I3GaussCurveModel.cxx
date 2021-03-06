/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3GaussCurveModel.cxx 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3GaussCurveModel.cxx
 *
 * \author Javier Gonzalez
 * \date 28 Jan 2013
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

static const char CVSId[] =
  "$Id: I3GaussCurveModel.cxx 173728 2019-06-04 17:46:14Z dsoldin $";

#include <rock_bottom/models/icetop/I3GaussCurveModel.h>
#include <rock_bottom/I3RbUtilities.h>
#include <icetray/I3SingleServiceFactory.h>

typedef I3SingleServiceFactory<I3GaussCurveModel, I3RbSignalModel> GaussCurveModel;
I3_SERVICE_FACTORY(GaussCurveModel);

using std::string;
using std::pow;
using std::exp;
using std::log10;
using std::log;

I3GaussCurveModel::I3GaussCurveModel(const I3Context &c):
  I3RbSignalModel(c),
  parameter_names_(rock_bottom::GetNParameters()),
  default_parameters_(rock_bottom::GetNParameters()) {

  rock_bottom::FillParameterNames(parameter_names_);
}


I3GaussCurveModel::I3GaussCurveModel(const std::string &name):
  I3RbSignalModel(name),
  parameter_names_(rock_bottom::GetNParameters()),
  default_parameters_(rock_bottom::GetNParameters())
 {
}


void
I3GaussCurveModel::Configure() {
  log_info("Configuring signal model (%s)", GetName().c_str());
}


double I3GaussCurveModel::GetSignalLogCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  // Not Used, Just Declared
  return 0;
}

double I3GaussCurveModel::GetSignalCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  // Not Used, Just Declared
  return 0;
}

double I3GaussCurveModel::GetSignalMean(
  const I3RockBall& ball) const {
  return pow(10., GetLogSignalMean(ball));
}

double I3GaussCurveModel::GetLogSignalMean(
  const I3RockBall& ball) const {
  // Not Used, Just Declared
  return 0;
}

double I3GaussCurveModel::GetHitProbability(
  const I3RockBall& ball) const {
  // Not Used, Just Declared
  return 0;
}

double I3GaussCurveModel::GetSignalLogProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  // Not Used, Just Declared
  return 0;
}

double I3GaussCurveModel::GetSignalVariance(
  const I3RockBall& ball) const{
  
  const I3Position pos = *(ball.GetPosition());
  const double rho = rock_bottom::GetDistToAxis(*particle_, pos);

  const double time1 = ball.GetDeltaT();
  const double time2 = ball.GetDeltaT2();
  const double charge1 = ball.GetCharge();
  const double charge2 = ball.GetCharge2();

  double mean_t = (time1+time2)/2.;
  double sum_1 = pow(time1 - mean_t,2.);
  double sum_2 = pow(time2 - mean_t,2.);
  double q_sum = charge1+charge2;
  double local_sigma_t = 4.0*(sqrt(sum_1+sum_2)/pow(q_sum,1.))+1.22;  //Emily
  //double local_sigma_t = 2.92 + ((3.77e-4)*rho*rho); 
  return pow(local_sigma_t, 2.);


}

double I3GaussCurveModel::TimingLLH(
  const I3RockBall& ball, 
  const I3EventHypothesis &hypo) const {

  /*
  * This calculates the curvature fluctuations based on the shower front curvature in Laputop
  * Two sigmas are available, and due to the use of the parameters, any can be varied
  */

  I3ParticlePtr my_part = hypo.particle;
  const I3Position pos = *(ball.GetPosition()); 
  const double rho = rock_bottom::GetDistToAxis(*my_part, pos);
  const double deltaT = ball.GetDeltaT();
  
  I3ParameterMapPtr ldf_parameters = boost::dynamic_pointer_cast<I3ParameterMap>(hypo.nonstd);
  double expectedTime = ldf_parameters->GetParameterByName("Ncurve") * (exp(-rho * rho / (ldf_parameters->GetParameterByName("Dcurve") * ldf_parameters->GetParameterByName("Dcurve"))) - 1.) - ldf_parameters->GetParameterByName("Amp") * rho * rho;
  //log_info("p0 %f p1 %f p2 %f",ldf_parameters->GetParameterByName("Ncurve"),ldf_parameters->GetParameterByName("Dcurve"),ldf_parameters->GetParameterByName("Amp"));
  //log_info("expectedTime %f",expectedTime);
  double local_sigma_t =  sqrt(GetSignalVariance(ball));
  //log_info("deltaT %f expectedTime %f local_sigma_t %f",deltaT, expectedTime,local_sigma_t);
  double local_delta_t = (deltaT - expectedTime) / local_sigma_t;
  //log_info("local_sigma_t %f",local_sigma_t);
  //log_info("local_delta_t %f",local_delta_t);
  //log_info("deltat %f %f",local_curv, deltaT);
  //log_info("delta t %f",local_delta_t);
  return -(local_delta_t*local_delta_t / 2.) - log(local_sigma_t);
}

I3ParameterMapPtr I3GaussCurveModel::GuessParameters(
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
  parameters[0] = log_charge;
  parameters[1] = 2.;
  //parameters[5] = 125.;
  parameters[18] = 0.30264;
  //parameters[19] = 118.1;
  //parameters[20] = 19.41;

  log_trace("Guessing parameters");
  for (unsigned int i = 0; i != parameters.size(); ++i) {
    log_trace("   - par_[%d] = %f", i, parameters[i]);
  }

  return I3ParameterMapPtr(new I3ParameterMap("GaussCurveModel", parameters, parameter_names_));
}


double I3GaussCurveModel::CalcChi2(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double time) const {

  const I3Position pos = *(ball.GetPosition());

  I3ParticlePtr my_part = hypo.particle;
  const double deltaT = rock_bottom::GetDistToPlane(*particle_, pos, time);
  const double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  I3ParameterMapPtr ldf_parameters = boost::dynamic_pointer_cast<I3ParameterMap>(hypo.nonstd);
  double local_curv = ldf_parameters->GetParameterByName("Ncurve") * (exp(-rho * rho / (ldf_parameters->GetParameterByName("Dcurve") * ldf_parameters->GetParameterByName("Dcurve"))) - 1.) - ldf_parameters->GetParameterByName("Amp") * rho * rho;
  double local_sigma_t =  sqrt(GetSignalVariance(ball));
  //double local_sigma_t =  1.;
  double local_delta_t = (deltaT - local_curv) / local_sigma_t;

  double time_chi2 = local_delta_t*local_delta_t;

  return time_chi2;
}

