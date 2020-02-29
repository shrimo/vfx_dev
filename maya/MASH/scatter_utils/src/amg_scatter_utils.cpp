// API for python MAYA/MASH/XGen
// 
#include <Python.h>
// #include "partio_exchange.h"
#include <ctime>
#include <iostream>
#include <string>
#include <vector>
#include "OpenEXR/ImathMatrix.h"
#include "OpenEXR/ImathMatrixAlgo.h"

using namespace std;
const float PI180 = 3.1415926535897932384626433832795 / 180.0;

inline float radian(float deg)
{
    return deg * PI180;
}
inline vector<float> flat_convert(Imath::M44f input_m44f)
{
    // return from matrix44 -> float_array16
    vector<float> float_out;
    float_out.clear();

    for (auto i = 0; i < 4; i++)
    {
        for (auto j = 0; j < 4; j++)
        {
            float_out.push_back(input_m44f[i][j]);
        }
    }
    return float_out;
}

static PyObject *set_matrix(PyObject *self, PyObject *args)
{
    PyObject *_position, *_rotation, *_scale, *_matrix;

    float position[3];
    float rotate[3];
    float scale[3];

    if (!PyArg_ParseTuple(args, "OOO", &_position, &_rotation, &_scale))
    {
        return NULL;
    }

    auto a_size = PySequence_Length(_position);
    int i;
    for (i = 0; i < a_size; i++)
    {
        position[i] = PyFloat_AsDouble(PyList_GetItem(_position, i));
        rotate[i] = PyFloat_AsDouble(PyList_GetItem(_rotation, i));
        scale[i] = PyFloat_AsDouble(PyList_GetItem(_scale, i));
    }

    Imath::M44f matrix44;
    Imath::V3f t(position[0], position[1], position[2]);
    Imath::V3f s(scale[0], scale[1], scale[2]);
    Imath::V3f r(radian(rotate[0]), radian(rotate[1]), radian(rotate[2]));
    // Matrix44 matrix44;
    matrix44.setTranslation(t);
    matrix44.scale(s);
    matrix44.rotate(r);

    vector<float> M_in;
    M_in = flat_convert(matrix44);

    PyObject *matrix_out = PyList_New(16);
    for (i = 0; i < 16; i++)
    {
        _matrix = Py_BuildValue("f", M_in[i]);
        PyList_SetItem(matrix_out, i, _matrix);
    }

    return Py_BuildValue("O", matrix_out);
}

static PyObject *get_mash_method(PyObject *self, PyObject *args)
{
    /* API for Maya/MASH
    position = (mash object).getVectorData('position')
    attr(string) - 'getVectorData', f_attr(string) - 'position'
    explorer.ocmash( (mash object), attr, f_attr) */

    /* inbox - mash object, method - 'getVectorData',
    T_val[array] - method attribute 'position, rotation, scale', 
    val_none - empty attribute */
    PyObject *inbox, *method, *imethod, *T_val[3], *val_none;

    /* T_obj[array] - (mash object).getVectorData('position, etc')
    obj_size - obj.length(), sq - iterate object 
    I_obj, I_val - get index objects *.getDoubleData('objectIndex') */
    PyObject *sq, *obj_length, *obj_size;
    PyObject *T_obj[3];
    PyObject *I_obj, *I_val;

    if (!PyArg_ParseTuple(args, "O", &inbox))
    {
        return NULL;
    }

    vector<int> idx = {0, 1, 2}; // loop iterator
    vector<string> T_name = {"position", "rotation", "scale"};
    vector<string> T_axis = {"x", "y", "z"};

    // call metod -> input_points_data.getVectorData('position (or rotation, scale)')
    val_none = Py_BuildValue("()");
    method = PyObject_GetAttrString(inbox, "getVectorData");
    for (auto &i : idx)
    {
        T_val[i] = Py_BuildValue("(s)", T_name[i].c_str());
        T_obj[i] = PyObject_CallObject(method, T_val[i]);
    }
    Py_DECREF(method);
    // getting object index from Maya/MASH -> *.getDoubleData('objectIndex')
    imethod = PyObject_GetAttrString(inbox, "getDoubleData");
    I_val = Py_BuildValue("(s)", "objectIndex");
    I_obj = PyObject_CallObject(imethod, I_val);
    
    Py_DECREF(imethod);
    Py_DECREF(I_val);

    // get amount of objects
    obj_length = PyObject_GetAttrString(T_obj[0], "length");
    obj_size = PyObject_CallObject(obj_length, val_none);
    auto a_size = PyLong_AsLong(obj_size);

    Py_DECREF(obj_length);
    Py_DECREF(obj_size);

    /* pt - position, rt - rotation, st - scale, obj_idx - object index
    0 - axis X, 1 - axis Y, 2 - axis Z */
    PyObject *pt[3], *rt[3], *st[3];

    float position[3], rotate[3], scale[3];
    vector<float> M_import;
    Imath::M44f matrix44;

    PyObject *_data_out; // = PyList_New(0);
    PyObject *index_key, *i_key;
    // PyObject *index_list = PyList_New(0);
    PyObject *dict_out = PyDict_New();
    PyObject *_matrix;

    for (auto i = 0; i < a_size; i++)
    {
        sq = PySequence_GetItem(T_obj[0], i); // read position
        for (auto &j : idx)
        {
            pt[j] = PyObject_GetAttrString(sq, T_axis[j].c_str());
            position[j] = PyFloat_AsDouble(pt[j]);
        }
        sq = PySequence_GetItem(T_obj[1], i); // read rotation
        for (auto &j : idx)
        {
            rt[j] = PyObject_GetAttrString(sq, T_axis[j].c_str());
            rotate[j] = PyFloat_AsDouble(rt[j]);
        }
        sq = PySequence_GetItem(T_obj[2], i); // read scale
        for (auto &j : idx)
        {
            st[j] = PyObject_GetAttrString(sq, T_axis[j].c_str());
            scale[j] = PyFloat_AsDouble(st[j]);
        }

        index_key = PySequence_GetItem(I_obj, i); // read index
        int ind_key = (int)PyFloat_AsDouble(index_key);
        i_key = Py_BuildValue("i", ind_key);                    // (int) key for dict _data_out
        // PyList_Append(index_list, Py_BuildValue("i", ind_key)); // append index to list

        // set data for matrix44 convert (x,y,z) -> Imath::V3f
        Imath::V3f t(position[0], position[1], position[2]);
        Imath::V3f s(scale[0], scale[1], scale[2]);
        Imath::V3f r(radian(rotate[0]), radian(rotate[1]), radian(rotate[2]));

        // matrix44.makeIdentity(); // M44f(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
        matrix44.setTranslation(t);
        matrix44.scale(s);
        matrix44.rotate(r);
        M_import = flat_convert(matrix44); //convert M44f to flat array

        /* pointer to list (_data_out) in dictionary (dict_out)
        if there is no key, we create a pointer to the list 
        and associate it with the key. like setdefault() in python*/
        if (!PyDict_Contains(dict_out, i_key))
        {
            _data_out = PyList_New(0);
            PyDict_SetItem(dict_out, i_key, _data_out);
        }
        else
        {
            _data_out = PyDict_GetItem(dict_out, i_key);
        }
        // filling in dictionary list (_data_out) values
        for (auto n = 0; n < 16; n++)
        {
            _matrix = Py_BuildValue("f", M_import[n]);
            PyList_Append(_data_out, _matrix);
        }
    }    
    // return Py_BuildValue("iOO", a_size, index_list, dict_out);
    return Py_BuildValue("O", dict_out);
}

static PyMethodDef amg_scatter_utils_Methods[] = {
    {"M44f", set_matrix, METH_VARARGS, "Set attribute for Matrix"},
    {"ocmash", get_mash_method, METH_VARARGS, "Get matrix44 from Maya/MASH"},
    {NULL, NULL, 0, NULL}};

PyMODINIT_FUNC initamg_scatter_utils(void)
{
    PyObject *ver, *m;
    m = Py_InitModule("amg_scatter_utils", amg_scatter_utils_Methods);
    ver = PyString_FromString("version - 1.0.0");
    
    (void)Py_InitModule("amg_scatter_utils", amg_scatter_utils_Methods);
    PyModule_AddObject(m, "__version__", ver);
}
