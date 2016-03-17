cmake_minimum_required(VERSION 2.8.10)

project(cxxfileno C CXX)

file(GLOB CPP_FILES ${E}/libcxxfileno/*.cpp)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -O1 -g")

add_library(${PROJECT_NAME} STATIC ${CPP_FILES})

# Required on Unix OS family to be able to be linked into shared libraries.
set_target_properties(${PROJECT_NAME}
                      PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_link_libraries(${PROJECT_NAME})

# Expose B's public includes (including Boost transitively) to other
# subprojects through cache variable.
set(${PROJECT_NAME}_INCLUDE_DIRS ${E}/libcxxfileno
    CACHE INTERNAL "${PROJECT_NAME}: Include Directories" FORCE)
