/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3TopNKG.cxx 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3RbNKG.cxx
 *
 * \author Javier Gonzalez
 * \date 19 Nov 2012
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

static const char CVSId[] =
"$Id: I3TopNKG.cxx 173728 2019-06-04 17:46:14Z dsoldin $";

#include <rock_bottom/I3RbUtilities.h>
#include <rock_bottom/functions/I3RbNKG.h>

#include <cmath>

using namespace std;


I3RbNKG::I3RbNKG(double r_ref):
  I3RbLDFService("NKG", rock_bottom::GetNParameters()) {
  
  rock_bottom::FillParameterNames(fParameterNames);
}


double I3RbNKG::GetSignal(
  double rho, 
  double zenith, 
  bool zenith_dependence, 
  I3ParameterMapPtr fparams) const {
  
  return pow(10., GetLogSignal(rho, zenith, zenith_dependence, fparams));
}


double I3RbNKG::GetLogSignal(
  double rho, 
  double zenith, 
  bool zenith_dependence, 
  I3ParameterMapPtr fparams) const {

  const double local_x = log10(rho/fparams->GetParameterByName("r_ref"));
  const double s = fparams->GetParameterByName("Log10_S125") + (fparams->GetParameterByName("Beta")-2.)*local_x + 
    (fparams->GetParameterByName("Beta")-4.5)*log10((rho+128.)/(fparams->GetParameterByName("r_ref")+128.));
    
  fparams->SetParameterByName("LDFtype",1);
  
  return s;
}
