#!/bin/bash
#use in takeoxdna

ct="$(date +'%Y:%m:%d-%H:%M:%S')"
# Commit comment


git add .

git commit -m $ct

git push origin master