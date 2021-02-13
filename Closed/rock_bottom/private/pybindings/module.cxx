/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: module.cxx 173671 2019-06-03 17:59:13Z acoleman $
 *
 * \author Javier Gonzalez
 * \date 22 Nov 2012
 * \version $Revision: 173671 $
 * Last changed by $LastChangedBy: acoleman $ on $LastChangedDate: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 */

#include <icetray/load_project.h>

void registerI3RbLDFService();
void registerI3LaputopSignalModel();
void registerI3RbUtilities();
void register_I3ParameterMap();
void registerI3TwoLDFSignalModel();
void registerI3ScintSignalModel();

using namespace boost::python;

BOOST_PYTHON_MODULE(rock_bottom)
{
  load_project("librock_bottom", false);

  registerI3RbLDFService();
  registerI3LaputopSignalModel();
  registerI3RbUtilities();
  register_I3ParameterMap();
  registerI3TwoLDFSignalModel();
  registerI3ScintSignalModel();

}
