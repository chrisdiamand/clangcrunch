cmake_minimum_required(VERSION 2.8.10)

project(cxxgen CXX)

file(GLOB CPP_FILES ${E}/libcxxgen/src/*.cpp)

set(CMAKE_CXX_FLAGS
    "${CMAKE_CXX_FLAGS} -Wall -O1 -g -std=c++11 -Wno-deprecated-declarations")

include_directories(
    ${E}/libcxxgen/include
    ${E}/libcxxgen/include/cxxgen
    ${srk31cxx_INCLUDE_DIRS}
    ${dwarfpp_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} STATIC ${CPP_FILES})

# Required on Unix OS family to be able to be linked into shared libraries.
set_target_properties(${PROJECT_NAME}
                      PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_link_libraries(${PROJECT_NAME} libdwarfidl libsrk31cxx libcxxfileno)

set(${PROJECT_NAME}_INCLUDE_DIRS ${E}/libcxxgen/include
                                 ${cxxfileno_INCLUDE_DIRS}
                                 ${dwarfidl_INCLUDE_DIRS}
                                 ${srk31cxx_INCLUDE_DIRS}
                                 ${Boost_INCLUDE_DIRS}
    CACHE INTERNAL "${PROJECT_NAME}: Include Directories" FORCE)
