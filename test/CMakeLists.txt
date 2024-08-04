# Download Google Test Source.
include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG "v1.15.0" # https://github.com/google/googletest/releases/tag/v1.15.0
)

# For Windows: Prevent overriding the parent project's compiler/linker settings.
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# Add testing files to executable.
add_executable(
  hephaestus_test
  hello_test.cpp
)

# Add the Hephaestus and GTest library's code to the executable.
target_link_libraries(
  hephaestus_test
  GTest::gtest_main # Needed to detect and run test cases automatically.
  hephaestus        
)

# Ensure all test cases can access internal header files as well.
target_include_directories(hephaestus_test
	PRIVATE
	${PROJECT_SOURCE_DIR}/src
)