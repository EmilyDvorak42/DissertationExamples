/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3TopMuonLDF.cxx 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3RbMuonLDF.cxx
 *
 * \author Dennis Soldin
 * \date 19 Nov 2012
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

static const char CVSId[] =
"$Id: I3TopMuonLDF.cxx 173728 2019-06-04 17:46:14Z dsoldin $";

#include <rock_bottom/I3RbUtilities.h>
#include <rock_bottom/functions/I3RbMuonLDF.h>

#include <cmath>

using namespace std;


I3RbMuonLDF::I3RbMuonLDF(double r_ref):
  I3RbLDFService("MuonLDF", rock_bottom::GetNParameters()) {
  
  rock_bottom::FillParameterNames(fParameterNames);
}


double I3RbMuonLDF::GetSignal(
  double rho, double zenith, 
  bool zenith_dependence, 
  I3ParameterMapPtr fparams) const {

  const double mu_moliere = 320*I3Units::m;
  double beta = 0.75;
  double gamma = 2.5;
  if (zenith_dependence) {
  	beta = GetBeta(zenith);
    gamma = GetGamma(zenith);
  }
  fparams->SetParameterByName("gamma",gamma);
  fparams->SetParameterByName("omega",beta);
  return fparams->GetParameterByName("RhoMu") *
    pow(rho/fparams->GetParameterByName("r_mu_ref"), -beta) *
    pow((rho+mu_moliere)/(fparams->GetParameterByName("r_mu_ref")+mu_moliere), -gamma);
}


double I3RbMuonLDF::GetLogSignal(
  double rho,
  double zenith, 
  bool zenith_dependence, 
  I3ParameterMapPtr fparams) const {

  const double mu_moliere = 320*I3Units::m;
  double beta = 0.75;
  double gamma = 2.5;
  if (zenith_dependence) {
    beta = GetBeta(zenith);
    gamma = GetGamma(zenith);
  }
  fparams->SetParameterByName("gamma",gamma);
  fparams->SetParameterByName("omega",beta);
  return log(fparams->GetParameterByName("RhoMu")) +
    (-beta)*log(rho/fparams->GetParameterByName("r_mu_ref")) +
    (-gamma)*log((rho+mu_moliere)/(fparams->GetParameterByName("r_mu_ref")+mu_moliere));
}


double I3RbMuonLDF::GetBeta(double zenith) const {

  // get zenith dependent beta of the Greisen formula
  // obtained from CORSIKA simulations (Sibyll 2.1)
  const double a_beta = 0.0588828018308;
  const double b_beta = 0.690841945182;
  return a_beta + b_beta*cos(zenith);
}


double
I3RbMuonLDF::GetGamma(double zenith)
  const
{
  // get zenith dependent gamma of the Greisen formula
  // obtained from CORSIKA simulations (Sibyll 2.1)
  const double a_gamma = 2.34120348911;
  const double b_gamma = 0.713622251311;
  return a_gamma + b_gamma*cos(zenith);
}


