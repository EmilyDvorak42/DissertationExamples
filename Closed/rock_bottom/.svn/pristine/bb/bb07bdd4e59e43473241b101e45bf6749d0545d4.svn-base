#ifndef _rock_bottom_I3RbLikelihoodBase_h_
#define _rock_bottom_I3RbLikelihoodBase_h_

#include <gulliver/I3EventLogLikelihoodBase.h>
#include <icetray/I3ServiceBase.h>
#include <icetray/I3SingleServiceFactory.h>

#include <dataclasses/geometry/I3Geometry.h>
#include <dataclasses/calibration/I3Calibration.h>
#include <dataclasses/status/I3DetectorStatus.h>

#include <dataclasses/geometry/I3TankGeo.h>
#include <gulliver/I3EventHypothesis.h>
#include <rock_bottom/I3RbUtilities.h>
#include <rock_bottom/interface/I3RbSignalModel.h>
#include "rock_bottom/snowservices/tankPulse.h"

#include <radcube/dataclasses/I3AntennaDataMap.h>
#include <radcube/dataclasses/I3RadGeometry.h>


class I3RbLikelihoodBase: public I3ServiceBase,
  public I3EventLogLikelihoodBase {


 public:
  I3RbLikelihoodBase(const I3Context &c);

  //Virtual functions for I3ServiceBase
  virtual void Configure();
  virtual const std::string GetName() const
  { return I3ServiceBase::GetName(); }

  //Virtual functions for I3EventLogLikelihoodBase
  virtual void SetGeometry(const I3Geometry &geometry);
  virtual void SetEvent(const I3Frame &frame);
  virtual double GetLogLikelihood(const I3EventHypothesis &ehypo);
  virtual unsigned int GetMultiplicity();

  //Declare the wrapper functions for each of the detector types
  //When you add a detector, you must declare what happens for each of these functions
#define DECLARE_WRAPPED(detType)\
  void Construct##detType();\
  void Configure##detType();\
  void Set##detType##Geometry(const I3Geometry &f);\
  void Set##detType##Event(const I3Frame &f);\
  I3RecoPulseSeriesMap Get##detType##Pulses(const I3Frame& frame, std::string name) const;\
  I3RecoPulseSeriesMap Get##detType##SaturatedPulses(const I3Frame& frame, std::string name);\
  virtual double Get##detType##LogLikelihood(const I3EventHypothesis &ehypo) = 0;\
  virtual unsigned int Get##detType##Multiplicity() = 0;\

  DECLARE_WRAPPED(IceTop);
  DECLARE_WRAPPED(Scint);
  DECLARE_WRAPPED(Radio);
  //Add new detectors here//

#undef DECLARE_WRAPPED

  rock_bottom::DetectorTypes fCurrentType;
  I3RbSignalModelPtr fSignalModel;

  ////////////////////////////////////////////////////
  /// Variables for all/many detector types
  ////////////////////////////////////////////////////

  bool fUseSilent;
  bool ToprecRepeat;
  double fMinSignal;
  bool fUseSaturated;


  std::string fPulsesName1;     //Name of "HLC" series
  std::string fPulsesName2;     //Name of "SLC" series
  std::string fBadDetectorsName; //Name of "BadTankList"

  I3RecoPulseSeriesMap fPulseSeries1;     //Holds "HLC" series
  I3RecoPulseSeriesMap fPulseSeries2;     //Holds "SLC" series
  I3RecoPulseSeriesMap fSaturatedSeries;  //Holds saturated series

  ////////////////////////////////////////////////////
  /// Variables for IceTop
  ////////////////////////////////////////////////////
  I3RecoPulseSeriesMap MergeIceTopPulses(const I3Frame& frame, I3RecoPulseSeriesMap pulses1, I3RecoPulseSeriesMap pulses2) const; \
  I3VectorI3Position GetOMPosition(const I3Frame& frame, std::string name) const; \

  double fLowGainSaturationThreshold;

  std::map<TankKey, I3TankGeo> fStations;
  I3VectorTankKey fBadTanks;
  I3VectorTankKey fSilentTanks;

  I3RecoPulseSeriesMap fSaturatedSeries1;
  I3RecoPulseSeriesMap fSaturatedSeries2;

  I3VectorI3Position fPulseSeriesDOMs1;
  I3VectorI3Position fPulseSeriesDOMs2;
  I3VectorI3Position fSaturatedDOMs1;
  I3VectorI3Position fSaturatedDOMs2;
  I3VectorI3Position fSaturatedDOMs;
  I3VectorI3Position fSilentDOMs;

  std::vector<double> fSilentSnow;  // for noHitLlh (same struct)

  I3CalibrationConstPtr fCalibration;
  I3DetectorStatusConstPtr fStatus;

  ////////////////////////////////////////////////////
  /// Variables for Scint
  ////////////////////////////////////////////////////
  I3VectorOMKey fSilentScint; //List of silent OMs
  std::map<OMKey, I3OMGeo> fScintOMGeo;  //List of all OMs in geometry


  ////////////////////////////////////////////////////
  /// Variables for Radio
  ////////////////////////////////////////////////////
  I3AntennaDataMap fAntennaDataMap;
  I3RadGeoMap fRadGeo;


  SET_LOGGER("RockBottom");
};

I3_POINTER_TYPEDEFS(I3RbLikelihoodBase);


#endif
