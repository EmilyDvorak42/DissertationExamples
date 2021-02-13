/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3RbLagutin.h 173671 2019-06-03 17:59:13Z acoleman $
 *
 * \file I3RbLagutin.h
 *
 * \author Javier Gonzalez
 * \date 19 Nov 2012
 * \version $Revision: 173671 $
 * Last changed by $LastChangedBy: acoleman $ on $LastChangedDate: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 */

#ifndef __I3RbLagutin_h_
#define __I3RbLagutin_h_

static const char CVSId__I3RbLagutinLDF[] =
"$Id: I3RbLagutin.h 173671 2019-06-03 17:59:13Z acoleman $";


#include <rock_bottom/interface/I3RbLDFService.h>

class I3RbLagutin: public I3RbLDFService {
public:
  I3RbLagutin(double r_ref=100.);
  virtual ~I3RbLagutin(){}

  virtual double GetSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const;
  virtual double GetLogSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const;

private: 
  double GetBeta(double zenith) const;
  double GetGamma(double zenith) const;

}; // class I3RbLagutin


I3_POINTER_TYPEDEFS(I3RbLagutin);

#endif // __I3RbLagutin_h_

// Configure (x)emacs for this file ...
// Local Variables:
// mode:c++
// compile-command: "make -C .. -k"
// End:
