/**
 * copyright  (C) 2014
 *
 * The Icecube Collaboration
 *
 * $Id: I3ParameterMap.h 173728 2019-06-04 17:46:14Z dsoldin $
 *
 * \file I3ParameterMap.h
 *
 * \author Javier Gonzalez
 * \date 18 Feb 2014
 * \version $Revision: 173728 $
 * Last changed by $LastChangedBy: dsoldin $ on $LastChangedDate: 2019-06-04 12:46:14 -0500 (Tue, 04 Jun 2019) $
 */

#ifndef _rockbottom_I3ParameterMap_h_
#define _rockbottom_I3ParameterMap_h_

static const char CVSId__I3ParameterMap[] =
"$Id: I3ParameterMap.h 173728 2019-06-04 17:46:14Z dsoldin $";

static const unsigned i3parametermap_version_ = 1;


#include <icetray/I3FrameObject.h>
#include <icetray/I3PointerTypedefs.h>
#include <dataclasses/I3Vector.h>
#include <string>
#include <algorithm>

#include <map>
#include <boost/iterator/zip_iterator.hpp>
#include <boost/iterator/transform_iterator.hpp>



class I3ParameterMap: public I3FrameObject {
  typedef boost::tuple<std::vector<std::string>::const_iterator,
                       std::vector<double>::const_iterator> Tuple;

  typedef boost::zip_iterator<Tuple> ZipIterator;

  struct Zip :
    public std::unary_function<std::pair<std::string, double>, const boost::tuple<std::string, double>&>
  {
    std::pair<std::string, double> operator()(const boost::tuple<std::string, double>& p) const
    {
      return std::pair<std::string, double>(p.get<0>(),p.get<1>());
    }
  };

public:
  typedef boost::transform_iterator<Zip, ZipIterator, std::pair<std::string, double> > Iterator;

  Iterator Begin() const
  {
    return Iterator(ZipIterator(Tuple(fParameterNames.begin(), fParameters.begin())), Zip());
  }
  Iterator End() const
  {
    return Iterator(ZipIterator(Tuple(fParameterNames.end(), fParameters.end())), Zip());
  }

  I3ParameterMap(){}

  I3ParameterMap(std::string name,
                 I3Vector<double> parameters, I3Vector<std::string> parameterNames):
    fName(name),
    fParameters(parameters),
    fParameterNames(parameterNames)
  {}
  ~I3ParameterMap(){}

  std::string GetName() const
  { return fName; }

  unsigned int GetSize() const
  { return fParameters.size(); }

  std::string GetParameterName(unsigned int i) const
  { return fParameterNames[i]; }

  unsigned int GetParameterIndex(std::string name) const
  {
    I3Vector<std::string>::const_iterator it = std::find(fParameterNames.begin(), fParameterNames.end(), name);
    if (it == fParameterNames.end())
      log_fatal("There is no parameter '%s' in '%s' parameter container.", name.c_str(), fName.c_str());
    return it - fParameterNames.begin();
  }

  double GetParameter(unsigned int i) const
  { return fParameters[i]; }

  void SetParameter(unsigned int i, double v)
  { fParameters[i] = v; }

  double HasParameter(std::string name) const
  { return std::find(fParameterNames.begin(), fParameterNames.end(), name) != fParameterNames.end(); }

  double GetParameterByName(std::string name) const
  { return fParameters[GetParameterIndex(name)]; }

  void SetParameterByName(std::string name, double v)
  { fParameters[GetParameterIndex(name)] = v; }

  template <class Archive>
  void serialize(Archive & ar, unsigned version);

private:
  std::string fName;
  I3Vector<double> fParameters;
  I3Vector<std::string> fParameterNames;

}; // class I3ParameterMap


I3_POINTER_TYPEDEFS(I3ParameterMap);

I3_CLASS_VERSION(I3ParameterMap, i3parametermap_version_);

#endif // __I3ParameterMap_h_
