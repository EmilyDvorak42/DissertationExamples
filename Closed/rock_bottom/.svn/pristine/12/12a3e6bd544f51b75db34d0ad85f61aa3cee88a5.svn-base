/**
 * copyright  (C) 2019
 *
 * The Icecube Collaboration
 *
 * $Id: I3RbSignalModel.cxx 173671 2019-06-03 17:59:13Z acoleman $
 *
 * \file I3TopSignalModel.cxx
 *
 * \author Javier Gonzalez and Alan Coleman
 * \date 17 May 2019
 * \version $Revision: 173671 $
 * Last changed by $LastChangedBy: acoleman $ on $LastChangedDate: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 */

static const char CVSId[] =
  "$Id: I3RbSignalModel.cxx 173671 2019-06-03 17:59:13Z acoleman $";

#include <rock_bottom/interface/I3RbSignalModel.h>

using std::string;
using std::pow;
using std::exp;
using std::log10;
using std::log;

void I3RbSignalModel::SetParameters(const I3EventHypothesis &ehypo) {
  particle_ = ehypo.particle;

  ldf_parameters_ = boost::dynamic_pointer_cast<I3ParameterMap>(ehypo.nonstd);
  if (!ldf_parameters_) {
    log_fatal("Unrecognized non-std class in event hypothesis.");
  }
}

double I3RbSignalModel::GetSignalCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  return exp(GetSignalLogCumulativeProbability(ball, hypo, signal));
}

double I3RbSignalModel::GetSignalLogCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  return GetSignalLogCumulativeProbability(ball, hypo, signal);
}

double I3RbSignalModel::GetSignalMean(
  const I3RockBall& ball) const {
  return exp(GetLogSignalMean(ball));
}

double I3RbSignalModel::GetLogSignalMean(
  const I3RockBall& ball) const {
  return GetLogSignalMean(ball);
}

double I3RbSignalModel::GetHitProbability(
  const I3RockBall& ball) const {
  return GetHitProbability(ball);
}

double I3RbSignalModel::GetSignalProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  return exp(GetSignalLogProbability(ball, hypo, signal));
}

double I3RbSignalModel::GetSignalLogProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  return GetSignalLogProbability(ball, hypo, signal);
}

double I3RbSignalModel::CalcChi2(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  return CalcChi2(ball, hypo, signal);
}

double I3RbSignalModel::GetSignalVariance(
  const I3RockBall& ball) const {
  return GetSignalVariance(ball);
}

double I3RbSignalModel::TimingLLH(
  const I3RockBall& ball,
  const I3EventHypothesis &hypo) const {
  return TimingLLH(ball, hypo);
}