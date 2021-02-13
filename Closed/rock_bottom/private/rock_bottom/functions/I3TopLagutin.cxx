/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3TopLagutin.cxx 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3RbLagutin.cxx
 *
 * \author Javier Gonzalez
 * \date 19 Nov 2012
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

static const char CVSId[] =
"$Id: I3TopLagutin.cxx 173728 2019-06-04 17:46:14Z dsoldin $";

#include <rock_bottom/I3RbUtilities.h>
#include <rock_bottom/functions/I3RbLagutin.h>
#include <gsl/gsl_sf_gamma.h>
#include <gsl/gsl_sf_hyperg.h>
#include <cmath>

using namespace std;


I3RbLagutin::I3RbLagutin(double r_ref):
  I3RbLDFService("Lagutin", rock_bottom::GetNParameters()) {
  
  rock_bottom::FillParameterNames(fParameterNames);
}


double I3RbLagutin::GetSignal(
  double rho, 
  double zenith, 
  bool zenith_dependence, 
  I3ParameterMapPtr fparams) const {
  
  const double local_x = rho/fparams->GetParameterByName("r_ref");
  double N = fparams->GetParameterByName("Log10_S125");
  double alpha = fparams->GetParameterByName("Beta");
  double d = 0.01000;
  double beta = 3.2000;
  double delta = 0.6;
  double F = gsl_sf_hyperg_2F1(delta, -(alpha)+2., delta-(alpha)+beta, 1.0-d);
  double B = (tgamma(2.-(alpha)) * tgamma(delta+beta-2.) )/ tgamma(2.-(alpha)+delta+beta-2.);
  double C = 1./(2.*M_PI*(fparams->GetParameterByName("r_ref"))*(fparams->GetParameterByName("r_ref"))*F*B);
 
  const double sig = C*pow(10., N)*pow(local_x, -alpha)*pow(1.+local_x,alpha-beta)*pow(1.+d*local_x, -1.*delta);
  fparams->SetParameterByName("LDFtype",2);
  return sig;
}

double I3RbLagutin::GetLogSignal(
  double rho, 
  double zenith, 
  bool zenith_dependence, 
  I3ParameterMapPtr fparams) const {
  
  const double local_x = rho/fparams->GetParameterByName("r_ref");
  std::cout << "Ref_radius: " << fparams->GetParameterByName("r_ref") <<std::endl;
  double d = 0.01000;
  double beta = 3.2000;
  double delta = 0.6;
  double F = gsl_sf_hyperg_2F1(delta, -(fparams->GetParameterByName("Beta"))+2., delta-(fparams->GetParameterByName("Beta"))+beta, 1.0-d);
  double B = (tgamma(2.-(fparams->GetParameterByName("Beta"))) * tgamma(delta+beta-2.) )/ tgamma(2.-(fparams->GetParameterByName("Beta"))+delta+beta-2.);
  double C = 1./(2.*M_PI*(fparams->GetParameterByName("r_ref"))*(fparams->GetParameterByName("r_ref"))*F*B);
  const double s = log10(C)+fparams->GetParameterByName("Log10_S125")-(fparams->GetParameterByName("Beta"))*log10(local_x)+((fparams->GetParameterByName("Beta"))-beta)*log10(1.+local_x)-delta*log10(1.+d*local_x);
  fparams->SetParameterByName("LDFtype",2);
  
  return s;
}


