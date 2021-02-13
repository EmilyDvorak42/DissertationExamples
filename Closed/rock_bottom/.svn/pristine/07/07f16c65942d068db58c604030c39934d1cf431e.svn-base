/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3RbUtilities.cxx 173671 2019-06-03 17:59:13Z acoleman $
 *
 * \author Javier Gonzalez
 * \date 22 Nov 2012
 * \version $Revision: 173671 $
 * Last changed by $LastChangedBy: acoleman $ on $LastChangedDate: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 */

#include <rock_bottom/I3RbUtilities.h>

using namespace boost::python;
namespace bp = boost::python;
using namespace rock_bottom;


void registerI3RbUtilities() {
  // All these are here to be able to overload the methods.
  I3Direction (*FromShowerToDetector_dir)(const I3Particle&, const I3Direction&) = FromShowerToDetector;
  I3Position  (*FromShowerToDetector_pos)(const I3Particle&,  const I3Position&) = FromShowerToDetector;

  I3Direction (*FromDetectorToShower_dir)(const I3Particle&, const I3Direction&) = FromDetectorToShower;
  I3Position  (*FromDetectorToShower_pos)(const I3Particle&,  const I3Position&) = FromDetectorToShower;

  def("from_shower_to_detector", FromShowerToDetector_pos,
      "Calculate a position in detector coordinates from a position in shower plane coordinates.",
      (bp::arg("shower_axis"), bp::arg("position")));
  def("from_shower_to_detector", FromShowerToDetector_dir,
      "Calculate a direction in detector coordinates from a direction in shower plane coordinates.",
      (bp::arg("shower_axis"), bp::arg("direction")));
  def("from_detector_to_shower", FromDetectorToShower_pos,
      "Calculate a position in shower plane coordinates from a position in detector coordinates.",
      (bp::arg("shower_axis"), bp::arg("position")));
  def("from_detector_to_shower", FromDetectorToShower_dir,
      "Calculate a position in shower plane coordinates from a direction in detector coordinates.",
      (bp::arg("shower_axis"), bp::arg("direction")));


  enum_<rock_bottom::DetectorTypes>("DetectorTypes")
  .value("IceTop", rock_bottom::IceTop)
  .value("Scint", rock_bottom::Scint)
  .value("Radio", rock_bottom::Radio)
  .value("NDetectorTypes", rock_bottom::NDetectorTypes)
  .export_values()
  ;
}
