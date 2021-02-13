//This file should go in rock_bottom/public/pybindings/

#include <tableio/converter/pybindings.h>
#include <rock_bottom/models/SkeletonSignalModel.h>
#include <icetray/python/context_suite.hpp>

using namespace boost::python;


void registerSkeletonSignalModel()
{
  class_<SkeletonSignalModel, bases<I3FrameObject>, boost::noncopyable>
    ("SkeletonSignalModel", boost::python::init<const I3Context &>())
    .def("GetSignalProbability", &I3RbSignalModel::GetSignalProbability)
    .def("GetSignalLogProbability", &I3RbSignalModel::GetSignalLogProbability)
    .def("GetSignalMean", &I3RbSignalModel::GetSignalMean)
    .def("GetLogSignalMean", &I3RbSignalModel::GetLogSignalMean)
    .def("GetHitProbability", &I3RbSignalModel::GetHitProbability)
    .def("CalcChi2", &I3RbSignalModel::CalcChi2)
    .def("GetSignalVariance", &I3RbSignalModel::GetSignalVariance)
    .def("GuessParameters", &I3RbSignalModel::GuessParameters)
    .def("TimingLLH", &I3RbSignalModel::TimingLLH)
    .def(icetray::python::context_suite<SkeletonSignalModel>())
    ;
}
