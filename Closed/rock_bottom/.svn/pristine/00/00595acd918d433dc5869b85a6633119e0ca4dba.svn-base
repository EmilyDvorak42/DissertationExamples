/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3RbMuonLDF.h 173671 2019-06-03 17:59:13Z acoleman $
 *
 * \file I3RbMuonLDF.h
 *
 * \author Javier Gonzalez
 * \date 19 Nov 2012
 * \version $Revision: 173671 $
 * Last changed by $LastChangedBy: acoleman $ on $LastChangedDate: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 */

#ifndef __I3RbMuonLDF_h_
#define __I3RbMuonLDF_h_

static const char CVSId__I3RbMuonLDF[] =
"$Id: I3RbMuonLDF.h 173671 2019-06-03 17:59:13Z acoleman $";


#include <rock_bottom/interface/I3RbLDFService.h>

class I3RbMuonLDF: public I3RbLDFService {
public:
  I3RbMuonLDF(double r_ref=125.);
  virtual ~I3RbMuonLDF(){}

  virtual double GetSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const;
  virtual double GetLogSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const;
  
private: 
  double GetBeta(double zenith) const;
  double GetGamma(double zenith) const;

}; // class I3RbMuonLDF


I3_POINTER_TYPEDEFS(I3RbMuonLDF);

#endif // __I3RbMuonLDF_h_

// Configure (x)emacs for this file ...
// Local Variables:
// mode:c++
// compile-command: "make -C .. -k"
// End:
