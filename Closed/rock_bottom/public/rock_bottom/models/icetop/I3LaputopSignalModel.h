/**
 * copyright  (C) 2012
 *
 * The Icecube Collaboration
 *
 * $Id: I3LaputopSignalModel.h 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3LaputopSignalModel.h
 *
 * \author Javier Gonzalez
 * \date 19 Nov 2012
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

#ifndef __I3LaputopSignalModel_h_
#define __I3LaputopSignalModel_h_

static const char CVSId__I3LaputopSignalModel[] =
"$Id: I3LaputopSignalModel.h 173728 2019-06-04 17:46:14Z dsoldin $";

#include <rock_bottom/interface/I3RbSignalModel.h>
#include <rock_bottom/interface/I3RbLDFService.h>
#include <rock_bottom/snowservices/I3SnowCorrectionService.h>


class I3LaputopSignalModel: public I3RbSignalModel {
  public:
    I3LaputopSignalModel(const std::string &name);
    I3LaputopSignalModel(const I3Context &c);

    virtual ~I3LaputopSignalModel() {}

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

    virtual double GetSignalVariance(
      const I3RockBall& ball) const;      

    virtual double CalcChi2(
      const I3RockBall& ball,
      const I3EventHypothesis& hypo,
      double signal) const;

    virtual I3ParameterMapPtr GuessParameters(const I3Particle& axis,
        I3RecoPulseSeriesMapConstPtr hlcs,
        I3RecoPulseSeriesMapConstPtr slcs) const;
        
    double GetTopSigmaSignal(
      double signal, double rho) const;

  protected:
    I3Vector<std::string> parameter_names_;
    I3Vector<double> default_parameters_;
  
    I3SnowCorrectionServiceBasePtr snow_service_;

  private:
  
    I3RbLDFServicePtr fLDF;
    double new_r_ref;
    double core_radius_;

    SET_LOGGER( "I3LaputopSignalModel" );

}; // class I3LaputopSignalModel

I3_POINTER_TYPEDEFS(I3LaputopSignalModel);

#endif // __I3LaputopSignalModel_h_

