#include <rock_bottom/interface/I3RbLikelihoodBase.h>

I3RbLikelihoodBase::I3RbLikelihoodBase(const I3Context &c):
  I3ServiceBase(c) {

  fCurrentType = rock_bottom::DetectorTypes::NDetectorTypes;
  fSignalModel = NULL;
  fPulsesName1 = "";
  fPulsesName2 = "";
  fUseSaturated = false;
  fUseSilent = false;
  fMinSignal = 0.;
  fBadDetectorsName = "";

  ConstructIceTop();
  ConstructScint();
  ConstructRadio();
  //Add new detectors here//

  AddParameter("DetectorType", "Which detector type this LDF should be associated with", fCurrentType);
  AddParameter("Model", "Signal model to use", "");
  AddParameter("Pulses1", "HLC reco pulse map vector", fPulsesName1);
  AddParameter("Pulses2", "SLC reco pulse map vector", fPulsesName2);
  AddParameter("IgnoreDetectors", "List of Tank Keys. These tanks completely ignored, as if they did not exist.", fBadDetectorsName);
  AddParameter("UseSaturated", "Flag to tell it to use saturated pulses", fUseSaturated);
  AddParameter("UseSilent", "Flag to tell it to use silent tanks", fUseSilent);
  AddParameter("MinSignal", "Minimum signal (in VEM) required to calculate the tank's signal probability (for smaller signals, the CDF is used instead)", fMinSignal);

}

void I3RbLikelihoodBase::Configure() {
  log_info("Configuring the Rock Bottom LDF, boss!");

  log_trace("Configuring likelihood (%s)", GetName().c_str());
  GetParameter( "DetectorType",  fCurrentType);

  std::string modelName;
  GetParameter( "Model",  modelName);
  if (!context_.Has<I3RbSignalModelPtr>(modelName)) {
    log_fatal("I3RbLikelihoodBase requires a signal model (%s) and it is not found!", modelName.c_str());
  }
  fSignalModel = context_.Get<I3RbSignalModelPtr>(modelName);

  //Run the configure function for each of the detector types
  switch (fCurrentType) {
  case rock_bottom::DetectorTypes::IceTop :
    log_info("Configuring IceTop");
    ConfigureIceTop();
    break;
  case rock_bottom::DetectorTypes::Scint :
    log_info("Configuring Scint");
    ConfigureScint();
    break;
  case rock_bottom::DetectorTypes::Radio :
    log_info("Configuring Radio");
    ConfigureRadio();
    break;
  default:
    log_fatal("I3RbLikelihoodBase::Configure has not been programmed for this detector type. Get to it, boss!");
  }
  GetParameter( "Pulses1",  fPulsesName1);
  GetParameter( "Pulses2",  fPulsesName2);
  GetParameter( "UseSaturated",  fUseSaturated);
  GetParameter( "UseSilent",  fUseSilent);
  GetParameter( "MinSignal", fMinSignal);
  GetParameter( "IgnoreDetectors",  fBadDetectorsName);

  if ("" == fPulsesName1) {
    log_fatal("You MUST define a name for \"Pulses1\"!");
  } else {
    log_info("It exists!");
    }
}

void I3RbLikelihoodBase::SetGeometry( const I3Geometry &geometry ) {
  log_trace("Setting geometry in likelihood (%s)", GetName().c_str());

  switch (fCurrentType) {
  case rock_bottom::DetectorTypes::IceTop :
    log_debug("Setting geometry for IceTop");
    SetIceTopGeometry(geometry);
    break;
  case rock_bottom::DetectorTypes::Scint :
    log_debug("Setting geometry for Scint");
    SetScintGeometry(geometry);
    break;
  case rock_bottom::DetectorTypes::Radio :
    log_debug("Setting geometry for Radio");
    SetRadioGeometry(geometry);
    break;
  default:
    log_fatal("I3RbLikelihoodBase::SetGeometry has not been programmed for this detector type. Get to it, boss!");
  }

}

void I3RbLikelihoodBase::SetEvent( const I3Frame &frame ) {

  //Safety check to make sure that Pulses1 exists in the frame and that
  //Pulses2 exists if the name was defined

  rock_bottom::CheckIfExsitsInFrame(frame, fPulsesName1, true, "I3RecoPulseSeriesMap");

  if ("" != fPulsesName2) { //If you defined Pulses2
    rock_bottom::CheckIfExsitsInFrame(frame, fPulsesName2, false, "I3RecoPulseSeriesMap");
  }

  if ("" != fBadDetectorsName) {
    rock_bottom::CheckIfExsitsInFrame(frame, fBadDetectorsName, false);
  }

  switch (fCurrentType) {
  case rock_bottom::DetectorTypes::IceTop :
    log_debug("Setting event for IceTop");
    SetIceTopEvent(frame);
    break;
  case rock_bottom::DetectorTypes::Scint :
    log_debug("Setting event for Scint");
    SetScintEvent(frame);
    break;
  case rock_bottom::DetectorTypes::Radio :
    log_debug("Setting event for Radio");
    SetRadioEvent(frame);
    break;
  default:
    log_fatal("I3RbLikelihoodBase::SetEvent has not been programmed for this detector type. Get to it, boss!");
  }

}

double I3RbLikelihoodBase::GetLogLikelihood( const I3EventHypothesis &ehypo ) {

  switch (fCurrentType) {
  case rock_bottom::DetectorTypes::IceTop :
    log_debug("Calculating Icetop LogLikelihood");
    return GetIceTopLogLikelihood(ehypo);
    break;
  case rock_bottom::DetectorTypes::Scint :
    log_debug("Calculating Scint LogLikelihood");
    return GetScintLogLikelihood(ehypo);
    break;
  case rock_bottom::DetectorTypes::Radio :
    log_debug("Calculating Radio LogLikelihood");
    return GetRadioLogLikelihood(ehypo);
    break;
  default:
    log_fatal("I3RbLikelihoodBase::GetLogLikelihood has not been programmed for this detector type. Get to it, boss!");
    return 0;
  }

  return 0.;
}

unsigned int I3RbLikelihoodBase::GetMultiplicity() {

  switch (fCurrentType) {
  case rock_bottom::DetectorTypes::IceTop :
    log_debug("Calculating Icetop Multiplicity");
    return GetIceTopMultiplicity();
    break;
  case rock_bottom::DetectorTypes::Scint :
    log_debug("Calculating Scint Multiplicity");
    return GetScintMultiplicity();
    break;
  case rock_bottom::DetectorTypes::Radio :
    log_debug("Calculating Radio Multiplicity");
    return GetRadioMultiplicity();
    break;
  default:
    log_fatal("I3RbLikelihoodBase::GetMultiplicity has not been programmed for this detector type. Get to it, boss!");
    return 0;
  }

  return 1.;
}
