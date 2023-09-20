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

# Utility rule file for rovigatti.

# Include any custom commands dependencies for this target.
include contrib/rovigatti/CMakeFiles/rovigatti.dir/compiler_depend.make

# Include the progress variables for this target.
include contrib/rovigatti/CMakeFiles/rovigatti.dir/progress.make

contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/MGAssemblyConf.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/PolymerInteraction.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/DensityPressureProfile.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/PolydisperseLTInteraction.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/ConstructwisePressure.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/MicrogelElasticity.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/MGAnalysis.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/AOInteraction.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/RadialDensityProfile.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/MGInteraction.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/GenericGrByInsertion.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/YasutakaAnalysis.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/VoidPercolation.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/Remoteness.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/CPAnalysis.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/Widom.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/LevyDelta.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/LevyInteraction.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/CPMixtureInteraction.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/StarrInteraction.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/NathanInteraction.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/mWInteraction.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/ManfredoInteraction.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/GraftedInteraction.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/FSInteraction.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/TSPAnalysis.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/StarrConf.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/SPBAnalysis.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/PatchyToMgl.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/Diblock.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/ConstructwiseBonds.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/DiblockComs.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/EmptyVolume.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/FSConf.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/GrByInsertion.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/Gyradius.dylib
contrib/rovigatti/CMakeFiles/rovigatti: ../contrib/rovigatti/PatchyToMgl.dylib

rovigatti: contrib/rovigatti/CMakeFiles/rovigatti
rovigatti: contrib/rovigatti/CMakeFiles/rovigatti.dir/build.make
.PHONY : rovigatti

# Rule to build all files generated by this target.
contrib/rovigatti/CMakeFiles/rovigatti.dir/build: rovigatti
.PHONY : contrib/rovigatti/CMakeFiles/rovigatti.dir/build

contrib/rovigatti/CMakeFiles/rovigatti.dir/clean:
	cd /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti && $(CMAKE_COMMAND) -P CMakeFiles/rovigatti.dir/cmake_clean.cmake
.PHONY : contrib/rovigatti/CMakeFiles/rovigatti.dir/clean

contrib/rovigatti/CMakeFiles/rovigatti.dir/depend:
	cd /Users/takepy/takeoxdna/oxDNA_python2/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/takepy/takeoxdna/oxDNA_python2 /Users/takepy/takeoxdna/oxDNA_python2/contrib/rovigatti /Users/takepy/takeoxdna/oxDNA_python2/build /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti /Users/takepy/takeoxdna/oxDNA_python2/build/contrib/rovigatti/CMakeFiles/rovigatti.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : contrib/rovigatti/CMakeFiles/rovigatti.dir/depend

