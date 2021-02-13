#include <rock_bottom/models/radio/I3RadioSignalModel.h>
#include <rock_bottom/I3RbUtilities.h>

I3RadioSignalModel::I3RadioSignalModel(const I3Context &c):
  I3RbSignalModel(c),
  parameter_names_(rock_bottom::GetNParameters()),
  default_parameters_(rock_bottom::GetNParameters()) {
  rock_bottom::FillParameterNames(parameter_names_);

  AddParameter("LDF", "LDF service to use", "");
  //ddParameter("LTP", "Local Trigger Probability function. Silent stations are ignored if this is empty.", "");

}

I3RadioSignalModel::I3RadioSignalModel(const std::string &name):
  I3RbSignalModel(name),
  parameter_names_(rock_bottom::GetNParameters()),
  default_parameters_(rock_bottom::GetNParameters()) {
  rock_bottom::FillParameterNames(parameter_names_);

  AddParameter("LDF", "LDF service to use", "");
  //AddParameter("LTP", "Local Trigger Probability function. Silent stations are ignored if this is empty.", "");
}

void I3RadioSignalModel::Configure() {
  log_info("Configuring signal model (%s)", GetName().c_str());

  GetParameter( "LDF",  fLDF);
  //GetParameter( "LTP",  fLTP);
}

double I3RadioSignalModel::GetSignalCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  return 0;
}

double I3RadioSignalModel::GetSignalLogCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  return 0;
}

double I3RadioSignalModel::GetSignalMean(
  const I3RockBall& ball) const {

  return 0;
}

double I3RadioSignalModel::GetLogSignalMean(
  const I3RockBall& ball) const {

  return 0;
}

double I3RadioSignalModel::GetHitProbability(
  const I3RockBall& ball) const {

  return 0;
}

double I3RadioSignalModel::GetSignalVariance(
  const I3RockBall& ball) const {

  return 0;
}

I3ParameterMapPtr I3RadioSignalModel::GuessParameters(const I3Particle& axis,
    I3RecoPulseSeriesMapConstPtr hlcs,
    I3RecoPulseSeriesMapConstPtr slcs) const {

  //Make a copy because this is const func
  I3Vector<double> parameters = default_parameters_;

  parameters[0] = 1.; //S125

  log_trace("Guessing parameters");
  for (unsigned int i = 0; i != parameters.size(); ++i) {
    log_trace("   - par_[%d] = %f", i, parameters[i]);
  }

  return I3ParameterMapPtr(new I3ParameterMap("RadioSignalModel", parameters, parameter_names_));
}
