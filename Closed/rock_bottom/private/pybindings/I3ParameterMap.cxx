/**
 * copyright  (C) 2014
 *
 * The Icecube Collaboration
 *
 * $Id: I3ParameterMap.cxx 173671 2019-06-03 17:59:13Z acoleman $
 *
 * \author Javier Gonzalez
 * \date 18 Feb 2014
 * \version $Revision: 173671 $
 * Last changed by $LastChangedBy: acoleman $ on $LastChangedDate: 2019-06-03 12:59:13 -0500 (Mon, 03 Jun 2019) $
 */

#include <rock_bottom/I3ParameterMap.h>
#include <boost/iterator/transform_iterator.hpp>
#include <sstream>

namespace bp = boost::python;

using bp::range;
using bp::tuple;
using bp::iterator;
using bp::object;
using bp::class_;
using bp::init;
using bp::bases;
using bp::list;
using bp::make_tuple;

using std::string;
using std::ostringstream;
using std::pair;

namespace i3_parameter_map {
  static string repr(const I3ParameterMap& x)
  {
    ostringstream str;
    str << "I3ParameterMap(\""<< x.GetName() << "\", ";
    if (x.GetSize()) {
      str << "(";
      for(unsigned int i = 0; i != x.GetSize(); i++) {
        if (i)
          str << ", ";
        str << x.GetParameter(i);
      }
      str << "), (";
      for(unsigned int i = 0; i != x.GetSize(); i++) {
        if (i)
          str << ", ";
        str << "\"" << x.GetParameterName(i) << "\"";
      }
      str << ")";
    }
    str << ")";
    return str.str();
  }

  static string str(const I3ParameterMap& x)
  {
    ostringstream str;
    str << x.GetName() << ": ";
    if (x.GetSize()) {
      str << "{";
      for(unsigned int i = 0; i != x.GetSize(); i++) {
        if (i)
          str << ", ";
        str << "\"" << x.GetParameterName(i) << "\": " << x.GetParameter(i);
      }
      str << "}";
    }
    return str.str();
  }

  // return a list of keys
  static list keys(const I3ParameterMap& x)
  {
    list t;
    for(unsigned int i = 0; i != x.GetSize(); i++)
      t.append(x.GetParameterName(i));
    return t;
  }
  // return a list of values
  static list values(const I3ParameterMap& x)
  {
    list t;
    for(unsigned int i = 0; i != x.GetSize(); i++)
      t.append(x.GetParameter(i));
    return t;
  }
  // return a list of (key,value) tuples
  static list items(I3ParameterMap const&  x)
  {
    list t;
    for(unsigned int i = 0; i != x.GetSize(); i++)
      t.append(make_tuple(x.GetParameterName(i), x.GetParameter(i)));
    return t;
  }

  // set up operators to extract the key, value, or a tuple from a pair
  struct iterkeys
  {
    typedef string result_type;
    result_type operator()(pair<string, double> const& x) const
    {
      return x.first;
    }
  };

  struct itervalues
  {
    typedef double result_type;
    result_type operator()(pair<string, double> const& x) const
    {
      return x.second;
    }
  };

  struct iteritems {
    typedef tuple result_type;
    result_type operator()(pair<string, double> const& x) const
    {
      return make_tuple(x.first,x.second);
    }
  };

  template <typename Transform>
  struct make_iterator
  {
    typedef boost::transform_iterator<Transform, I3ParameterMap::Iterator> iterator;

    static iterator begin(const I3ParameterMap& m)
    {
      return boost::make_transform_iterator(m.Begin(), Transform());
    }
    static iterator end(const I3ParameterMap& m)
    {
      return boost::make_transform_iterator(m.End(), Transform());
    }
    static object range()
    {
      return bp::range(&begin, &end);
    }
  };

}


using namespace i3_parameter_map;

void register_I3ParameterMap()
{
  class_<I3ParameterMap, bases<I3FrameObject>, I3ParameterMapPtr>("I3ParameterMap", init<string,I3Vector<double>,I3Vector<string> >())
    //.def(dataclass_suite<I3ParameterMap >())
    .def("__repr__", &repr)
    .def("__str__", &str)
    .def("__iter__", make_iterator<iterkeys>::range())
    .def("iteritems", make_iterator<iteritems>::range())
    .def("iterkeys", make_iterator<iterkeys>::range())
    .def("itervalues", make_iterator<itervalues>::range())
    .def("keys", &keys, "m.keys() -> list of m's (key,value) pairs\n")
    .def("values", &values, "m.keys() -> list of m's values\n")
    .def("items", &items, "m.keys() -> list of m's keys\n")
    .def("parameter_name", &I3ParameterMap::GetParameterName)
    .def("parameter_index", &I3ParameterMap::GetParameterIndex)
    .def("__setitem__", &I3ParameterMap::SetParameterByName)
    .def("__getitem__", &I3ParameterMap::GetParameterByName)
    .def("__contains__", &I3ParameterMap::HasParameter)
    .def("__len__", &I3ParameterMap::GetSize)
    .add_property("name", &I3ParameterMap::GetName)
    .def("get_parameter", &I3ParameterMap::GetParameter)
    .def("set_parameter", &I3ParameterMap::SetParameter)
    ;

  register_pointer_conversions<I3ParameterMap>();
}
