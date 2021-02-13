/**
 * copyright  (C) 2014
 *
 * The Icecube Collaboration
 *
 * $Id: I3ParameterMap.cxx 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \author Javier Gonzalez
 * \date 18 Feb 2014
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

static const char CVSId[] =
"$Id: I3ParameterMap.cxx 173728 2019-06-04 17:46:14Z dsoldin $";


#include <rock_bottom/I3ParameterMap.h>



template <class Archive>
void I3ParameterMap::serialize(Archive & ar, unsigned version)
{
  ar & make_nvp("I3FrameObject", base_object<I3FrameObject>(*this));
  ar & make_nvp("name", fName);
  ar & make_nvp("parameters", fParameters);
  ar & make_nvp("names", fParameterNames);
}

I3_SERIALIZABLE(I3ParameterMap);

