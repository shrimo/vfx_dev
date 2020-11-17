/*
 * ------------------------------
 * description: Dynamic Library Loader
 * ------------------------------
 */

#include <Python.h>
#include <iostream>
#include <string>
#include <boost/dll.hpp>
#include <boost/python.hpp>
#include <boost/filesystem.hpp>

using namespace std;
namespace py = boost::python;

py::object call(const py::tuple &args, const py::dict &kw)
{
    py::str lib_pystr = py::extract<py::str>(kw["lib"]);
    string lib_str = py::extract<string>(lib_pystr);
    boost::filesystem::path lib_path = lib_str;
    string func_name = py::extract<string>(kw["func"]);
    function<py::object(const py::tuple&, const py::dict&)> func_ext;
    func_ext = boost::dll::import<py::object(const py::tuple&, const py::dict&)>(lib_path, func_name.c_str());
    py::object out_object = func_ext(args, kw);
    return out_object;
}

BOOST_PYTHON_MODULE(lib_loader)
{
    py::def("call", py::raw_function(call));
}
