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

# Utility rule file for test_run.

# Include any custom commands dependencies for this target.
include CMakeFiles/test_run.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/test_run.dir/progress.make

CMakeFiles/test_run:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/Users/takepy/takeoxdna/oxDNA_python2/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Running build integration tests"
	cd /Users/takepy/takeoxdna/oxDNA_python2/TEST_LR && /Users/takepy/takeoxdna/oxDNA_python2/TEST_LR/TestSuite.py test_folder_list.txt /Users/takepy/takeoxdna/oxDNA_python2/build/bin/oxDNA run
	cd /Users/takepy/takeoxdna/oxDNA_python2/TEST_LR && /Users/takepy/takeoxdna/oxDNA_python2/TEST_LR/TestSuite.py test_folder_list.txt /Users/takepy/takeoxdna/oxDNA_python2/build/bin/DNAnalysis analysis

test_run: CMakeFiles/test_run
test_run: CMakeFiles/test_run.dir/build.make
.PHONY : test_run

# Rule to build all files generated by this target.
CMakeFiles/test_run.dir/build: test_run
.PHONY : CMakeFiles/test_run.dir/build

CMakeFiles/test_run.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/test_run.dir/cmake_clean.cmake
.PHONY : CMakeFiles/test_run.dir/clean

CMakeFiles/test_run.dir/depend:
	cd /Users/takepy/takeoxdna/oxDNA_python2/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/takepy/takeoxdna/oxDNA_python2 /Users/takepy/takeoxdna/oxDNA_python2 /Users/takepy/takeoxdna/oxDNA_python2/build /Users/takepy/takeoxdna/oxDNA_python2/build /Users/takepy/takeoxdna/oxDNA_python2/build/CMakeFiles/test_run.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/test_run.dir/depend

