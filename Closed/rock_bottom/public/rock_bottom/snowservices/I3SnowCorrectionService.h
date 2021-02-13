#ifndef I3SNOWSERVICE_H_INCLUDED
#define I3SNOWSERVICE_H_INCLUDED

/**
 *
 * @file I3SnowCorrectionService.h
 * @brief declaration of the I3SnowCorrectionService classes
 *
 * (c) 2007 the IceCube Collaboration
 * $Id: I3SnowCorrectionService.h 173671 2019-06-03 17:59:13Z acoleman $
 *
 * @version $Revision: 173671 $
 * @date $Date: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 * @author kath
 *
 */

#include <string>
#include <icetray/I3Logging.h>
#include <icetray/I3ServiceBase.h>
#include <dataclasses/physics/I3Particle.h>
#include <dataclasses/I3Position.h>

#include "rock_bottom/snowservices/tankPulse.h"
#include <rock_bottom/I3ParameterMap.h>
#include <recclasses/I3LaputopParams.h>
#include <cmath>
#include "rock_bottom/snowservices/SnowCorrectionDiagnostics.h"
#include "rock_bottom/snowservices/I3SnowCorrectionService.h"
/**
 * @class I3SnowCorrectionServiceBase
 * @brief Service (generic base class) to provide snow attenuation to IceTop reconstructors
 *
 */
class I3SnowCorrectionServiceBase : public I3ServiceBase {

 public:
  
  // constructors and destructors
  I3SnowCorrectionServiceBase(const std::string& name) : I3ServiceBase(name) {}
  I3SnowCorrectionServiceBase(const I3Context &c) : I3ServiceBase(c) {}
  virtual ~I3SnowCorrectionServiceBase() {}
  
  /// Do the calculation!  These vary from derived class to derived class
  /// Default = do nothing. (The "Null" snow correction)
  virtual double AttenuationFactor(const I3Position& pos,
                                   double snowDepth,
                                   const I3Particle& hypoth,
                                   const I3ParameterMap& params)
                                   //const I3LaputopParams& params)
    const
  { return 1.0; }

  // Fill the "snow diagnostics" object; this will be called by Laputop at the end.
  virtual void FillSnowDiagnostics(I3ComboSnowCorrectionDiagnosticsPtr diag, 
                                   I3ParticleConstPtr hypoth,
                                   I3ParameterMapConstPtr paramPtr)
                                   //I3LaputopParamsConstPtr paramPtr)
    const
  {}

  // for Laputop
  double CalculateAttenuatedLogS(double oldlogS,
				 const I3Position& pos,
                                 double snowdepth, 
                                 I3ParticleConstPtr hypoth,
                                 I3ParameterMapConstPtr paramPtr)
                                 //I3LaputopParamsConstPtr paramPtr)
    const
  {
    //log_info("rock_bottom SNOW x %f y %f z %f signal %f snow depth %f result %f", pos.GetX(), pos.GetY(),pos.GetZ(),oldlogS, snowdepth,AttenuationFactor(pos, snowdepth, *hypoth, *paramPtr));
    return oldlogS + std::log10(AttenuationFactor(pos, snowdepth, *hypoth, *paramPtr));
  }
  //{ return oldlogS + std::log10(AttenuationFactor(I3Position(tp.x, tp.y, tp.z), tp.snowdepth, *hypoth)); }
  //{ return oldlogS + std::log10(AttenuationFactor(I3Position(tp.x, tp.y, tp.z), tp.snowdepth, *hypoth, *paramPtr)); }

 protected:

  SET_LOGGER( "rock bottom" );

};


//---------------- SIMPLE ("LAMBDA") SNOW CORRECTION ---------------------
/**
 * @class I3SimpleSnowCorrectionService
 * @brief This one just attenuates by exp(-slantdepth/lambda), where "lambda" is a configurable parameter
 *
 */
class I3ComboSnowCorrectionService : public I3SnowCorrectionServiceBase {
 public:
  
  /// default constructor for unit tests
  I3ComboSnowCorrectionService(const std::string& name, double lambda);
  /// constructor I3Tray
  I3ComboSnowCorrectionService(const I3Context &c);
  /// destructor
  virtual ~I3ComboSnowCorrectionService(){}
  
  void Configure();
  
  /// Setter function for Lambda
  void ResetLambda(double newlambda);
  double GetLambda() const { return fLambda_; }
  
  /// Do the calculation!
  virtual double AttenuationFactor(const I3Position&,
                                   double,
				   const I3Particle&,
                                   const I3ParameterMap&) const;
                                   //const I3LaputopParams&) const;

  virtual void FillSnowDiagnostics(I3ComboSnowCorrectionDiagnosticsPtr,
                                   I3ParticleConstPtr,
                                   I3ParameterMapConstPtr) const;
                                   //I3LaputopParamsConstPtr) const;

 private:

  static const std::string LAMBDA_TAG;
  static const double DEFAULT_SIMPLE_LAMBDA;
  
  // Internal variables
  double fLambda_;

};

//---------------- BORS ---------------------
/**
 * @class I3BORSSnowCorrectionService
 * @brief This one implements Kath's BORS function
 *
 */
class I3borsSnowCorrectionService : public I3SnowCorrectionServiceBase {
 public:
  
  /// default constructor for unit tests
  I3borsSnowCorrectionService(const std::string& name, bool fEMonly);
  /// constructor I3Tray
  I3borsSnowCorrectionService(const I3Context &c);
  /// destructor
  virtual ~I3borsSnowCorrectionService(){}
  
  void Configure();

  /// Do the calculation!
  virtual double AttenuationFactor(const I3Position&,
                                   double,
                                   const I3Particle&,
                                   const I3ParameterMap&) const;
                                   //const I3LaputopParams&) const;

  virtual void FillSnowDiagnostics(I3ComboSnowCorrectionDiagnosticsPtr diag,
                                   I3ParticleConstPtr hypoth,
                                   I3ParameterMapConstPtr paramPtr) const;
                                   //I3LaputopParamsConstPtr paramPtr) const;

  // Additional functions
  double DominantExponentialSlope(double r, double t) const;
  double TurnoverExponentialSlope(double r, double t) const;
  double Turnover_c0(double r, double t) const;
  double FractionEM(double r, double logS125) const;
  double T_from_beta_zenith(double beta, double zenith) const;

  // Getter functions (may be useful for diagnostics?
  double GetTStage() const { return t_; }

  // Setter function: so you can send it tstage directly, and
  // don't have to compute T from beta/zenith (for instance, Javier's two-LDF)
  // You'd want to call this BEFORE calling CalculateAttenuatedS.
  // WARNING: may do strange things if one service is being called by multiple modules!
  void SetTStage(double myt) {
    t_ = myt;
    t_set_externally_ = 1;
  }
  void UnsetTStage() { t_set_externally_ = 0; }

 private:

  static const std::string EM_ONLY_TAG;

  // User parameters
  bool fEMonly_;

  // Internal variables
  mutable double t_;
  bool t_set_externally_;

};


I3_POINTER_TYPEDEFS( I3SnowCorrectionServiceBase );
I3_POINTER_TYPEDEFS( I3ComboSnowCorrectionService );
I3_POINTER_TYPEDEFS( I3borsSnowCorrectionService );

#endif
