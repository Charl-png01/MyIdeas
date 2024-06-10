cmake_minimum_required(VERSION 3.20)
project(C_Project C)

set(CMAKE_C_STANDARD 17)

# Add path for custom modules
set(CMAKE_MODULE_PATH
        ${CMAKE_MODULE_PATH}
        "${CMAKE_CURRENT_SOURCE_DIR}/cmake"
        )

include(CompilerSetup)

add_executable(executable
        main.c
        allocation.c allocation.h broken_sort.c broken_sort.h)

enable_c_warnings_for(executable)
link_math_library(executable)

