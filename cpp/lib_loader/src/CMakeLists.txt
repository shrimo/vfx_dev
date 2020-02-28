# DEPLOY: //bstorage/rep/set/scripts/amg/system/cpp/
PROJECT(lib_loader)
SET (SRC "lib_loader.cpp")

CMAKE_MINIMUM_REQUIRED (VERSION 2.4.6)
if (COMMAND cmake_policy)
    cmake_policy(SET CMP0003 NEW)  # Libraries linked via full path no longer produce linker search paths.
    cmake_policy(SET CMP0015 NEW)  # to supress relative library directory warnings
endif ()    
MARK_AS_ADVANCED (CMAKE_BACKWARDS_COMPATIBILITY)
## allow more human readable "if then else" constructs
SET(CMAKE_ALLOW_LOOSE_LOOP_CONSTRUCTS TRUE)
## Use verbose make file
SET (CMAKE_VERBOSE_MAKEFILE TRUE)
SET (CMAKE_BUILD_TYPE "Release")

## CHANGE THIS TO WHERE YOU PUT THE MAIN DIRECTORY
SET (AMG_HOME ${CMAKE_SOURCE_DIR})
message(STATUS "AMG_HOME = " ${AMG_HOME})
SET (CMAKE_INSTALL_PREFIX "${AMG_HOME}")

# message("* CMAKE_CURRENT_BINARY_DIR = " ${CMAKE_CURRENT_BINARY_DIR})
SET (CMAKE_MODULE_PATH ${AMG_HOME}/cmake)

## Setup platform specific helper defines build variants
IF (WIN32)
    SET (BOOST_ROOT "//fstorage/projects/dev/lib/boost/boost-1.67_msvc_2015")
    SET (BOOST_INCLUDE_PATH "${BOOST_ROOT}/include")
    SET (BOOST_LIBRARY_PATH "${BOOST_ROOT}/lib")
    SET (BOOST_LIBS
        "boost_python27-vc140-mt-x64-1_67"
        "boost_system-vc140-mt-x64-1_67"
        "boost_filesystem-vc140-mt-x64-1_67")
    SET (PYTHON_INCLUDE_PATH "//bstorage/rep/set/include/windows/python2.7")
    # SET (MAYA_LOCATION "/usr/autodesk/maya2018" CACHE STRING "Maya location")
    SET (MAYA_LOCATION "C:/Program Files/Autodesk/maya2018")
    SET (MAYA_INCLUDE_PATH "${MAYA_LOCATION}/include")
    SET (MAYA_LIBRARY_PATH "${MAYA_LOCATION}/lib")
    SET (EXTRA_LIBRARY_PATH "//bstorage/rep/set/libs/lib_windows/dependencies")
    add_definitions (-DWIN32)
    add_definitions (-DBOOST_ALL_NO_LIB)
    add_definitions (-Ox)
ELSE (WIN32)
    SET (BOOST_ROOT "/home/shrimo/lib/boost")
    SET (BOOST_INCLUDE_PATH "${BOOST_ROOT}/include")
    SET (BOOST_LIBRARY_PATH "${BOOST_ROOT}/lib")
    SET (BOOST_LIBS
        "${BOOST_LIBRARY_PATH}/libboost_python27.so.1.69.0"
        "${BOOST_LIBRARY_PATH}/libboost_system.so.1.69.0"
        "${BOOST_LIBRARY_PATH}/libboost_filesystem.so.1.69.0")
    SET (PYTHON_INCLUDE_PATH "/usr/autodesk/maya2019/include/python2.7")
    SET (MAYA_LOCATION "/usr/autodesk/maya2019" CACHE STRING "Maya location")
    # SET (MAYA_LOCATION "//bstorage/rep/cg/autodesk/maya2018.5")
    SET (MAYA_INCLUDE_PATH "${MAYA_LOCATION}/include")
    SET (MAYA_LIBRARY_PATH "${MAYA_LOCATION}/lib")
    SET (EXTRA_LIBRARY_PATH "/usr/local/lib")   
    add_definitions (-std=c++11)
    add_definitions (-fPIC)
    add_definitions (-Ofast)
    # add_definitions (-pthread)
ENDIF (WIN32)

include_directories (
    "${PYTHON_INCLUDE_PATH}"
    "${BOOST_INCLUDE_PATH}"
)
link_directories (
    ${EXTRA_LIBRARY_PATH}
    ${MAYA_LIBRARY_PATH}
    ${BOOST_LIBRARY_PATH}
)

ADD_LIBRARY (${PROJECT_NAME} SHARED ${SRC})
set_target_properties (${PROJECT_NAME} PROPERTIES PREFIX "")
IF (WIN32)
    set_target_properties (${PROJECT_NAME} PROPERTIES SUFFIX ".pyd")
ENDIF (WIN32)

target_link_libraries(
    ${PROJECT_NAME}
    ${BOOST_LIBS}
)

install (
    TARGETS ${PROJECT_NAME}
    DESTINATION "${CMAKE_INSTALL_PREFIX}"
)
