/**
 * copyright  (C) 2012
 *
 * The Icecube Collaboration
 *
 * $Id: I3RbLDFService.h 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3RbLDFService.h
 *
 * \author Javier Gonzalez
 * \date 19 Nov 2012
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

#ifndef __I3RbLDFService_h_
#define __I3RbLDFService_h_

static const char CVSId__I3RbLDFService[] =
"$Id: I3RbLDFService.h 173728 2019-06-04 17:46:14Z dsoldin $";


#include <dataclasses/physics/I3Particle.h>
#include <dataclasses/I3Position.h>
#include <dataclasses/I3Vector.h>
#include <gulliver/I3EventHypothesis.h>
#include <string>

#include <rock_bottom/I3ParameterMap.h>
#include <dataclasses/I3MapOMKeyMask.h>

class I3Context;

class I3RbLDFService {
public:
  I3RbLDFService(const std::string &name, int n):
    fParameters(n),
    fParameterNames(n)
  {}
  virtual ~I3RbLDFService(){}

  virtual double GetSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const = 0;
  virtual double GetLogSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const = 0;
                                 
  void SetParameter(int i, double p)
  { fParameters[i] = p; }

  void SetParameters(const I3Particle& core, const I3ParameterMap& params)
  {
    const unsigned int size = params.GetSize();
    if (size!= fParameters.size()) {
      log_warn("Setting parameters of different sizes! (%u != %lu)",
               size, fParameters.size());
      fParameters.resize(size);
      fParameterNames.resize(size);
    }
    fCore = core;
    for (unsigned int i = 0; i != size; ++i) {
      fParameters[i] = params.GetParameter(i);
      fParameterNames[i] = params.GetParameterName(i);
    }
    log_trace(" - axis: (%f, %f, %f), direction: (%f, %f), time: %f",
              fCore.GetX(),
              fCore.GetY(),
              fCore.GetZ(),
              fCore.GetZenith(),
              fCore.GetAzimuth(),
              fCore.GetTime()
              );
    for (unsigned int i = 0; i != fParameters.size(); ++i) {
      log_debug(" - %s: %f", fParameterNames[i].c_str(), fParameters[i]);
    }
  }

  I3Particle GetAxis() const
  {
    return fCore;
  }

  //I3ParameterMap GetParameters() const
  I3ParameterMap GetParameters() const
  {
    return I3ParameterMap(fName,
                          fParameters, fParameterNames);
  }

  double GetParameter(int i) const
  { return fParameters[i]; }
  std::string GetParameterName(int i) const
  { return fParameterNames[i]; }
  I3Vector<std::string> GetParameterNames() const
  { return fParameterNames; }


protected:
  std::string fName;
  I3Particle fCore;
  I3Vector<double> fParameters;
  I3Vector<std::string> fParameterNames;

  SET_LOGGER( "RockBottom" );

}; // class I3RbLDFService

I3_POINTER_TYPEDEFS(I3RbLDFService);

#endif // __I3RbLDFService_h_

