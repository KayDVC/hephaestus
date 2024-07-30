
## 
# Generated using `Generate Submodule Cmake Lists Utility` v1.0.0
##

# Create a variable to use in place of submodule name
set(subm_name common)

# Add all source and header files in submodule
add_library(${subm_name}
file.cpp
${PROJECT_SOURCE_DIR}/include/hephaestus/common/conversions.h
${PROJECT_SOURCE_DIR}/include/hephaestus/common/sizes.h
${PROJECT_SOURCE_DIR}/include/hephaestus/common/enums.h
${PROJECT_SOURCE_DIR}/include/hephaestus/common/math.h
)

# Ensure submodule accessible using hephaestus::<submodule_name>.
# Note, does not account for nested folders.
add_library(${PROJECT_NAME}::${subm_name} ALIAS ${subm_name})

# Submodule Meta Data
set_target_properties(${subm_name} PROPERTIES VERSION ${PROJECT_VERSION})
set_target_properties(${subm_name} PROPERTIES SOVERSION ${PROJECT_VERSION_MAJOR})
