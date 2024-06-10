
cmake_minimum_required(VERSION 3.20)
project(C_Project C)

# Add path for custom modules
set(CMAKE_MODULE_PATH
        ${CMAKE_MODULE_PATH}
        "${CMAKE_CURRENT_SOURCE_DIR}/cmake"
        )

include(CompilerSetup)

add_executable(executable
        main.c
        substitution.c substitution.h test_substitution.c percent.c percent.h test_percent.c)

enable_c_warnings_for(executable)
link_math_library(executable)