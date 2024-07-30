# Usage:
#   mkdir build && cmake --build build

# Set CMake Restrictions.
cmake_minimum_required(VERSION "3.17")
set(CMAKE_CXX_STANDARD 17)

# Set project meta data.
project(hephaestus
VERSION "0.1.0"
DESCRIPTION "A collection of generally useful functions and classes"
LANGUAGES "CXX"
)

# If Hephaestus is not the main project, the build settings are taken from the parent.
if (CMAKE_PROJECT_NAME STREQUAL "hephaestus")

    # Set Hephaestus to be built as a static library unless otherwise specified. 
    option(BUILD_SHARED_LIBS "Build shared libraries." OFF)
    option(BUILD_STATIC_LIBS "Build the static library." ON)

    # Output files to sane central locations in build directory. 
    set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
    
endif()

# Create a unit test build using GTest Framework.
option(HEPHAESTUS_BUILD_TESTS "Build a unit test executable." OFF)

# All internal includes should be like `#include 'hephaestus/<module>/<headerfile>'
include_directories("include")

# Build necessary subdirectories
add_subdirectory(src)

# Combine all of the public libraries into one library (more like an alias).
# Users attempting to use this will only need to link the hephaestus "library" to use/refer to
# all of the public modules.
add_library(${PROJECT_NAME} INTERFACE)
target_link_libraries(${PROJECT_NAME} INTERFACE
    hephaestus::common
    hephaestus::containers
)

# Create a unit test executable.
if (HEPHAESTUS_BUILD_TESTS)
    add_subdirectory(test)
endif()
