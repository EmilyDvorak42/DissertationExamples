/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3RbLogLog.h 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3RbLogLog.h
 *
 * \author Javier Gonzalez
 * \date 19 Nov 2012
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

#ifndef __I3RbLogLog_h_
#define __I3RbLogLog_h_

static const char CVSId__I3RbLogLog[] =
"$Id: I3RbLogLog.h 173728 2019-06-04 17:46:14Z dsoldin $";


#include <rock_bottom/interface/I3RbLDFService.h>

class I3RbLogLog: public I3RbLDFService {
public:
  //I3RbLogLog(double r_ref=125.);
  I3RbLogLog(double r_ref);
  virtual ~I3RbLogLog(){}

  virtual double GetSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const;
  virtual double GetLogSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const;

}; // class I3RbLogLog


I3_POINTER_TYPEDEFS(I3RbLogLog);

#endif // __I3RbLogLog_h_

