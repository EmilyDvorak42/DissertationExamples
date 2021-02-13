/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3RbLDFService.cxx 173671 2019-06-03 17:59:13Z acoleman $
 *
 * \file I3RbLDFService.cxx
 *
 * \author Javier Gonzalez
 * \date 20 Nov 2012
 * \version $Revision: 173671 $
 * Last changed by $LastChangedBy: acoleman $ on $LastChangedDate: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 */

#include <rock_bottom/interface/I3RbLDFService.h>
#include <rock_bottom/functions/I3RbNKG.h>
#include <rock_bottom/functions/I3RbLogLog.h>
#include <rock_bottom/functions/I3RbMuonLDF.h>
#include <rock_bottom/functions/I3RbLagutin.h>

#include <boost/python.hpp>

using namespace boost::python;

class LdfNS{};

struct I3RbLDFServiceWrapper: public I3RbLDFService, public boost::python::wrapper<I3RbLDFService>
{
  I3RbLDFServiceWrapper(const std::string &name, int n, int m=0):
    I3RbLDFService(name,n)
  {}

  virtual double GetSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const
  {
    return this->get_override("GetSignal")(rho, zenith, zenith_dependence, fparams);
  }

  virtual double GetLogSignal(double rho, double zenith, bool zenith_dependence, I3ParameterMapPtr fparams) const
  {
    return this->get_override("GetLogSignal")(rho, zenith, zenith_dependence, fparams);
  }
    
  virtual void Configure() {
    this->get_override("Configure")();
  }
};

template<class C> boost::shared_ptr<C> Init(double t)
{ return boost::shared_ptr<C>(new C(t)); }

void registerI3RbLDFService()
{
  // still missing an overloaded method to set parameters from a list
  boost::python::class_<I3RbLDFService, boost::shared_ptr<I3RbLDFService>,
                        boost::noncopyable>("I3RbLDFServiceBase", boost::python::no_init)
    .def("SetParameters", &I3RbLDFService::SetParameters)
    .def("SetParameter", &I3RbLDFService::SetParameter)
    .def("GetParameters", &I3RbLDFService::GetParameters)
    .def("GetParameter", &I3RbLDFService::GetParameter)
    .def("GetParameterName", &I3RbLDFService::GetParameterName)
    .def("GetParameterNames", &I3RbLDFService::GetParameterNames)
    ;

  boost::python::class_<I3RbLDFServiceWrapper, boost::shared_ptr<I3RbLDFServiceWrapper>,
                        boost::noncopyable>("I3RbLDFService", boost::python::init<const std::string &, int, int>())
    .def("SetParameters", &I3RbLDFService::SetParameters)
    .def("SetParameter", &I3RbLDFService::SetParameter)
    .def("GetParameters", &I3RbLDFService::GetParameters)
    .def("GetParameter", &I3RbLDFService::GetParameter)
    .def("GetParameterName", &I3RbLDFService::GetParameterName)
    .def("GetParameterNames", &I3RbLDFService::GetParameterNames)
    .def("GetSignal", &I3RbLDFService::GetSignal)
    .def("GetLogSignal", &I3RbLDFService::GetLogSignal)
    ;

  boost::python::scope a = boost::python::class_<LdfNS>("ldf");
  boost::python::class_<I3RbNKG, boost::shared_ptr<I3RbNKG>, boost::python::bases<I3RbLDFService>, boost::noncopyable>
    ("NKG", "Nishimura-Kamata-Greisen lateral distribution", boost::python::no_init)
    .def("__init__", boost::python::make_constructor(&Init<I3RbNKG>, boost::python::default_call_policies(),
                                                 (boost::python::arg("r_ref")=125.)));
  boost::python::class_<I3RbLogLog, boost::shared_ptr<I3RbLogLog>, boost::python::bases<I3RbLDFService>, boost::noncopyable>
    ("LogLog", "log-log parabola lateral distribution", boost::python::no_init)
    .def("__init__", boost::python::make_constructor(&Init<I3RbLogLog>, boost::python::default_call_policies(),
                                                 (boost::python::arg("r_ref"))));
  //                                               (boost::python::arg("r_ref")=125.)));
                                                 
  boost::python::class_<I3RbMuonLDF, boost::shared_ptr<I3RbMuonLDF>, boost::python::bases<I3RbLDFService>, boost::noncopyable>
    ("MuonLDF", "Muon LDF function", boost::python::no_init)
    .def("__init__", boost::python::make_constructor(&Init<I3RbMuonLDF>, boost::python::default_call_policies(),
                                                     (boost::python::arg("r_ref")=125.)));

  boost::python::class_<I3RbLagutin, boost::shared_ptr<I3RbLagutin>, boost::python::bases<I3RbLDFService>, boost::noncopyable>
    ("Lagutin", "Lagutin LDF function", boost::python::no_init)
    .def("__init__", boost::python::make_constructor(&Init<I3RbLagutin>, boost::python::default_call_policies(),
                                                     (boost::python::arg("r_ref")=100.)));                                                     
                                                     
}
