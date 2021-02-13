/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3RbUtilities.h 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3RbUtilities.h
 *
 * \author Javier Gonzalez
 * \date 30 Jan 2013
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

#ifndef _rock_bottom_I3RbUtilities_h_
#define _rock_bottom_I3RbUtilities_h_

static const char CVSId_rock_bottom_I3RbUtilities[] =
  "$Id: I3RbUtilities.h 173728 2019-06-04 17:46:14Z dsoldin $";

#include <icetray/I3Frame.h>
#include <dataclasses/I3Position.h>
#include <dataclasses/physics/I3Particle.h>
#include <boost/numeric/ublas/matrix.hpp>

/*
  These are some utilities that should not exist but I haven't found
  any general-purpose tools (Root does not count!) to do this.
 */


namespace rock_bottom {
boost::numeric::ublas::matrix<double> ShowerToDetectorRotation(const I3Direction& direction);
boost::numeric::ublas::matrix<double> DetectorToShowerRotation(const I3Direction& direction);

I3Position FromShowerToDetector(const I3Particle& particle, const I3Position& pos);
I3Position FromDetectorToShower(const I3Particle& particle, const I3Position& pos);
double GetDistToAxis(const I3Particle& particle, const I3Position& pos);
double GetDistToPlane(const I3Particle& particle, const I3Position& pos, double time);
I3Direction FromShowerToDetector(const I3Particle& particle, const I3Direction& pos);
I3Direction FromDetectorToShower(const I3Particle& particle, const I3Direction& pos);

enum DetectorTypes {
  IceTop = 0,
  Scint = 1,
  Radio = 2,
  NDetectorTypes = 3
};

unsigned int GetNParameters();
void FillParameterNames(I3Vector<std::string> &parameterNames);

bool CheckIfExsitsInFrame(const I3Frame &frame, std::string name, bool doFatal = false, std::string objType = "");

} // end namespace rock_bottom


#endif // _rock_bottom_I3RbUtilities_h_

