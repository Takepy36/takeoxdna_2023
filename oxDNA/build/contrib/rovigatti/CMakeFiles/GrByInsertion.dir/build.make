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
include contrib/rovigatti/CMakeFiles/GrByInsertion.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include contrib/rovigatti/CMakeFiles/GrByInsertion.dir/compiler_depend.make

# Include the progress variables for this target.
include contrib/rovigatti/CMakeFiles/GrByInsertion.dir/progress.make

# Include the compile flags for this target's objects.
include contrib/rovigatti/CMakeFiles/GrByInsertion.dir/flags.make

contrib/rovigatti/CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.o: contrib/rovigatti/CMakeFiles/GrByInsertion.dir/flags.make
contrib/rovigatti/CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.o: ../contrib/rovigatti/src/Observables/GrByInsertion.cpp
contrib/rovigatti/CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.o: contrib/rovigatti/CMakeFiles/GrByInsertion.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/takepy/takeoxdna/oxDNA_python2/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object contrib/rovigatti/CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.o"
	cd /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT contrib/rovigatti/CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.o -MF CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.o.d -o CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.o -c /Users/takepy/takeoxdna/oxDNA_python2/contrib/rovigatti/src/Observables/GrByInsertion.cpp

contrib/rovigatti/CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.i"
	cd /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/takepy/takeoxdna/oxDNA_python2/contrib/rovigatti/src/Observables/GrByInsertion.cpp > CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.i

contrib/rovigatti/CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.s"
	cd /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti && /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/takepy/takeoxdna/oxDNA_python2/contrib/rovigatti/src/Observables/GrByInsertion.cpp -o CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.s

# Object files for target GrByInsertion
GrByInsertion_OBJECTS = \
"CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.o"

# External object files for target GrByInsertion
GrByInsertion_EXTERNAL_OBJECTS =

../contrib/rovigatti/GrByInsertion.dylib: contrib/rovigatti/CMakeFiles/GrByInsertion.dir/src/Observables/GrByInsertion.cpp.o
../contrib/rovigatti/GrByInsertion.dylib: contrib/rovigatti/CMakeFiles/GrByInsertion.dir/build.make
../contrib/rovigatti/GrByInsertion.dylib: contrib/rovigatti/CMakeFiles/GrByInsertion.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/takepy/takeoxdna/oxDNA_python2/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library ../../../contrib/rovigatti/GrByInsertion.dylib"
	cd /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/GrByInsertion.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
contrib/rovigatti/CMakeFiles/GrByInsertion.dir/build: ../contrib/rovigatti/GrByInsertion.dylib
.PHONY : contrib/rovigatti/CMakeFiles/GrByInsertion.dir/build

contrib/rovigatti/CMakeFiles/GrByInsertion.dir/clean:
	cd /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti && $(CMAKE_COMMAND) -P CMakeFiles/GrByInsertion.dir/cmake_clean.cmake
.PHONY : contrib/rovigatti/CMakeFiles/GrByInsertion.dir/clean

contrib/rovigatti/CMakeFiles/GrByInsertion.dir/depend:
	cd /Users/takepy/takeoxdna/oxDNA_python2/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/takepy/takeoxdna/oxDNA_python2 /Users/takepy/takeoxdna/oxDNA_python2/contrib/rovigatti /Users/takepy/takeoxdna/oxDNA_python2/build /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti/CMakeFiles/GrByInsertion.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : contrib/rovigatti/CMakeFiles/GrByInsertion.dir/depend

