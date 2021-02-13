/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3RbUtilities.cxx 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3RbUtilities.cxx
 *
 * \author Javier Gonzalez
 * \date 30 Jan 2013
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

static const char CVSId[] =
  "$Id: I3RbUtilities.cxx 173728 2019-06-04 17:46:14Z dsoldin $";


#include <rock_bottom/I3RbUtilities.h>
#include <cmath>
#include <iostream>

using std::endl;
using std::cout;
using std::cos;
using std::sin;
using namespace boost::numeric::ublas;

namespace rock_bottom {

I3Position test(I3Particle& particle, const I3Position& pos)
{ return I3Position(); }

matrix<double>
ShowerToDetectorRotation(const I3Direction& direction) {
  cout << "ShowerToDetectorRotation " << direction.GetZenith() / I3Units::deg << ", " << direction.GetAzimuth() / I3Units::deg << endl;
  // clockwise zenith rotation
  matrix<double> d_theta = matrix<double>(3, 3);
  d_theta *= 0.;
  d_theta(0, 0) =  cos(direction.GetZenith());
  d_theta(1, 1) =  1.;
  d_theta(2, 2) =  cos(direction.GetZenith());
  d_theta(0, 2) = -sin(direction.GetZenith());
  d_theta(2, 0) =  sin(direction.GetZenith());

  // counter-clockwise azimuth rotation
  matrix<double> d_phi = matrix<double>(3, 3);
  d_phi *= 0.;
  d_phi(0, 0) =  cos(direction.GetAzimuth());
  d_phi(1, 1) =  cos(direction.GetAzimuth());
  d_phi(2, 2) =  1.;
  d_phi(0, 1) =  sin(direction.GetAzimuth());
  d_phi(1, 0) = -sin(direction.GetAzimuth());
  return prod(d_phi, d_theta);
}

matrix<double>
DetectorToShowerRotation(const I3Direction& direction) {
  cout << "double " << direction.GetZenith() / I3Units::deg << ", " << direction.GetAzimuth() / I3Units::deg << endl;
  // counter-clockwise zenith rotation
  matrix<double> d_theta = matrix<double>(3, 3);
  d_theta *= 0.;
  d_theta(0, 0) =  cos(direction.GetZenith());
  d_theta(1, 1) =  1.;
  d_theta(2, 2) =  cos(direction.GetZenith());
  d_theta(0, 2) = -sin(direction.GetZenith());
  d_theta(2, 0) =  sin(direction.GetZenith());

  // clockwise azimuth rotation
  matrix<double> d_phi = matrix<double>(3, 3);
  d_phi *= 0.;
  d_phi(0, 0) =  cos(direction.GetAzimuth());
  d_phi(1, 1) =  cos(direction.GetAzimuth());
  d_phi(2, 2) =  1.;
  d_phi(0, 1) =  sin(direction.GetAzimuth());
  d_phi(1, 0) = -sin(direction.GetAzimuth());
  return prod(d_theta, d_phi);
}


I3Position FromShowerToDetector(const I3Particle& particle, const I3Position& pos) {
//   const matrix<double> m = ShowerToDetectorRotation(particle.GetDir());
//   vector<double> r(3);
//   r(0) = pos.GetX();
//   r(1) = pos.GetY();
//   r(2) = pos.GetZ();
//   r = prod(m, r);
//   return I3Position(r(0)+particle.GetPos().GetX(),
//                     r(1)+particle.GetPos().GetY(),
//                     r(2)+particle.GetPos().GetZ());
  I3Position p = pos;
  p.RotateY(particle.GetDir().GetZenith());
  p.RotateZ(particle.GetDir().GetAzimuth());
  return p + particle.GetPos();
}


I3Position FromDetectorToShower(const I3Particle& particle, const I3Position& pos) {
//   const matrix<double> m = ShowerToDetectorRotation(particle.GetDir());
//   vector<double> r(3);
//   r(0) = pos.GetX()-particle.GetPos().GetX();
//   r(1) = pos.GetY()-particle.GetPos().GetY();
//   r(2) = pos.GetZ()-particle.GetPos().GetZ();
//   r = prod(m, r);
//   return I3Position(r(0),r(1),r(2));
  I3Position p = pos - particle.GetPos();
  //p.RotateZ(-particle.GetDir().GetAzimuth());
  //p.RotateY(-particle.GetDir().GetZenith());
  return p;
}


//double I3CurveLikelihood::GetDistToAxis(const I3EventHypothesis &hypo, const I3Position &pos)
double GetDistToAxis(const I3Particle& particle, const I3Position &pos) {
  double x_c = particle.GetPos().GetX();
  double y_c = particle.GetPos().GetY();
  double z_c = particle.GetPos().GetZ();
  double nx = particle.GetDir().GetX();
  double ny = particle.GetDir().GetY();

  //log_info("hypo %f %f %f hit %f %f %f", x_c, y_c, z_c, pos.GetX(),pos.GetY(),pos.GetZ());
  //log_info("nx %f ny %f",nx, ny);
  double abs_x_sq = (pos.GetX() - x_c) * (pos.GetX() - x_c)
                    + (pos.GetY() - y_c) * (pos.GetY() - y_c)
                    + (pos.GetZ() - z_c) * (pos.GetZ() - z_c);

  double n_prod_x = nx * (pos.GetX() - x_c)
                    + ny * (pos.GetY() - y_c)
                    - sqrt(1. - nx * nx - ny * ny) * (pos.GetZ() - z_c);

  //log_info("part local_R %f %f",abs_x_sq, n_prod_x);
  //log_info("local_R %f",sqrt(abs_x_sq - n_prod_x * n_prod_x));
  return sqrt(abs_x_sq - n_prod_x * n_prod_x);
}

double GetDistToPlane(const I3Particle& particle, const I3Position &pos, const double time) {
  double x_0 = particle.GetPos().GetX();
  double y_0 = particle.GetPos().GetY();
  double z_c = particle.GetPos().GetZ();
  double nx = particle.GetDir().GetX();
  double ny = particle.GetDir().GetY();
  double t_0 = particle.GetTime();
  double t_plane = t_0 + (nx * (pos.GetX() - x_0) + ny * (pos.GetY() - y_0) - sqrt(1. - nx * nx - ny * ny) * (pos.GetZ() - z_c)) / I3Constants::c;
  return t_plane - time;

}


I3Direction FromShowerToDetector(const I3Particle& particle, const I3Direction& pos) {
//   const matrix<double> m = DetectorToShowerRotation(particle.GetDir());
//   vector<double> r(3);
//   r(0) = pos.GetX();
//   r(1) = pos.GetY();
//   r(2) = pos.GetZ();
//   r = prod(m, r);
//   return I3Direction(r(0),r(1),r(2));
  I3Direction p = pos;
  p.RotateY(particle.GetDir().GetZenith());
  p.RotateZ(particle.GetDir().GetAzimuth());
  return p;
}


I3Direction FromDetectorToShower(const I3Particle& particle, const I3Direction& pos) {
//   const matrix<double> m = DetectorToShowerRotation(particle.GetDir());
//   vector<double> r(3);
//   r(0) = pos.GetX();
//   r(1) = pos.GetY();
//   r(2) = pos.GetZ();
//   r = prod(m, r);
//   return I3Direction(r(0),r(1),r(2));
  I3Direction p = pos;
  p.RotateZ(-particle.GetDir().GetAzimuth());
  p.RotateY(-particle.GetDir().GetZenith());
  return p;
}

unsigned int GetNParameters() {
  return 22;
}

void FillParameterNames(I3Vector<std::string> &parameterNames) {
  parameterNames[0] = "Log10_S125";
  parameterNames[1] = "Beta";
  parameterNames[2] = "RhoMu";
  parameterNames[3] = "Chi2_ldf";
  parameterNames[4] = "ndof_ldf";
  parameterNames[5] = "r_ref";
  parameterNames[6] = "Moliere";
  parameterNames[7] = "r_mu_ref";
  parameterNames[8] = "llh_ldf";
  parameterNames[9] = "LDFtype";
  parameterNames[10] = "gamma";
  parameterNames[11] = "omega";
  parameterNames[12] = "Amp";
  parameterNames[13] = "Chi2_time";
  parameterNames[14] = "ndof_time";
  parameterNames[15] = "llh_time";
  parameterNames[16] = "NX";
  parameterNames[17] = "NY";
  parameterNames[18] = "Kappa";
  parameterNames[19] = "Dcurve";
  parameterNames[20] = "Ncurve";
  parameterNames[21] = "ndof";
}

bool CheckIfExsitsInFrame(const I3Frame &frame, std::string name, bool doFatal, std::string objType) {
  if (!frame.Has(name)) {
    std::string ofType = "" != objType ? " of type (" + objType + ")" : "";
    std::string message = "The requested parameter" + ofType
                          + " with name (" + name + ") does not exists in the frame!";

    if (doFatal)
      log_fatal(message.c_str());
    else
      log_warn(message.c_str());

    return false;
  }

  return true;
}

}

