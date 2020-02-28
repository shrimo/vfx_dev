// finding asymmetric polygons relative to X axis
#include <Python.h>
#include <cmath>
#include <thread>
#include <mutex>
#include <algorithm>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <maya/MSelectionList.h>
#include <maya/MString.h>
#include <maya/MItMeshPolygon.h>
#include <maya/MObject.h>
#include <maya/MDagPath.h>
#include <maya/MPoint.h>
#include <maya/MGlobal.h>
#include <maya/MPointArray.h>
#include <boost/config.hpp>
#include <boost/python.hpp>
#include <boost/format.hpp>

using namespace std;
namespace py = boost::python;
#define API extern "C" BOOST_SYMBOL_EXPORT

struct Point;
struct Face;
using VerticesList = vector<Point>;
using ShapeFaces = map<string, set<int>>;
using SliceDict = map<int, vector<Face>>;
float TOLERANCE;
const string __version__("1.3.3");

void maya_message(const string &name)
{
	MGlobal::displayInfo(MString(name.c_str()));
}

inline float py_scalar(py::object scalar)
{
	return PyFloat_AsDouble(PyObject_GetAttrString(scalar.ptr(), "real"));
}

template <typename T>
inline vector<T> py_list2stl_vector(const py::object &iterable)
{
	return vector<T>(py::stl_input_iterator<T>(iterable), py::stl_input_iterator<T>());
}

inline py::dict stl_map2py_dict(const ShapeFaces &sf)
{
	py::dict result;
	for (const auto &shape_it : sf)
	{
		py::list python_components;
		for (int index : shape_it.second)
			python_components.append(index);
		result[shape_it.first] = python_components;
	}
	return result;
}

struct Point
{
	float x, y, z;
};

struct Face
{
	int index;
	string shape;
	float center[3];
	VerticesList vertices;
	int slice;
	bool ignored;
	Face(unsigned int index, string &shape, float m_center[4], VerticesList m_vertices)
	{
		this->ignored = false;
		this->index = index;
		this->shape = shape;
		this->vertices = m_vertices;
		copy(m_center, m_center + 3, this->center);
		float max_y = -1000;
		for (auto &vert : this->vertices)
			if (vert.y > max_y)
				max_y = vert.y;
		this->slice = (int)max_y;
	}
};

struct Parallel
{
	ShapeFaces non_symmetrical;

	inline bool compare_vertices(VerticesList &vertices, VerticesList &opposite_vertices)
	{
		int idx = 0;
		int ver_size = static_cast<int>(vertices.size());
		int opp_ver_size = static_cast<int>(opposite_vertices.size());
		if (ver_size != opp_ver_size)
			return false;
		idx = 0;
		for (auto &vx : vertices)
		{
			for (auto &opp_vx : opposite_vertices)
			{
				float x = std::fabs(vx.x + opp_vx.x);
				float y = std::fabs(vx.y - opp_vx.y);
				float z = std::fabs(vx.z - opp_vx.z);
				if ((x < TOLERANCE) && (y < TOLERANCE) && (z < TOLERANCE))
				{
					++idx;
					break;
				}
			}
		}
		if (idx == opp_ver_size)
			return true;
		return false;
	}

	void compare_slice(vector<Face> &first, vector<Face> &second)
	{
		bool face_matched;
		for (auto &face : first)
		{
			if (face.ignored)
				continue;
			face_matched = false;
			for (auto &opposite_face : second)
			{
				if (compare_vertices(face.vertices, opposite_face.vertices))
				{
					opposite_face.ignored = true;
					face_matched = true;
					break;
				}
			}
			if (!face_matched)
				non_symmetrical[face.shape].insert(face.index);
		}
	}

	void compare(SliceDict &first_side, SliceDict &second_side)
	{
		bool face_matched;
		for (auto &slice_it : first_side)
		{
			auto slice = slice_it.second;
			auto opposite_slice = second_side[slice_it.first];
			compare_slice(slice, opposite_slice);
			compare_slice(opposite_slice, slice);
		}
	}

	thread compare_thread(SliceDict &arg1, SliceDict &arg2)
	{
		return thread(&Parallel::compare, this, ref(arg1), ref(arg2));
	}
};

ShapeFaces compare(int threads, SliceDict *left_side, SliceDict *right_side)
{
	ShapeFaces non_symmetrical;
	Parallel *parallel = new Parallel[threads];
	thread *t_parallel = new thread[threads];
	for (int i = 0; i < threads; i++)
		t_parallel[i] = parallel[i].compare_thread(left_side[i], right_side[i]);
	for (int i = 0; i < threads; i++)
	{
		t_parallel[i].join();
		for (const auto &shape_it : parallel[i].non_symmetrical)
			non_symmetrical[shape_it.first].insert(shape_it.second.begin(), shape_it.second.end());
	}
	delete[] parallel;
	delete[] t_parallel;
	return non_symmetrical;
}

API py::object get_non_symmetrical(py::tuple args, py::dict kw)
{
	py::object o_shapes = py::extract<py::object>(args[0]);
	vector<string> shapes = py_list2stl_vector<string>(o_shapes);
	MSelectionList sel;
	MObject m_obj;
	MDagPath m_dag_path;
	MPointArray points_array;
	float vertex[4];
	float center[4];
	const int threads = thread::hardware_concurrency();
	SliceDict *left_side = new SliceDict[threads];
	SliceDict *right_side = new SliceDict[threads];
	maya_message(
		(boost::format("Using %d threads") % threads).str());
	if (kw.has_key("tolerance"))
		TOLERANCE = py_scalar(kw["tolerance"]);
	else
		TOLERANCE = 1e-4;
	maya_message(
		(boost::format("C++ Tolerance: %f") % TOLERANCE).str());
	for (auto &shape : shapes)
	{
		sel.clear();
		sel.add(shape.c_str());
		sel.getDagPath(0, m_dag_path, m_obj);
		MItMeshPolygon poly_obj(m_dag_path, m_obj);
		int dummyIndex;
		for (unsigned int index = 0; index < poly_obj.count(); index++)
		{
			poly_obj.setIndex(index, dummyIndex);
			MPoint m_center = poly_obj.center(MSpace::kWorld);
			m_center.get(center);
			points_array.clear();
			VerticesList vertices;
			poly_obj.getPoints(points_array, MSpace::kWorld);
			for (unsigned int vn = 0; vn < points_array.length(); vn++)
			{
				points_array[vn].get(vertex);
				vertices.push_back({vertex[0], vertex[1], vertex[2]});
			}
			Face face(index, shape, center, vertices);
			if (face.center[0] < -TOLERANCE)
				left_side[face.slice % threads][face.slice].push_back(face);
			else if (face.center[0] > TOLERANCE)
				right_side[face.slice % threads][face.slice].push_back(face);
		}
	}
	ShapeFaces non_symmetrical = compare(threads, left_side, right_side);
	delete[] left_side;
	delete[] right_side;
	py::dict face_dict(stl_map2py_dict(non_symmetrical));
	py::dict result;
	result["version"] = __version__;
	result["non_symmetrical"] = face_dict;
	return result;
}
