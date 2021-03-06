/**
 * copyright  (C) 2011
 *
 * The Icecube Collaboration
 *
 * $Id: I3LaputopSignalModel.cxx 173671 2019-06-03 17:59:13Z acoleman $
 *
 * \author Javier Gonzalez
 * \date 22 Nov 2012
 * \version $Revision: 173671 $
 * Last changed by $LastChangedBy: acoleman $ on $LastChangedDate: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 */

#include <rock_bottom/models/icetop/I3LaputopSignalModel.h>
#include <tableio/converter/pybindings.h>
#include <icetray/python/context_suite.hpp>

using namespace boost::python;


void registerI3LaputopSignalModel()
{
  class_<I3LaputopSignalModel, bases<I3FrameObject>, boost::noncopyable>
    ("I3LaputopSignalModel", boost::python::init<const I3Context &>())
    .def("GetSignalProbability", &I3RbSignalModel::GetSignalProbability)
    .def("GetSignalLogProbability", &I3RbSignalModel::GetSignalLogProbability)
    .def("GetSignalMean", &I3RbSignalModel::GetSignalMean)
    .def("GetLogSignalMean", &I3RbSignalModel::GetLogSignalMean)
    .def("GetHitProbability", &I3RbSignalModel::GetHitProbability)
    .def("CalcChi2", &I3RbSignalModel::CalcChi2)
    .def("GetSignalVariance", &I3RbSignalModel::GetSignalVariance)
    .def("GuessParameters", &I3RbSignalModel::GuessParameters)
    .def(icetray::python::context_suite<I3LaputopSignalModel>())
    ;
}
