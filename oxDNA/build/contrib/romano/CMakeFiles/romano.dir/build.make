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

# Utility rule file for romano.

# Include any custom commands dependencies for this target.
include contrib/romano/CMakeFiles/romano.dir/compiler_depend.make

# Include the progress variables for this target.
include contrib/romano/CMakeFiles/romano.dir/progress.make

contrib/romano/CMakeFiles/romano: ../contrib/romano/HardIcoInteraction.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/PLCluster.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/PatchyShapeParticle.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/PatchyShapeInteraction.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/MCMovePatchyShape.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/ChiralRodInteraction.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/NematicS.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/Swim.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/ChiralRodExplicit.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/Reappear.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/CutVolume.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/Grow.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/Exhaust.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/FakePressure.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/FreeVolume.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/Depletion.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/NDepletion.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/DepletionVolume.dylib
contrib/romano/CMakeFiles/romano: ../contrib/romano/AVBDepletion.dylib

romano: contrib/romano/CMakeFiles/romano
romano: contrib/romano/CMakeFiles/romano.dir/build.make
.PHONY : romano

# Rule to build all files generated by this target.
contrib/romano/CMakeFiles/romano.dir/build: romano
.PHONY : contrib/romano/CMakeFiles/romano.dir/build

contrib/romano/CMakeFiles/romano.dir/clean:
	cd /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/romano && $(CMAKE_COMMAND) -P CMakeFiles/romano.dir/cmake_clean.cmake
.PHONY : contrib/romano/CMakeFiles/romano.dir/clean

contrib/romano/CMakeFiles/romano.dir/depend:
	cd /Users/takepy/takeoxdna/oxDNA_python2/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/takepy/takeoxdna/oxDNA_python2 /Users/takepy/takeoxdna/oxDNA_python2/contrib/romano /Users/takepy/takeoxdna/oxDNA_python2/build /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/romano /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/romano/CMakeFiles/romano.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : contrib/romano/CMakeFiles/romano.dir/depend

