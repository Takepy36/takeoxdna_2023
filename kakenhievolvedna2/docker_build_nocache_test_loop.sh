#!/bin/bash

nohup docker build --no-cache -t takeoxdna_test_loop -f Dockerfile_test_loop . &