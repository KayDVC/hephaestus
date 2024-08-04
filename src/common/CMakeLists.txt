
## 
# Generated using `Generate Submodule Cmake Lists Utility` 1.0.0
##

# Create a variable to use in place of submodule name
set(subm_name common)

# Add all source and header files in submodule
add_library(${subm_name}
string.cpp
file.cpp
${PROJECT_SOURCE_DIR}/include/hephaestus/common/sizes.h
${PROJECT_SOURCE_DIR}/include/hephaestus/common/types.h
${PROJECT_SOURCE_DIR}/include/hephaestus/common/math.h
${PROJECT_SOURCE_DIR}/include/hephaestus/common/string.h
)

# Ensure all files within the current directory accessible to files
# in this submodule. These are considered private and should not 
# be accessible to external users.
target_include_directories(${subm_name}
	PRIVATE
	${CMAKE_CURRENT_LIST_DIR}
)

# Ensure submodule accessible using hephaestus::<submodule_name>.
# Note, does not account for nested folders.
add_library(${PROJECT_NAME}::${subm_name} ALIAS ${subm_name})

# Submodule Meta Data
set_target_properties(${subm_name} PROPERTIES VERSION ${PROJECT_VERSION})
set_target_properties(${subm_name} PROPERTIES SOVERSION ${PROJECT_VERSION_MAJOR})
