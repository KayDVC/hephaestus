# Set CMake Restrictions.
cmake_minimum_required(VERSION "3.17")
set(CMAKE_CXX_STANDARD 17)

# Set project meta data.
project("Hephaestus"
VERSION "0.1.0"
DESCRIPTION "A collection of generally useful functions and classes"
LANGUAGES "CXX"
)

# All internal includes should be like `#include 'hephaestus/<module>/<headerfile>'
include_directories("include")

if (CMAKE_PROJECT_NAME STREQUAL "Hephaestus")
    option(BUILD_SHARED_LIBS "Build shared libraries." OFF)
endif()

# build necessary subdirectories
add_subdirectory(src)