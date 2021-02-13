/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3RbNKG.h 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3RbNKG.h
 *
 * \author Javier Gonzalez
 * \date 19 Nov 2012
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

#ifndef __I3RbNKG_h_
#define __I3RbNKG_h_

static const char CVSId__I3RbNKG[] =
"$Id: I3RbNKG.h 173728 2019-06-04 17:46:14Z dsoldin $";


#include <rock_bottom/interface/I3RbLDFService.h>

class I3RbNKG: public I3RbLDFService {
public:
  I3RbNKG(double r_ref=125.);
  virtual ~I3RbNKG(){}

  virtual double GetSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const;
  virtual double GetLogSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const;

}; // class I3RbNKG

I3_POINTER_TYPEDEFS(I3RbNKG);

#endif // __I3RbNKG_h_

