#!/bin/bash

prefix=$1
inputDir=$2
outputDir=$3
temperature=$4

mkdir -p $outputDir

echo Compute running time for prefix \'$prefix\' `complexes -T $temperature -material dna -pairs -mfe -degenerate -timeonly $inputDir/$prefix 2>&1 | grep estimate`

echo Running complexes for prefix \'$prefix\'
complexes -T $temperature -material dna -pairs -mfe -degenerate $inputDir/$prefix > $outputDir/$prefix-complexes.out

echo Running concentrations for prefix \'$prefix\'
concentrations -pairs $inputDir/$prefix > $outputDir/$prefix-concentrations.out

#echo Running distributions for prefix '$prefix'
#distributions -writestates $prefix > $outputDir/$prefix-distributions.out

mv $inputDir/$prefix.ocx* $outputDir/
mv $inputDir/$prefix.eq $outputDir/
mv $inputDir/$prefix.fpairs $outputDir/
#mv $inputDir/$prefix.dist $outputDir/
#mv $inputDir/$prefix.states $outputDir/

# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
