# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.21

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
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.21.4/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.21.4/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/takepy/takeoxdna/oxDNA_python2

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/takepy/takeoxdna/oxDNA_python2/build

# Include any dependencies generated for this target.
include contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/compiler_depend.make

# Include the progress variables for this target.
include contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/progress.make

# Include the compile flags for this target's objects.
include contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/flags.make

contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.o: contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/flags.make
contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.o: ../contrib/rovigatti/src/Observables/ConstructwisePressure.cpp
contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.o: contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/takepy/takeoxdna/oxDNA_python2/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.o"
	cd /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.o -MF CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.o.d -o CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.o -c /Users/takepy/takeoxdna/oxDNA_python2/contrib/rovigatti/src/Observables/ConstructwisePressure.cpp

contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.i"
	cd /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/takepy/takeoxdna/oxDNA_python2/contrib/rovigatti/src/Observables/ConstructwisePressure.cpp > CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.i

contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.s"
	cd /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/takepy/takeoxdna/oxDNA_python2/contrib/rovigatti/src/Observables/ConstructwisePressure.cpp -o CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.s

# Object files for target ConstructwisePressure
ConstructwisePressure_OBJECTS = \
"CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.o"

# External object files for target ConstructwisePressure
ConstructwisePressure_EXTERNAL_OBJECTS =

../contrib/rovigatti/ConstructwisePressure.dylib: contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/src/Observables/ConstructwisePressure.cpp.o
../contrib/rovigatti/ConstructwisePressure.dylib: contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/build.make
../contrib/rovigatti/ConstructwisePressure.dylib: contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/takepy/takeoxdna/oxDNA_python2/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library ../../../contrib/rovigatti/ConstructwisePressure.dylib"
	cd /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/ConstructwisePressure.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/build: ../contrib/rovigatti/ConstructwisePressure.dylib
.PHONY : contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/build

contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/clean:
	cd /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti && $(CMAKE_COMMAND) -P CMakeFiles/ConstructwisePressure.dir/cmake_clean.cmake
.PHONY : contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/clean

contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/depend:
	cd /Users/takepy/takeoxdna/oxDNA_python2/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/takepy/takeoxdna/oxDNA_python2 /Users/takepy/takeoxdna/oxDNA_python2/contrib/rovigatti /Users/takepy/takeoxdna/oxDNA_python2/build /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : contrib/rovigatti/CMakeFiles/ConstructwisePressure.dir/depend
