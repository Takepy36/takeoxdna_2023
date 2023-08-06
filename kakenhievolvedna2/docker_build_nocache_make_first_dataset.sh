#!/bin/bash

nohup docker build --no-cache -t takeoxdna_make_dataset -f Dockerfile_make_first_dataset . &
