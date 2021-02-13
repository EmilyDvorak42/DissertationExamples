//This file should go in rock_bottom/private/rock_bottom/models/mydet/

#include <rock_bottom/models/I3SkeltonSignalModel.h>

#include <rock_bottom/I3TopRockBottomUtilities.h>

I3SkeletonSignalModel::I3SkeletonSignalModel(const I3Context &c):
  I3RbSignalModel(c),
  parameter_names_(rock_bottom::GetNParameters()),
  default_parameters_(rock_bottom::GetNParameters()) {
  rock_bottom::FillParameterNames(parameter_names_);

  AddParameter("LDF", "LDF service to use", "");

}

I3SkeletonSignalModel::I3SkeletonSignalModel(const std::string &name):
  I3RbSignalModel(name),
  parameter_names_(rock_bottom::GetNParameters()),
  default_parameters_(rock_bottom::GetNParameters()) {
  rock_bottom::FillParameterNames(parameter_names_);

  AddParameter("LDF", "LDF service to use", "");
}

void I3SkeletonSignalModel::Configure() {
  log_info("Configuring signal model (%s)", GetName().c_str());

  GetParameter( "r_ref",  new_r_ref);
  GetParameter( "LDF",  fLDF);
}

double I3SkeletonSignalModel::GetSignalCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  return 0;
}

double I3SkeletonSignalModel::GetSignalLogCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  return 0;
}

double I3SkeletonSignalModel::GetSignalMean(
  const I3RockBall& ball) const {

  return 0;
}

double I3SkeletonSignalModel::GetLogSignalMean(
  const I3RockBall& ball) const {

  return 0;
}

double I3SkeletonSignalModel::GetHitProbability(
  const I3RockBall& ball) const {

  return 0;
}

double I3SkeletonSignalModel::GetSignalProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  return 0;
}

double I3SkeletonSignalModel::GetSignalLogProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  return 0;
}

double I3SkeletonSignalModel::CalcChi2(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  return 0;
}

double I3RbSignalModel::GetSignalVariance(
  const I3RockBall& ball) const {
  return GetSignalVariance(ball);
}

double I3SkeletonSignalModel::TimingLLH(
  const I3RockBall& ball,
  const I3EventHypothesis &hypo,
  const double rho) const {

  return 0;
}

I3ParameterMapPtr I3SkeletonSignalModel::GuessParameters(const I3Particle& axis,
    I3RecoPulseSeriesMapConstPtr hlcs,
    I3RecoPulseSeriesMapConstPtr slcs) const {

  //Make a copy because this is const func
  I3Vector<double> parameters = default_parameters_;

  parameters[0] = 1.; //S125

  log_trace("Guessing parameters");
  for (unsigned int i = 0; i != parameters.size(); ++i) {
    log_trace("   - par_[%d] = %f", i, parameters[i]);
  }

  return I3ParameterMapPtr(new I3ParameterMap("SkeletonSignalModel", parameters, parameter_names_));
}
