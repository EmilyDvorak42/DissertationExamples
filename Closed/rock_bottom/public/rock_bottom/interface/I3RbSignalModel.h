/**
 * copyright  (C) 2012
 *
 * The Icecube Collaboration
 *
 * $Id: I3RbSignalModel.h 173671 2019-06-03 17:59:13Z acoleman $
 *
 * \file I3RbSignalModel.h
 *
 * \author Javier Gonzalez and Alan Coleman
 * \date 19 Nov 2012
 * \version $Revision: 173671 $
 * Last changed by $LastChangedBy: acoleman $ on $LastChangedDate: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 */

#ifndef __I3RbSignalModel_h_
#define __I3RbSignalModel_h_

static const char CVSId__I3RbSignalModel[] =
  "$Id: I3RbSignalModel.h 173671 2019-06-03 17:59:13Z acoleman $";


#include <rock_bottom/I3ParameterMap.h>
#include <dataclasses/I3MapOMKeyMask.h>
#include <dataclasses/physics/I3RecoPulse.h>
#include <rock_bottom/interface/I3RockBall.h>
#include <gulliver/I3EventHypothesis.h>
#include <icetray/I3ServiceBase.h>

/**
 *
 * \class I3RbSignalModel
 * Interface class to provide a likelihood model of the shower parameters.
 *
 * This class knows nothing of the IceTray/IceTop/IceCube data
 * structures, HLCs, SLCs, whatever. It only deals with the model of
 * the air shower and the response of a single tank. It encapsulates
 * things like the LDF, the hit/no-hit probability, the snow
 * correction, and saturation effects.
 *
 * To set the parameters, this class uses I3EventHypothesis. It abuses
 * the nonStd data member for all the extra information that is
 * required (LDF parameters, muon fraction...) so it is trivial to use
 * it with a Gulliver likelihood. We can consider subclassing
 * I3EventHypothesis.
 *
 * This interface takes I3TankGeo references mostly for snowhight,
 * and I3VEMCalibration references mostly for pePerVEM and corrFactor.
 * Maybe this requires some thinking.
 *
 * To implement your own, just inherit from this class and add
 * something like the following to your implementation file:
 *   typedef I3SingleServiceFactory<I3LaputopSignalModel, I3RbSignalModel> LaputopSignalModel;
 *   I3_SERVICE_FACTORY(LaputopSignalModel);
 */

class I3RbSignalModel: public I3ServiceBase {
 public:
  I3RbSignalModel(const std::string &name):
    I3ServiceBase(name)
  {}

  I3RbSignalModel(const I3Context &c):
    I3ServiceBase(c)
  {}
  virtual ~I3RbSignalModel() {}

  void SetParameters(const I3EventHypothesis &ehypo);

  // These are the main methods (one can use the other, you decide wich)

  //
  virtual double GetSignalCumulativeProbability(
    const I3RockBall& ball,
    const I3EventHypothesis& hypo,
    double signal) const;

  virtual double GetSignalLogCumulativeProbability(
    const I3RockBall& ball,
    const I3EventHypothesis& hypo,
    double signal) const;

  //
  virtual double GetSignalMean(
    const I3RockBall& ball) const;

  virtual double GetLogSignalMean(
    const I3RockBall& ball) const;

  //
  virtual double GetHitProbability(  //REMOVE THIS?
    const I3RockBall& ball) const;

  //
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

  virtual double TimingLLH(
    const I3RockBall& ball,
    const I3EventHypothesis &hypo) const;

  virtual I3ParameterMapPtr GuessParameters(const I3Particle& axis,
      I3RecoPulseSeriesMapConstPtr hlcs,
      I3RecoPulseSeriesMapConstPtr slcs) const = 0;

 protected:
  const I3Configuration& GetConfiguration() { return I3ServiceBase::GetConfiguration(); }
  const I3Configuration& GetConfiguration() const { return const_cast<I3RbSignalModel&>(*this).GetConfiguration(); }

  I3ParticlePtr particle_;
  I3ParameterMapPtr ldf_parameters_;

  SET_LOGGER( "RockBottom" );

}; // class I3RbSignalModel

I3_POINTER_TYPEDEFS(I3RbSignalModel);

#endif