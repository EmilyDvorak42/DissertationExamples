/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3TopLogLog.cxx 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3RbLogLog.cxx
 *
 * \author Javier Gonzalez
 * \date 19 Nov 2012
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

static const char CVSId[] =
"$Id: I3TopLogLog.cxx 173728 2019-06-04 17:46:14Z dsoldin $";

#include <rock_bottom/I3RbUtilities.h>
#include <rock_bottom/functions/I3RbLogLog.h>

#include <cmath>

using namespace std;

I3RbLogLog::I3RbLogLog(double r_ref):
  I3RbLDFService("LogLog", rock_bottom::GetNParameters()) {
  
  rock_bottom::FillParameterNames(fParameterNames);
}


double I3RbLogLog::GetSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const {

  return pow(10., GetLogSignal(rho, zenith, zenith_dependence, fparams));
}


double I3RbLogLog::GetLogSignal(
  double rho, 
  double zenith, 
  bool zenith_dependence, 
  I3ParameterMapPtr fparams) const {
  
  //log_info("rho %f",rho);
  const double local_x = log10(rho/fparams->GetParameterByName("r_ref"));
  const double s = fparams->GetParameterByName("Log10_S125") - fparams->GetParameterByName("Beta")*local_x - fparams->GetParameterByName("Kappa")*local_x*local_x;
  fparams->SetParameterByName("LDFtype",0);
  //log_info("rref %f lgSref %f local_x %f beta %f kappa %f",fparams->GetParameterByName("r_ref"),fparams->GetParameterByName("Log10_S125"),local_x,fparams->GetParameterByName("Beta"),fparams->GetParameterByName("Kappa"));//log_info("s %f",s);
  return s;
}
