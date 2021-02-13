/**
 * copyright  (C) 2012
 *
 * The Icecube Collaboration
 *
 * $Id: I3TwoLDFSignalModel.h 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3TwoLDFSignalModel.h
 *
 * \author Javier Gonzalez
 * \date 19 Nov 2012
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

#ifndef __I3TwoLDFSignalModel_h_
#define __I3TwoLDFSignalModel_h_

static const char CVSId__I3TwoLDFSignalModel[] =
"$Id: I3TwoLDFSignalModel.h 173728 2019-06-04 17:46:14Z dsoldin $";

#include <rock_bottom/interface/I3RbSignalModel.h>

#include <photospline/I3SplineTable.h>
#include <rock_bottom/interface/I3RbLDFService.h>
#include <rock_bottom/snowservices/I3SnowCorrectionService.h>


class I3TwoLDFSignalModel: public I3RbSignalModel {
  public:
    I3TwoLDFSignalModel(const std::string &name);
    I3TwoLDFSignalModel(const I3Context &c);

    virtual ~I3TwoLDFSignalModel() {}

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
    
    virtual I3ParameterMapPtr GuessParameters(const I3Particle& axis,
        I3RecoPulseSeriesMapConstPtr hlcs,
        I3RecoPulseSeriesMapConstPtr slcs) const;

    // The following methods correspond to the tank response model. They could be factored out into another class, but interfaces might differ on each signal model implementation.
    double GetEMSignalLogProbability(double s, double mean_s, double  zenith, double rho) const;
    double GetMuonSignalLogProbability(double s, double mean_n, double  zenith) const;
    double GetEMSignalProbability(double s, double mean_s, double  zenith, double rho) const;
    double GetMuonSignalProbability(double s, double mean_n, double  zenith) const;
    double GetMuonSignalProbability2(double s, int n, double  zenith) const;
    double GetMuonSignalLogProbability2(double s, int n, double  zenith) const;
    void InitTankResponse(const std::string& dir);
    double GetTopSigmaSignal(double signal, double rho) const;


  protected:

    double TankResponseGetMuonMean(double zenith, int n) const;
    double TankResponseGetMuonWidth(double zenith, int n) const;

    double uptime_;
    std::vector<double> ltp_params_;

    std::vector<boost::shared_ptr<I3SplineTable> > muon_responses_;
    boost::shared_ptr<I3SplineTable> muon_response_mean_;
    boost::shared_ptr<I3SplineTable> muon_response_width_;

    // only for setting seeds?
    I3Vector<std::string> parameter_names_;
    I3Vector<double> default_parameters_;
    bool zenith_dependence;
    I3SnowCorrectionServiceBasePtr snow_service_;

  private:

    I3RbLDFServicePtr femLDF;
    I3RbLDFServicePtr fmuLDF;
  
    bool use_top_sigma;
    double core_radius_;
  
    SET_LOGGER( "I3TwoLDFSignalModel" );

}; // class I3TwoLDFSignalModel

I3_POINTER_TYPEDEFS(I3TwoLDFSignalModel);

#endif // __I3TwoLDFSignalModel_h_

