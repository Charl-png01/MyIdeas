# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.25

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /Applications/CLion.app/Contents/bin/cmake/mac/bin/cmake

# The command to remove a file.
RM = /Applications/CLion.app/Contents/bin/cmake/mac/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/executable.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/executable.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/executable.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/executable.dir/flags.make

CMakeFiles/executable.dir/main.c.o: CMakeFiles/executable.dir/flags.make
CMakeFiles/executable.dir/main.c.o: /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/main.c
CMakeFiles/executable.dir/main.c.o: CMakeFiles/executable.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/executable.dir/main.c.o"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/executable.dir/main.c.o -MF CMakeFiles/executable.dir/main.c.o.d -o CMakeFiles/executable.dir/main.c.o -c /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/main.c

CMakeFiles/executable.dir/main.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/executable.dir/main.c.i"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/main.c > CMakeFiles/executable.dir/main.c.i

CMakeFiles/executable.dir/main.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/executable.dir/main.c.s"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/main.c -o CMakeFiles/executable.dir/main.c.s

CMakeFiles/executable.dir/substitution.c.o: CMakeFiles/executable.dir/flags.make
CMakeFiles/executable.dir/substitution.c.o: /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/substitution.c
CMakeFiles/executable.dir/substitution.c.o: CMakeFiles/executable.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/executable.dir/substitution.c.o"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/executable.dir/substitution.c.o -MF CMakeFiles/executable.dir/substitution.c.o.d -o CMakeFiles/executable.dir/substitution.c.o -c /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/substitution.c

CMakeFiles/executable.dir/substitution.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/executable.dir/substitution.c.i"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/substitution.c > CMakeFiles/executable.dir/substitution.c.i

CMakeFiles/executable.dir/substitution.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/executable.dir/substitution.c.s"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/substitution.c -o CMakeFiles/executable.dir/substitution.c.s

CMakeFiles/executable.dir/test_substitution.c.o: CMakeFiles/executable.dir/flags.make
CMakeFiles/executable.dir/test_substitution.c.o: /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/test_substitution.c
CMakeFiles/executable.dir/test_substitution.c.o: CMakeFiles/executable.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object CMakeFiles/executable.dir/test_substitution.c.o"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/executable.dir/test_substitution.c.o -MF CMakeFiles/executable.dir/test_substitution.c.o.d -o CMakeFiles/executable.dir/test_substitution.c.o -c /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/test_substitution.c

CMakeFiles/executable.dir/test_substitution.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/executable.dir/test_substitution.c.i"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/test_substitution.c > CMakeFiles/executable.dir/test_substitution.c.i

CMakeFiles/executable.dir/test_substitution.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/executable.dir/test_substitution.c.s"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/test_substitution.c -o CMakeFiles/executable.dir/test_substitution.c.s

CMakeFiles/executable.dir/percent.c.o: CMakeFiles/executable.dir/flags.make
CMakeFiles/executable.dir/percent.c.o: /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/percent.c
CMakeFiles/executable.dir/percent.c.o: CMakeFiles/executable.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building C object CMakeFiles/executable.dir/percent.c.o"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/executable.dir/percent.c.o -MF CMakeFiles/executable.dir/percent.c.o.d -o CMakeFiles/executable.dir/percent.c.o -c /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/percent.c

CMakeFiles/executable.dir/percent.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/executable.dir/percent.c.i"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/percent.c > CMakeFiles/executable.dir/percent.c.i

CMakeFiles/executable.dir/percent.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/executable.dir/percent.c.s"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/percent.c -o CMakeFiles/executable.dir/percent.c.s

CMakeFiles/executable.dir/test_percent.c.o: CMakeFiles/executable.dir/flags.make
CMakeFiles/executable.dir/test_percent.c.o: /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/test_percent.c
CMakeFiles/executable.dir/test_percent.c.o: CMakeFiles/executable.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building C object CMakeFiles/executable.dir/test_percent.c.o"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/executable.dir/test_percent.c.o -MF CMakeFiles/executable.dir/test_percent.c.o.d -o CMakeFiles/executable.dir/test_percent.c.o -c /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/test_percent.c

CMakeFiles/executable.dir/test_percent.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/executable.dir/test_percent.c.i"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/test_percent.c > CMakeFiles/executable.dir/test_percent.c.i

CMakeFiles/executable.dir/test_percent.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/executable.dir/test_percent.c.s"
	/Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/test_percent.c -o CMakeFiles/executable.dir/test_percent.c.s

# Object files for target executable
executable_OBJECTS = \
"CMakeFiles/executable.dir/main.c.o" \
"CMakeFiles/executable.dir/substitution.c.o" \
"CMakeFiles/executable.dir/test_substitution.c.o" \
"CMakeFiles/executable.dir/percent.c.o" \
"CMakeFiles/executable.dir/test_percent.c.o"

# External object files for target executable
executable_EXTERNAL_OBJECTS =

executable: CMakeFiles/executable.dir/main.c.o
executable: CMakeFiles/executable.dir/substitution.c.o
executable: CMakeFiles/executable.dir/test_substitution.c.o
executable: CMakeFiles/executable.dir/percent.c.o
executable: CMakeFiles/executable.dir/test_percent.c.o
executable: CMakeFiles/executable.dir/build.make
executable: CMakeFiles/executable.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Linking C executable executable"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/executable.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/executable.dir/build: executable
.PHONY : CMakeFiles/executable.dir/build

CMakeFiles/executable.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/executable.dir/cmake_clean.cmake
.PHONY : CMakeFiles/executable.dir/clean

CMakeFiles/executable.dir/depend:
	cd /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/cmake-build-debug /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/cmake-build-debug /Users/charleskokofi/Desktop/JobHub/MyIdeas/midterm/cmake-build-debug/CMakeFiles/executable.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/executable.dir/depend

