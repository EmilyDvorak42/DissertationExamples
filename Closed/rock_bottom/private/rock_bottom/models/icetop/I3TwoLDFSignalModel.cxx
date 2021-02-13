/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3TwoLDFSignalModel.cxx 173853 2019-06-07 22:16:19Z dsoldin $
 *
 * \file I3TwoLDFSignalModel.cxx
 *
 * \author Javier Gonzalez
 * \date 28 Jan 2013
 * \version $Revision: 173853 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-07 17:16:19 -0500 (Fri, 07 Jun 2019) $
 */

static const char CVSId[] =
  "$Id: I3TwoLDFSignalModel.cxx 173853 2019-06-07 22:16:19Z dsoldin $";


#include <rock_bottom/models/icetop/I3TwoLDFSignalModel.h>
#include <rock_bottom/I3RbUtilities.h>
#include <icetray/I3SingleServiceFactory.h>

#include <rock_bottom/snowservices/tankPulse.h>
#include <boost/filesystem.hpp>
#include <boost/math/special_functions/factorials.hpp>

typedef I3SingleServiceFactory<I3TwoLDFSignalModel, I3RbSignalModel> TwoLDFSignalModel;
I3_SERVICE_FACTORY(TwoLDFSignalModel);

using std::string;
using std::pow;
using std::exp;
using std::log10;
using std::log;
using std::vector;
namespace bfs = boost::filesystem;


static const double min_exponent = -250;
static const double max_exponent = 250;
static const double min_value = exp(min_exponent);
static const double max_value = exp(max_exponent);

namespace {
double max(double a, double b)
{ return (a > b ? a : b); }
}

I3TwoLDFSignalModel::I3TwoLDFSignalModel(const I3Context &c):
  I3RbSignalModel(c),
  uptime_(0.995),
  parameter_names_(rock_bottom::GetNParameters()),
  default_parameters_(rock_bottom::GetNParameters()),
  zenith_dependence(true),
  use_top_sigma(false)
{
  rock_bottom::FillParameterNames(parameter_names_); 

  AddParameter("r_ref", "Reference radius", 125.*I3Units::m);
  AddParameter("r_mu_ref", "Reference radius for muon LDF", 600.*I3Units::m);
  AddParameter("ZenithDependence", "Enable zenith dependent muon LDF", zenith_dependence);
  AddParameter("emLDF", "LDF service to use for e.m. part", "");
  AddParameter("muLDF", "LDF service to use for muon part", "");
  ltp_params_.push_back(-0.657577319);
  ltp_params_.push_back(0.14);
  AddParameter("SnowService", "Name of snow service", "");
  string data_dir(ROCKBOTTOM_DATA_DIR);
  AddParameter("TankResponseTablesDir", "Directory containing whetever files are required for tank response", data_dir + "/tank_response");
  AddParameter("UpTime", "Fraction of the time a tank is ready to launch.", uptime_);
  AddParameter("use_top_sigma", "Use Laputop (True) or simple (false) sigma.", use_top_sigma);
}


I3TwoLDFSignalModel::I3TwoLDFSignalModel(const std::string &name):
  I3RbSignalModel(name),
  uptime_(0.995),
  parameter_names_(rock_bottom::GetNParameters()),
  default_parameters_(rock_bottom::GetNParameters()),
  zenith_dependence(true),
  use_top_sigma(false)
{
  AddParameter("r_ref", "Reference radius", 125.*I3Units::m);
  AddParameter("r_mu_ref", "Reference radius for muon LDF", 600.*I3Units::m);
  AddParameter("ZenithDependence", "Enable zenith dependent muon LDF", zenith_dependence);
  AddParameter("emLDF", "LDF service to use for e.m. part", "");
  AddParameter("muLDF", "LDF service to use for muon part", "");
  ltp_params_.push_back(-0.657577319);
  ltp_params_.push_back(0.14);
  AddParameter("SnowService", "Name of snow service", "");
  string data_dir(ROCKBOTTOM_DATA_DIR);
  std::string dirname(ROCKBOTTOM_DATA_DIR);
  bfs::path dir(dirname + "/tank_response");
  if (bfs::exists(dir)) {
    InitTankResponse(dirname);
  } else {
    log_info("'%s' does not exist. Not initializing tank response", dirname.c_str());
  }
  AddParameter("TankResponseTablesDir", "Directory containing whetever files are required for tank response", data_dir + "/tank_response");
  AddParameter("UpTime", "Fraction of the time a tank is ready to launch.", uptime_);
  AddParameter("use_top_sigma", "Use Laputop (True) or simple (false) sigma.", use_top_sigma);
}


void I3TwoLDFSignalModel::Configure() {
  log_debug("Configuring signal model (%s)", GetName().c_str());
  GetParameter("r_ref", default_parameters_[5]);
  GetParameter("r_mu_ref", default_parameters_[6]);
  GetParameter("ZenithDependence", zenith_dependence);
  GetParameter( "emLDF",  femLDF);
  GetParameter( "muLDF",  fmuLDF);
  GetParameter("use_top_sigma", use_top_sigma);
  string dir;
  GetParameter("TankResponseTablesDir", dir);
  InitTankResponse(dir);
  string snow_service;
  GetParameter( "SnowService",  snow_service);
  if (context_.Has< I3SnowCorrectionServiceBase >( snow_service )) {
    snow_service_ = context_.Get< I3SnowCorrectionServiceBasePtr >(snow_service);
  } else {
    if (snow_service == "") {
      log_warn("NOT correcting for snow");
    } else {
      log_fatal("Snow service '%s' not found", snow_service.c_str());
    }
  }
}


void I3TwoLDFSignalModel::InitTankResponse(const std::string& d) {

  try {
    log_debug("Initializing tank response from %s", d.c_str());
    bfs::path dir(d);
    if (!bfs::exists(dir)) {
      log_fatal("Trying to initialize tank response from non-existent directory '%s'", d.c_str());
    }
    if (!bfs::is_directory(dir)) {
      log_fatal("Trying to initialize tank response from '%s', which is not a directory", d.c_str());
    }
    muon_responses_.clear();
    muon_response_mean_.reset();
    muon_response_width_.reset();
    vector<bfs::path> files;
    copy(bfs::directory_iterator(dir), bfs::directory_iterator(), back_inserter(files));
    sort(files.begin(), files.end());
    for (vector<bfs::path>::const_iterator it (files.begin()); it != files.end(); ++it) {
      const string f = it->string();
      const string name = it->filename().string();
      if (name.find("response-") == 0) {
        log_debug("Reading %d-muon response table from '%s'", int(muon_responses_.size() + 1), f.c_str());
        muon_responses_.push_back(boost::shared_ptr<I3SplineTable>(new I3SplineTable(f)));
      } else if (name == "gauss-mean.fits") {
        log_debug("Reading muon response mean from '%s'", f.c_str());
        muon_response_mean_ = boost::shared_ptr<I3SplineTable>(new I3SplineTable(f));
      } else if (name == "gauss-width.fits") {
        log_debug("Reading muon response width from '%s'", f.c_str());
        muon_response_width_ = boost::shared_ptr<I3SplineTable>(new I3SplineTable(f));
      }
    }
    if (!muon_response_mean_ || !muon_response_width_ || !muon_responses_.size()) {
      log_warn("Failed initialization somehow");
    }
  } catch (const bfs::filesystem_error& ex) {
    string what = ex.what();
    log_fatal("Failed trying to initialize tank response: %s", what.c_str());
  }
}


// This function is called for HLC and SLC llhs when the min signal given is > 0
// This is the most used function
double I3TwoLDFSignalModel::GetSignalLogProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  
  const I3TankGeo tankGeo = *(ball.GetTankGeo());
  const I3VEMCalibration vemCalib = *(ball.GetVEMCalibration());
  const I3Position pos = *(ball.GetPosition());
  const bool saturated = ball.GetSaturatedStatus();
  
  if (ldf_parameters_->GetParameterByName("Log10_S125") < -1. || ldf_parameters_->GetParameterByName("RhoMu") < 0.) {
    return -max_exponent;
  }
  // change position to shower coordinate system
  double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  
  // Reject Beta<0
  if (ldf_parameters_->GetParameterByName("Beta")<0) {
    return log(min_value);
  }
  
  const double core_radius_ = std::max(5.0,ldf_parameters_->GetParameterByName("r_ref") *
    pow(10, -ldf_parameters_->GetParameterByName("Beta")/(2.*ldf_parameters_->GetParameterByName("Kappa"))));
    
  if (rho < core_radius_) {
    rho = core_radius_;
  }
  const double zenith = particle_->GetDir().GetZenith();
  log_debug("   core (%f, %f, %f), pos (%f, %f, %f)",
            particle_->GetPos().GetX(), particle_->GetPos().GetY(), particle_->GetPos().GetZ(),
            pos.GetX(), pos.GetY(), pos.GetZ()
           );
  log_debug("      -> (%f, %f, %f) -> %f",
            pos_shower_cs.GetX(), pos_shower_cs.GetY(), pos_shower_cs.GetZ(),
            rho
           );

  // Muon expected signal in VEM is the muon density no matter the zenith angle
  // because the signal per muon is proportional to track_length
  // track_length ~ 1 VEM/tank_area
  // and the number of muons is rho*tank_area
  const double tank_area = I3Constants::pi * tankGeo.tankradius * tankGeo.tankradius * cos(zenith) + 2 * tankGeo.fillheight * tankGeo.tankradius * sin(zenith);
  const double expectedEMSignal = femLDF->GetSignal(rho, zenith, false, ldf_parameters_); // NKG EM LDF
  const double expectedMuonSignal = fmuLDF->GetSignal(rho, zenith, zenith_dependence, ldf_parameters_); // Muon LDF (muons per unit area!)
  // these sigmas are not used in the probability, just to estimate the integration step size for the convolution
  const double expectedMuonResponseSigma = TankResponseGetMuonWidth(zenith, int(expectedMuonSignal * tank_area + 1)); // the one is arbitrary, just so it is never 0
  const double expectedMuonSigma = sqrt(expectedMuonResponseSigma * expectedMuonResponseSigma + expectedMuonSignal * tank_area); // adding tank response sigma and sqrt(N) in quadrature
  double expectedEMSigma = 0.;
  if (use_top_sigma) {
    const double expectedEMSigma = GetTopSigmaSignal(log10(expectedEMSignal), rho);
  } else {
    const double expectedEMSigma = GetSignalVariance(ball);
  }

  // Calculate snow correction factor
  const tankPulse pulse(OMKey(), pos.GetX(), pos.GetY(), pos.GetZ() , 0., 0., 0., tankGeo.snowheight, false);
  double expectedEMSignalCorrected = expectedEMSignal;
  if (snow_service_) {
    const double snow_depth = tankGeo.snowheight;
    expectedEMSignalCorrected = snow_service_->CalculateAttenuatedLogS(log10(expectedEMSignal), pos, snow_depth, hypo.particle, ldf_parameters_);
    expectedEMSignalCorrected = pow(10, expectedEMSignalCorrected);
  }
  const double snowCorrectionFactor = expectedEMSignalCorrected / expectedEMSignal;

  log_debug("      S_em = %f, S_mu = %f", expectedEMSignal, expectedMuonSignal);
  double llh = 0;
  double norm = 0;
  if (expectedEMSigma < 0.1 * expectedMuonSigma) {
    log_trace("   Fixed EM");
    // treat em signal like a delta
    llh = GetMuonSignalLogProbability(signal - expectedEMSignalCorrected, expectedMuonSignal, zenith);
  } else if (expectedMuonSigma < 0.1 * expectedEMSigma) {
    log_trace("   Fixed mu");
    // treat muon signal like a delta
    llh = GetEMSignalLogProbability((signal - expectedMuonSignal) / snowCorrectionFactor, expectedEMSignal, zenith, rho);
  } else {
    log_trace("   convolving");
    // integrate over EM signal fraction range
    if (signal > 0 && expectedMuonSignal > 0 && expectedEMSigma> 0 ) {
      log_trace("signal = %f", signal);
      const double step = (expectedMuonSigma < expectedEMSigma ? expectedMuonSigma : expectedEMSigma) / 10;
      for (int i = 0; i <= signal / step; ++i) {
        double signal_em = i * step;  
        llh += GetEMSignalProbability(signal_em / snowCorrectionFactor, expectedEMSignal, zenith, rho) * GetMuonSignalProbability(signal - signal_em, expectedMuonSignal, zenith);
        norm += GetEMSignalProbability(signal_em / snowCorrectionFactor, expectedEMSignal, zenith, rho);
      }
    }
    if (norm > min_value) {
      llh = log(llh / norm + min_value);
    } else {
      llh = log(min_value);
    }
  }
  // discriminator trigger probability, saturation should be a factor like this as well
  log_trace("   calculating trigger probability");
  const double trigger_probabilty = 0.5 * (erf((signal - ltp_params_[0]) / (ltp_params_[1] * sqrt(2.))) + 1);
  if (trigger_probabilty == 0.0) {
    llh += log(min_value);
  }  else {
    llh += log(trigger_probabilty);
  }
  if (std::isnan(llh) == 1) {
    return log(min_value);
  } else {
    return llh;
  }
}

double I3TwoLDFSignalModel::CalcChi2(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  
  const I3TankGeo tankGeo = *(ball.GetTankGeo());
  const I3VEMCalibration vemCalib = *(ball.GetVEMCalibration());
  const I3Position pos = *(ball.GetPosition());
  const bool saturated = ball.GetSaturatedStatus();
  
  // Reject Beta<0
  if (ldf_parameters_->GetParameterByName("Beta")<0) {
    return log(min_value);
  }
  // change position to shower coordinate system
  double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  const double core_radius_ = std::max(5.0,ldf_parameters_->GetParameterByName("r_ref") *
    pow(10, -ldf_parameters_->GetParameterByName("Beta")/(2.*ldf_parameters_->GetParameterByName("Kappa"))));
    
  if (rho < core_radius_) {
    rho = core_radius_;
  }
  // Muon expected signal in VEM is the muon density no matter the zenith angle
  // because the signal per muon is proportional to track_length
  // track_length ~ 1 VEM/tank_area
  // and the number of muons is rho*tank_area
  const double zenith = particle_->GetDir().GetZenith();
  const double tank_area = I3Constants::pi * tankGeo.tankradius * tankGeo.tankradius * cos(zenith) + 2 * tankGeo.fillheight * tankGeo.tankradius * sin(zenith);
  const double expectedEMSignal = femLDF->GetSignal(rho, zenith, false, ldf_parameters_); // NKG EM LDF
  const double expectedMuonSignal = fmuLDF->GetSignal(rho, zenith, zenith_dependence, ldf_parameters_); // Muon LDF (muons per unit area!)
  const double expectedMuonResponseSigma = TankResponseGetMuonWidth(zenith, int(expectedMuonSignal * tank_area + 1)); // the one is arbitrary, just so it is never 0
  const double expectedMuonSigma = sqrt(expectedMuonResponseSigma * expectedMuonResponseSigma + expectedMuonSignal * tank_area); // adding tank response sigma and sqrt(N) in quadrature
  double expectedEMSigma = 0.;
  if (use_top_sigma) {
    expectedEMSigma = GetTopSigmaSignal(log10(expectedEMSignal), rho);
  } else {
    expectedEMSigma = GetSignalVariance(ball);
  }
  //Calculate snow correction factor
  double expectedEMSignalCorrected = expectedEMSignal;
  if (snow_service_) {
    const double snow_depth = tankGeo.snowheight;
    expectedEMSignalCorrected = snow_service_->CalculateAttenuatedLogS(log10(expectedEMSignal), pos, snow_depth, hypo.particle, ldf_parameters_);
    expectedEMSignalCorrected = pow(10, expectedEMSignalCorrected);
  }
  double sigma = sqrt(expectedMuonSigma * expectedMuonSigma + expectedEMSigma * expectedEMSigma);
  double delta = ( signal - (expectedEMSignalCorrected + expectedMuonSignal) ) / sigma ;
  double chi2 = delta * delta;
  return chi2;
}


double I3TwoLDFSignalModel::GetSignalLogCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  
  const I3VEMCalibration vemCalib = *(ball.GetVEMCalibration());
  const I3Position pos = *(ball.GetPosition());
  const bool saturated = ball.GetSaturatedStatus();
    
  // Reject Beta<0
  if (ldf_parameters_->GetParameterByName("Beta")<0) {
    return log(min_value);
  }
  
  if (saturated) {
    double rho = rock_bottom::GetDistToAxis(*particle_, pos);
    const double core_radius_ = std::max(5.0,ldf_parameters_->GetParameterByName("r_ref") *
      pow(10, -ldf_parameters_->GetParameterByName("Beta")/(2.*ldf_parameters_->GetParameterByName("Kappa"))));
    if (rho < core_radius_) {
      rho = core_radius_;
    }
    double sigma_sat = 0.;
    if (use_top_sigma) {
      sigma_sat = GetTopSigmaSignal(log10(signal), rho);
    } else {
      sigma_sat = GetSignalVariance(ball);
    }
    if (sigma_sat <= 0) {
      return log(min_value);
    }
    const double SAT_LG = 90000.;
    const double pe_per_vem = vemCalib.pePerVEM / vemCalib.corrFactor;
    const double lg_sat = SAT_LG / pe_per_vem;
    const double logsat = log10(SAT_LG / pe_per_vem);
    const double p_sat = 0.5 * (1. - erf((logsat - log10(signal)) / sqrt(2.) / sigma_sat) );
    if (std::isnan(p_sat) == 1) {
      return min_value;
    } else {
      return p_sat;
    }
  } else if (GetSignalCumulativeProbability(ball, hypo, signal) > 0.) {
    return log(GetSignalCumulativeProbability(ball, hypo, signal));
  } else {
    return log(min_value);
  }
}


double I3TwoLDFSignalModel::GetSignalCumulativeProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {
  
  const I3TankGeo tankGeo = *(ball.GetTankGeo());
  const I3VEMCalibration vemCalib = *(ball.GetVEMCalibration());
  const I3Position pos = *(ball.GetPosition());
  
  if (ldf_parameters_->GetParameterByName("Log10_S125") < -1. || ldf_parameters_->GetParameterByName("Beta") < 0. || ldf_parameters_->GetParameterByName("RhoMu") < 0.) {
    log_debug("   llh = %f", min_value);
    return min_value;
  }
  // change position to shower coordinate system
  double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  const double core_radius_ = std::max(5.0,ldf_parameters_->GetParameterByName("r_ref") *
    pow(10, -ldf_parameters_->GetParameterByName("Beta")/(2.*ldf_parameters_->GetParameterByName("Kappa"))));
  if (rho < core_radius_) {
    rho = core_radius_;
  }
  const double zenith = particle_->GetDir().GetZenith();
  log_trace("   core (%f, %f, %f), pos (%f, %f, %f)",
            particle_->GetPos().GetX(), particle_->GetPos().GetY(), particle_->GetPos().GetZ(),
            pos.GetX(), pos.GetY(), pos.GetZ()
           );
  log_trace("      -> (%f, %f, %f) -> %f",
            pos_shower_cs.GetX(), pos_shower_cs.GetY(), pos_shower_cs.GetZ(),
            rho
           );

  // Muon expected signal in VEM is the muon density no matter the zenith angle
  // because the signal per muon is proportional to track_length
  // track_length ~ 1 VEM/tank_area
  // and the number of muons is rho*tank_area
  const double tank_area = I3Constants::pi * tankGeo.tankradius * tankGeo.tankradius * cos(zenith) + 2 * tankGeo.fillheight * tankGeo.tankradius * sin(zenith);
  const double expectedEMSignal = femLDF->GetSignal(rho, zenith, false, ldf_parameters_); // NKG EM LDF
  const double expectedMuonSignal = fmuLDF->GetSignal(rho, zenith, zenith_dependence, ldf_parameters_); // Muon LDF (muons per unit area!)
  // these sigmas are not used in the probability, just to estimate the integration step size for the convolution
  const double expectedMuonResponseSigma = TankResponseGetMuonWidth(zenith, int(expectedMuonSignal * tank_area + 1)); // the one is arbitrary, just so it is never 0
  const double expectedMuonSigma = sqrt(expectedMuonResponseSigma * expectedMuonResponseSigma + expectedMuonSignal * tank_area); // adding tank response sigma and sqrt(N) in quadrature
  double expectedEMSigma = 0.;
  if (use_top_sigma) {
    expectedEMSigma = GetTopSigmaSignal(log10(expectedEMSignal), rho);
  } else {
    expectedEMSigma = GetSignalVariance(ball);
  }

  // snow correction factor
  const tankPulse pulse(OMKey(), pos.GetX(), pos.GetY(), pos.GetZ() , 0., 0., 0., tankGeo.snowheight, false);
  double expectedEMSignalCorrected = expectedEMSignal;
  if (snow_service_) {
    const double snow_depth = tankGeo.snowheight;
    expectedEMSignalCorrected = snow_service_->CalculateAttenuatedLogS(log10(expectedEMSignal), pos, snow_depth, hypo.particle, ldf_parameters_);
    expectedEMSignalCorrected = pow(10, expectedEMSignalCorrected);
  }
  
  if (expectedMuonSigma <= 0 || expectedEMSigma <= 0) {
      return min_value;
  }

  if (signal < 2) {
    // strictly speaking, I need to convolve the EM and the muon probability distribution functions, then multiply by trigger probability, and then calculate the CDF, but...
    const double N_mu = expectedMuonSignal * tank_area;
    if (N_mu > 5) {
      log_debug("   llh = %f", uptime_);
      return uptime_;
    }
    const double ds_em = signal - expectedEMSignalCorrected;
    const double p_em = 0.5 * (1. + erf(ds_em / (expectedEMSigma * sqrt(2.)))); // what happens to EM_sigma with snow attenuation? what about log10?
    // very very dummy trapezoid integration for poisson term up to three
    double p1 = 0.;
    double p2 = 0.;
    double p3 = 0.;
    double norm1 = 0.;
    double norm2 = 0.;
    double norm3 = 0.;
    double p1_0 = 0.;
    double p2_0 = 0.;
    double p3_0 = 0.;
    const double ds = 0.1;
    for (double s = 0.; s <= 10; s += ds) {
      const double p1_1 = GetMuonSignalProbability2(s, 1, zenith);
      const double p2_1 = GetMuonSignalProbability2(s, 2, zenith);
      const double p3_1 = GetMuonSignalProbability2(s, 3, zenith);
      if (s > signal) {
        p1 += (p1_1 + p1_0) / ds / 2;
        p2 += (p2_1 + p2_0) / ds / 2;
        p3 += (p3_1 + p3_0) / ds / 2;
      }
      norm1 += (p1_1 + p1_0) / ds / 2;
      norm2 += (p2_1 + p2_0) / ds / 2;
      norm3 += (p3_1 + p3_0) / ds / 2;
      p1_0 = p1_1;
      p2_0 = p2_1;
      p3_0 = p3_1;
    }
    p1 /= norm1;
    p2 /= norm2;
    p3 /= norm3;
    const double trigger_probabilty = 0.5 * (erf((signal - ltp_params_[0]) / (ltp_params_[1] * sqrt(2.))) + 1);

    // multiplying at the end is not correct as CDF calculation and p_trigger multiplication do not commute.
    const double p = max(min_value, uptime_ * trigger_probabilty * (exp(-N_mu) * p_em + N_mu * exp(-N_mu) * ((1 - p1) * p_em + p1) + N_mu * N_mu * exp(-N_mu) * ((1 - p2) * p_em + p2) / 2));
    if (std::isnan(p) == 1) {
      return min_value;
    } else {
      return p;
    }
  }
  if (signal > 100) {
    const double sigma = sqrt(expectedMuonSigma * expectedMuonSigma + expectedEMSigma * expectedEMSigma); // what happens to EM_sigma with snow attenuation? what about log10?
    const double ds = signal -  (TankResponseGetMuonMean(zenith, int(expectedMuonSignal * tank_area + 1)) + expectedEMSignalCorrected);
    const double p = max(min_value, uptime_ * 0.5 * (1 + erf(ds / (sigma * sqrt(2.)))));
    log_debug("   llh = %f", p);
    if (std::isnan(p) == 1) {
      return min_value;
    } else {
      return p;
    }
  }
  log_warn("Requested cumulative probability with signal between 2 and 100 VEM. This is not implemented by this class! Returning 1.");
  log_debug("   uptime = %f", uptime_);
  return uptime_;

}


double I3TwoLDFSignalModel::GetLogSignalMean(const I3RockBall& ball) const {

  return log(GetSignalMean(ball));
}


double I3TwoLDFSignalModel::GetHitProbability(const I3RockBall& ball) const {

  const double logvem_threshold = log10(0.1657);
  const I3Position pos = *(ball.GetPosition());
  double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  const double expectedSignal = GetSignalMean(ball);
  // what about two LDF?
  const double local_sigma = GetTopSigmaSignal(expectedSignal, rho);
  if (local_sigma <= 0) {
      return min_value;
  }
  const double p_hit = 0.5*(1 + erf((logvem_threshold-expectedSignal)/sqrt(2.)/local_sigma));
  if (std::isnan(p_hit) == 1) {
      return min_value;
  } else {
    return p_hit;
  }
  // what about snow correction?
  //return 0.5 * (erf((expectedSignal - ltp_params_[0]) / (ltp_params_[1] * sqrt(2.))) + 1);  
}


double I3TwoLDFSignalModel::GetSignalMean(const I3RockBall& ball) const {

  const I3Position pos = *(ball.GetPosition()); 
  double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  const double core_radius_ = std::max(5.0,ldf_parameters_->GetParameterByName("r_ref") *
    pow(10, -ldf_parameters_->GetParameterByName("Beta")/(2.*ldf_parameters_->GetParameterByName("Kappa"))));
  if (rho < core_radius_) {
    rho = core_radius_;
  }
  const double zenith = particle_->GetDir().GetZenith();
  return femLDF->GetSignal(rho, zenith, false, ldf_parameters_) + fmuLDF->GetSignal(rho, zenith, zenith_dependence, ldf_parameters_);
}


double I3TwoLDFSignalModel::GetEMSignalProbability(
  double s, 
  double mean_s, 
  double  zenith, 
  double rho) const {
  
  return exp(GetEMSignalLogProbability(s, mean_s, zenith, rho));
}


double I3TwoLDFSignalModel::GetEMSignalLogProbability(
  double s, 
  double mean_s, 
  double  zenith, 
  double rho) const {
  
  // gaussian with mean = mean_s
  const double delta_s = s - mean_s;
  double sigma = 0.;
  if (use_top_sigma) {
    // which signal?
    sigma = GetTopSigmaSignal(log10(mean_s), rho);
  } else {
    I3RockBall ball;
    const I3Position pos = particle_->GetPos();
    ball.SetPosition(&pos);
    sigma = GetSignalVariance(ball);
  }
  const double ret = -delta_s*delta_s / (2*sigma*sigma) - log(sigma) - 0.5 * log(2*M_PI);
  return ret;
}


double I3TwoLDFSignalModel::GetMuonSignalLogProbability2(
  double s, 
  int n, 
  double zenith) const {
  
  if (n <= 0) return -max_exponent;
  assert(muon_responses_.size() != 0);
  log_trace("          log(p_mu)(s = %f, n=%d)", s, n);
  if ((unsigned int)n < muon_responses_.size()) { // cast gets rid of warning, already checked n>0
    double x[2];
    x[0] = zenith;
    x[1] = s;
    double r(0);
    muon_responses_[n - 1]->Eval(x, &r);
    r = log10(r);
    return (r > min_exponent ? r : min_exponent);
  }
  // approximate by a gaussian
  const double mu_sigma = TankResponseGetMuonWidth(zenith, n);
  if (mu_sigma <= 0) {
    return log(min_value);
  }
  const double ds = s - TankResponseGetMuonMean(zenith, n);
  const double ret = -ds * ds / (2*mu_sigma*mu_sigma) - log(mu_sigma) - 0.5 * log(2*M_PI);
  log_trace("          p_mu = %f", ret);
  if (std::isnan(ret) == 1) {
    return log(min_value);
  } else {
    return ret;
  }
}

double I3TwoLDFSignalModel::GetMuonSignalProbability2(
  double s, 
  int n, 
  double zenith) const {
  
  return exp(GetMuonSignalLogProbability2(s, n, zenith));
}
  
double I3TwoLDFSignalModel::GetMuonSignalProbability(
  double s, 
  double mean_n, 
  double zenith) const {

  log_trace("       p_mu(s=%f, N=%f, zenith=%f)", s, mean_n, zenith);
  // the signal probability is the convolution of the Poisson distribution (for the number of muons)
  // and a normal distribution (tank response to an integer number of muons)

  if (mean_n > 50) {
    // if the mean N is large, the whole things is approximately gaussian
    const int N = mean_n;
    const double expectedMuonResponseSigma = TankResponseGetMuonWidth(zenith, N);
    const double expectedMuonResponseSignal = TankResponseGetMuonMean(zenith, N);
    const double sigma = sqrt(expectedMuonResponseSigma * expectedMuonResponseSigma + N); // adding response sigma and sqrt(N) in quadrature
    if (sigma <= 0 || std::isnan(sigma) == 1) {
      return min_value;
    }
    const double ds = expectedMuonResponseSignal - s;
    return exp(-ds*ds / (2*sigma*sigma)) / sqrt(2*M_PI) / sigma;
  }

  double r = 0;
  const double sigma = sqrt(mean_n);
  const int imin = (mean_n - 2 * sigma > 0 ? mean_n - 2 * sigma : 0);
  const int imax = (mean_n + 2 * sigma > 8 ? mean_n + 2 * sigma : 8);
  for (int i = imin; i <= imax; ++i) {
    const double poisson = pow(mean_n, i) * exp(-mean_n) / boost::math::factorial<double>(i);
    r += poisson * GetMuonSignalProbability2(s, i, zenith);
  }
  log_trace("       p_mu = %.20f", r);
  if (std::isnan(r) == 1) {
      return min_value;
  } else {
    return r;
  }
}


double I3TwoLDFSignalModel::GetMuonSignalLogProbability(double s, 
  double mean_n, 
  double  zenith) const {
  
  return log(GetMuonSignalProbability(s, mean_n, zenith) + 1e-15);
}


double I3TwoLDFSignalModel::TankResponseGetMuonMean(double zenith, int n) const {
  assert(muon_response_mean_);
  double x[1];
  x[0] = zenith;
  double m(0);
  muon_response_mean_->Eval(x, &m);
  return m * n;
}


double I3TwoLDFSignalModel::TankResponseGetMuonWidth(double zenith, int n) const {
  assert(muon_response_width_);
  double x[1];
  x[0] = zenith;
  double w(0);
  muon_response_width_->Eval(x, &w);
  return w * sqrt(n);
}


double I3TwoLDFSignalModel::GetSignalVariance(const I3RockBall& ball) const {

  // This is actually sigma. This is OK.
  
  // check signal model
  const I3Position pos = *(ball.GetPosition());
  const double rho = rock_bottom::GetDistToAxis(*particle_, pos);
  const double zenith = particle_->GetDir().GetZenith();
  return 0.6 * sqrt(femLDF->GetSignal(rho, zenith, false, ldf_parameters_));
}


double I3TwoLDFSignalModel::GetTopSigmaSignal(double signal, double rho) const {
  double a[2]     = {-.5519, -.078};
  double b[3]     = {-.373, -.658, .158};
  double trans[2] = {.340, 2.077};
  	 
  if(signal>trans[1]) signal=trans[1]; 
    if (signal<trans[0]) {
      return pow(10, a[0] + a[1] * signal);
    }
  else return pow(10, b[0] + b[1] * signal + b[2]*signal*signal);
}


double I3TwoLDFSignalModel::GetSignalProbability(
  const I3RockBall& ball,
  const I3EventHypothesis& hypo,
  double signal) const {

  return exp(GetSignalLogProbability(ball, hypo, signal));
}


I3ParameterMapPtr I3TwoLDFSignalModel::GuessParameters(
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
  parameters[0] = pow(10, log_charge);
  parameters[1] = 2.0;
  // This is really a ballpark guess. The molliere radius depends slightly on the zenith angle, atmosphere, etc.
  // Strictly speaking, it is a constant for each event so it might have to be fixed. Still, one can vary it.
  parameters[2] = 1.;
  parameters[5] = 125.*I3Units::m;
  parameters[6] = 320.;
  parameters[7] = 600.*I3Units::m;
  parameters[18] = 0.30264;
  parameters[19] = 118.1;
  parameters[20] = 19.41;
  log_trace("Guessing parameters");
  for (unsigned int i = 0; i != parameters.size(); ++i) {
    log_trace("   - par_[%d] = %f", i, parameters[i]);
  }

  return I3ParameterMapPtr(new I3ParameterMap(GetConfiguration().ClassName(), parameters, parameter_names_));
}

