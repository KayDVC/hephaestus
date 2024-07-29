
## 
# Generated using `Generate Submodule Cmake Lists Utility` v1.0.0
##

# Create a variable to use in place of submodule name
set(subm_name logging)

# Add all source and header files in submodule
add_library(${subm_name}


)

# Ensure submodule accessible using Hephaestus::<submodule_name>
add_library(${PROJECT_NAME}::${subm_name} ALIAS ${subm_name})

# Submodule Meta Data
set_target_properties(${subm_name} PROPERTIES VERSION ${PROJECT_VERSION})
set_target_properties(${subm_name} PROPERTIES SOVERSION ${PROJECT_VERSION_MAJOR})
