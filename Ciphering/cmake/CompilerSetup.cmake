#[=======================================================================[.rst:
CompilerSetup
-------

Provides functions to turn on lots of compiler warnings for a specified target,
enable color output, and so forth

Functions
^^^^^^^^^^^^^^^^

This module provides the following functions:

``enable_warnings_for(<target>)``
  Turns on warnings for the specified target

``colorize_output()``
  Turns on color diagnostics, sometimes needed

``link_math_library(<target>)``
  Checks whether libm needs to be specifically linked for target and
  links it if needed

#]=======================================================================]

# Should probably be replaced with CheckCompilerFlag which in turns defines
# check_compiler_flag(lang flag var) instead of the language
# specific ones, except the non-language specific one requires CMake 3.19+
include(CheckCCompilerFlag)
include(CheckCXXCompilerFlag)

function(_add_c_flag _target _flag)
    string(REGEX REPLACE "[^A-Za-z0-9]" "" _flagvar "${_flag}")
    check_c_compiler_flag(${_flag} SUPPORTS_WARNING_${_flagvar})
    if(SUPPORTS_WARNING_${_flagvar})
        target_compile_options(${_target} PRIVATE "${_flag}")
    endif()
endfunction()

macro(_add_cpp_flag _flag)
    string(REGEX REPLACE "[^A-Za-z0-9]" "" _flagvar "${_flag}")
    check_cxx_compiler_flag(${_flag} SUPPORTS_WARNING_${_flagvar})
    if(SUPPORTS_WARNING_${_flagvar})
        target_compile_options(${target} PRIVATE "${_flag}")
    endif()
endmacro()

function(enable_c_warnings_for target)
    # Maybe these should be generator expressions instead, but this seems to
    # work just fine
    if("${CMAKE_C_COMPILER_ID}}" MATCHES "Clang")
        # Matches is used to allow for Clang or AppleClang

        # Use theory of turn on all warnings, but disable ones that we don't care about
        _add_c_flag(${target} -Weverything)
        _add_c_flag(${target} -Wno-poison-system-directories)
    elseif("${CMAKE_C_COMPILER_ID}" STREQUAL "GNU")
        # Large warning groups
        _add_c_flag(${target} -Wall)
        _add_c_flag(${target} -Wextra)
        _add_c_flag(${target} -Wpedantic)
        # Individual warnings
    elseif("${CMAKE_C_COMPILER_ID}" STREQUAL "MSVC")
        _add_c_flag(${target} /W3)
    else()
        message(WARNING "Unknown compiler '${CMAKE_CXX_COMPILER_ID}', no warnings set")
    endif()
endfunction()

function(enable_cpp_warnings_for target)
    # Maybe these should be generator expressions instead, but this seems to
    # work just fine
    if("${CMAKE_CXX_COMPILER_ID}}" MATCHES "Clang")
        # Matches is used to allow for Clang or AppleClang

        # Use theory of turn on all warnings, but disable ones that we don't care about
        _add_cpp_flag(${target} PRIVATE -Weverything)
        _add_cpp_flag(${target} PRIVATE -Wno-c++98-compat)
        _add_cpp_flag(${target} PRIVATE -Wno-c++98-compat-pedantic)
        _add_cpp_flag(${target} PRIVATE -Wno-padded)
        _add_cpp_flag(${target} PRIVATE -Wno-documentation-unknown-command)
    elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
        # Large warning groups
        _add_cpp_flag("-Wall")
        _add_cpp_flag(${target} PRIVATE -Wextra)
        _add_cpp_flag(${target} PRIVATE -Wpedantic)
        # Individual warnings
        _add_cpp_flag(${target} PRIVATE -Walloc-zero)
        _add_cpp_flag(${target} PRIVATE -Wcast-align)
        _add_cpp_flag(${target} PRIVATE -Wcast-qual)
        _add_cpp_flag(${target} PRIVATE -Wconditionally-supported)
        _add_cpp_flag(${target} PRIVATE -Wconversion)
        _add_cpp_flag(${target} PRIVATE -Wctor-dtor-privacy)
        _add_cpp_flag(${target} PRIVATE -Wdate-time)
        _add_cpp_flag(${target} PRIVATE -Wdeprecated-copy-dtor)
        _add_cpp_flag(${target} PRIVATE -Wdouble-promotion)
        _add_cpp_flag(${target} PRIVATE -Wduplicated-branches)
        _add_cpp_flag(${target} PRIVATE -Wduplicated-cond)
        _add_cpp_flag(${target} PRIVATE -Wextra-semi)
        _add_cpp_flag(${target} PRIVATE -Wfloat-equal)
        _add_cpp_flag(${target} PRIVATE -Wformat=2)
        _add_cpp_flag(${target} PRIVATE -Wlogical-op)
        _add_cpp_flag(${target} PRIVATE -Wmissing-declarations)
        _add_cpp_flag(${target} PRIVATE -Wmissing-profile)
        _add_cpp_flag(${target} PRIVATE -Wno-long-long)
        _add_cpp_flag(${target} PRIVATE -Wno-pmf-conversions)
        _add_cpp_flag(${target} PRIVATE -Wnoexcept)
        _add_cpp_flag(${target} PRIVATE -Wnon-virtual-dtor)
        _add_cpp_flag(${target} PRIVATE -Wnormalized)
        _add_cpp_flag(${target} PRIVATE -Wnull-dereference)
        _add_cpp_flag(${target} PRIVATE -Wold-style-cast)
        _add_cpp_flag(${target} PRIVATE -Woverloaded-virtual)
        _add_cpp_flag(${target} PRIVATE -Wpacked)
        _add_cpp_flag(${target} PRIVATE -Wparentheses)
        _add_cpp_flag(${target} PRIVATE -Wredundant-decls)
        _add_cpp_flag(${target} PRIVATE -Wshadow)
        _add_cpp_flag(${target} PRIVATE -Wsign-conversion)
        _add_cpp_flag(${target} PRIVATE -Wsign-promo)
        _add_cpp_flag(${target} PRIVATE -Wstrict-null-sentinel)
        _add_cpp_flag(${target} PRIVATE -Wsuggest-attribute=const)
        _add_cpp_flag(${target} PRIVATE -Wsuggest-attribute=malloc)
        _add_cpp_flag(${target} PRIVATE -Wsuggest-attribute=noreturn)
        _add_cpp_flag(${target} PRIVATE -Wsuggest-attribute=pure)
        _add_cpp_flag(${target} PRIVATE -Wsuggest-final-methods)
        _add_cpp_flag(${target} PRIVATE -Wsuggest-final-types)
        _add_cpp_flag(${target} PRIVATE -Wsuggest-override)
        _add_cpp_flag(${target} PRIVATE -Wswitch-enum)
        _add_cpp_flag(${target} PRIVATE -Wuninitialized)
        _add_cpp_flag(${target} PRIVATE -Wundef)
        _add_cpp_flag(${target} PRIVATE -Wunsafe-loop-optimizations)
        _add_cpp_flag(${target} PRIVATE -Wunused)
        _add_cpp_flag(${target} PRIVATE -Wunused-macros)
        _add_cpp_flag(${target} PRIVATE -Wuseless-cast)
        _add_cpp_flag(${target} PRIVATE -Wvla)
        _add_cpp_flag(${target} PRIVATE -Wwrite-strings)
        _add_cpp_flag(${target} PRIVATE -Wzero-as-null-pointer-constant)

    elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
        _add_cpp_flag(${target} PRIVATE /W3)
    else()
        message(WARNING "Unknown compiler '${CMAKE_CXX_COMPILER_ID}', no warnings set")
    endif()
endfunction()


function(enable_warnings_for target)
    # This should be more intelligent and query the SOURCES property of the target
    # Then query files looking for their LANGUAGE
    enable_c_warnings_for(target)
    enable_cpp_warnings_for(target)
endfunction()

function(colorize_output)
    # In some situations Ninja may not detect it can output using ANSI colors
    if (CMAKE_GENERATOR STREQUAL "Ninja")
        if("${CMAKE_CXX_COMPILER_ID}}" MATCHES "Clang")
            add_compile_options(-fcolor-diagnostics)
        elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
            add_compile_options(-fdiagnostics-color)
        endif()
    endif()
endfunction()

function(link_math_library target)
    include(CheckLibraryExists)
    check_library_exists(m pow "" LIBM)
    if(LIBM)
        target_link_libraries(${target} PUBLIC m)
    endif()
endfunction()
