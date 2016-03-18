cmake_minimum_required(VERSION 2.8.10)

# You can tweak some common (for all subprojects) stuff here. For example:

set(E ${CMAKE_SOURCE_DIR}/../external)

set(CMAKE_DISABLE_IN_SOURCE_BUILD ON)
set(CMAKE_DISABLE_SOURCE_CHANGES  ON)

if ("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
  message(SEND_ERROR "In-source builds are not allowed.")
endif ()

set(CMAKE_VERBOSE_MAKEFILE ON)
set(CMAKE_COLOR_MAKEFILE   ON)

# Remove 'lib' prefix for shared libraries on Windows
if (WIN32)
  set(CMAKE_SHARED_LIBRARY_PREFIX "")
endif ()

# Subprojects in dependency order.
add_subdirectory(libcxxfileno)
add_subdirectory(libsrk31cxx)
add_subdirectory(libdwarfpp)
add_subdirectory(libcxxgen)
#add_subdirectory(dwarfidl)
