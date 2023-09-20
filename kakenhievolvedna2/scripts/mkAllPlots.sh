#!/bin/bash

dataDir=results
plotsDir=figs/plots
plotScripts=./scripts

nupackDataDir=$dataDir/nupack-output-8

mkdir -p $dataDir
mkdir -p $plotsDir


declare -a pids


function plotMap {
    local configName outputFile dataFile onlyCBar
    configName=$1
    outputFile=$2
    onlyCBar=${3:-false}
    minFit=${4:-""}
    maxFit=${5:-""}
    shift; shift; shift; shift; shift;

    if [ -z "$minFit" ]; then
        mincmd=""
    else
        mincmd="--minFit $minFit"
    fi
    if [ -z "$maxFit" ]; then
        maxcmd=""
    else
        maxcmd="--maxFit $maxFit"
    fi

    echo Creating plots for config \'$configName\'
    #mkdir -p $plotsDir/$configName
    dataFile=$(ls $dataDir/$configName/final_*.p | head -n 1)
    if $onlyCBar; then
        $plotScripts/plotMaps.py -C -i $dataFile -o $plotsDir/$outputFile $mincmd $maxcmd &
    else
        $plotScripts/plotMaps.py -i $dataFile -o $plotsDir/$outputFile $mincmd $maxcmd &
    fi
    pids+=($!)

    if $onlyCBar; then
        true
    else
        $plotScripts/plotBigMaps.py -i $dataFile -o $plotsDir/bigmap-$outputFile &
        pids+=($!)
    fi
}


function plotMapNupack {
    local configName nupackFile outputFile dataFile onlyCBar
    configName=$1
    nupackFile=$2
    outputFile=$3
    onlyCBar=${4:-false}
    minFit=${5:-""}
    maxFit=${6:-""}
    nupackFile2=${7:-""}
    shift; shift; shift; shift; shift; shift; shift;

    if [ -z "$minFit" ]; then
        mincmd=""
    else
        mincmd="--minFit $minFit"
    fi
    if [ -z "$maxFit" ]; then
        maxcmd=""
    else
        maxcmd="--maxFit $maxFit"
    fi

    if [ -z "$nupackFile2" ]; then
        file2Param=""
    else
        file2Param="--inputFile2 $dataDir/$nupackFile2"
    fi

    echo Creating plots for config \'$configName\'
    #mkdir -p $plotsDir/$configName
    dataFile=$(ls $dataDir/$configName/final_*.p | head -n 1)
    if $onlyCBar; then
        $plotScripts/plotMapsNupack.py -C --referenceFile $dataFile -i $dataDir/$nupackFile $file2Param -o $plotsDir/$outputFile $mincmd $maxcmd &
    else
        $plotScripts/plotMapsNupack.py --referenceFile $dataFile -i $dataDir/$nupackFile $file2Param -o $plotsDir/$outputFile $mincmd $maxcmd &
    fi
    pids+=($!)
}



function plotNupackHist {
    local inputFile outputFile
    inputFile=$1
    outputFile=$2
    inset=${3:-false}
    shift; shift; shift;

    echo Creating histogram of nupack data \'$inputFile\'
    if $inset; then
        $plotScripts/nupackHistogramReader.py -i $inputFile -o $plotsDir/$outputFile --inset &
    else
        $plotScripts/nupackHistogramReader.py -i $inputFile -o $plotsDir/$outputFile &
    fi
    pids+=($!)
}

function plotPepperHist {
    local inputFile outputFile idx lib
    inputFile=$1
    outputFile=$2
    idx=$3
    lib=$4
    shift; shift; shift; shift;

    echo Creating histogram of peppercorn data \'$inputFile\'
    $plotScripts/plotInd.py -i $dataDir/$inputFile -o $plotsDir/$outputFile --library $lib --index $idx &
    pids+=($!)
}


function plotConvergence {
    local inputDir outputPrefix
    inputDir=$1
    outputPrefix=$2
    shift; shift;

    echo Creating convergence plots of directory \'$inputDir\'
    $plotScripts/plotConvergence.py -i $dataDir/$inputDir -o $plotsDir/$outputPrefix &
    pids+=($!)
}

function plotConvergenceSeq {
    local inputDirRandom inputDirGA outputPrefix
    inputDirRandom=$1
    inputDirGA=$2
    outputPrefix=$3
    shift; shift; shift;

    echo Creating convergence plots of directories \'$inputDirRandom\' and \'$inputDirGA\'
    $plotScripts/plotConvergenceSeq.py -r $dataDir/$inputDirRandom -g $dataDir/$inputDirGA -o $plotsDir/$outputPrefix &
    pids+=($!)
}


# Sparse Random search
plotMap peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryRandom-300000x40-1x2-7 SRS-peppercorn-L2-meanStruct.pdf
plotMap peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryRandom-300000x40-1x2-7 SRS-peppercorn-L2-entropyReactionTypes.pdf
plotMap peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryRandom-300000x40-1x2-7 SRS-peppercorn-L3-meanStruct.pdf
plotMap peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryRandom-300000x40-1x2-7 SRS-peppercorn-L3-entropyReactionTypes.pdf

# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done

plotConvergence peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryRandom-300000x40-1x2-7 SRS-peppercorn-L2-MSS
plotConvergence peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryRandom-300000x40-1x2-7 SRS-peppercorn-L2-ERT
plotConvergence peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryRandom-300000x40-1x2-7 SRS-peppercorn-L3-MSS
plotConvergence peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryRandom-300000x40-1x2-7 SRS-peppercorn-L3-ERT

# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done





./scripts/plotOptimSequences.py -c conf/optimSeq.yaml &
pids+=($!)


plotMap peppercorn30x400x2000-L1-largestStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-L1-largestStruct.pdf
plotMap peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-L1-meanStruct.pdf
plotMap peppercorn30x400x2000-L1-entropyComplexSize0.0x4.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-L1-entropyComplexSize.pdf
plotMap peppercorn30x400x2000-L1-skewComplexSize0.0x10.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-L1-skewComplexSize.pdf

# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done

plotMap peppercorn30x400x2000-L1-mostCommonSize0x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-L1-mostCommonSize.pdf
plotMap peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-L1-entropyReactionTypes.pdf false 0.0 1.65
plotMap peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10nbBindReactions0.0x5.0-log10nbBranchReactions0.0x5.0-Grid3x50x50--Greycode-65536x64 peppercorn-L1-meanStructWRTreactionTypes.pdf

# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done

plotMap peppercorn30x400x2000-L3-largestStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L3-largestStruct.pdf
plotMap peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L3-meanStruct.pdf
plotMap peppercorn30x400x2000-L3-entropyComplexSize0.0x4.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L3-entropyComplexSize.pdf

# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done

plotMap peppercorn30x400x2000-L3-skewComplexSize0.0x10.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L3-skewComplexSize.pdf
plotMap peppercorn30x400x2000-L3-mostCommonSize0x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L3-mostCommonSize.pdf
plotMap peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L3-entropyReactionTypes.pdf false 0.0 1.65
plotMap peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10nbBindReactions0.0x5.0-log10nbBranchReactions0.0x5.0-Grid3x50x50--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L3-meanStructWRTreactionTypes.pdf


# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done

plotMap peppercorn30x400x2000-L2-largestStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L2-largestStruct.pdf
plotMap peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L2-meanStruct.pdf
plotMap peppercorn30x400x2000-L2-entropyComplexSize0.0x4.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L2-entropyComplexSize.pdf
plotMap peppercorn30x400x2000-L2-skewComplexSize0.0x10.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L2-skewComplexSize.pdf

# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done

plotMap peppercorn30x400x2000-L2-mostCommonSize0x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L2-mostCommonSize.pdf
plotMap peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L2-entropyReactionTypes.pdf
plotMap peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10nbBindReactions0.0x5.0-log10nbBranchReactions0.0x5.0-Grid3x50x50--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L2-meanStructWRTreactionTypes.pdf

# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done

plotMap peppercorn30x400x2000-L1-largestStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-cbar-largestStruct.pdf true
plotMap peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-cbar-meanStruct.pdf true
plotMap peppercorn30x400x2000-L1-entropyComplexSize0.0x4.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-cbar-entropyComplexSize.pdf true
plotMap peppercorn30x400x2000-L1-skewComplexSize0.0x10.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-cbar-skewComplexSize.pdf true

# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done

plotMap peppercorn30x400x2000-L1-mostCommonSize0x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-cbar-mostCommonSize.pdf true
plotMap peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-cbar-entropyReactionTypes.pdf true 0.0 1.65
plotMap peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10nbBindReactions0.0x5.0-log10nbBranchReactions0.0x5.0-Grid3x50x50--Greycode-65536x64 peppercorn-cbar-meanStructWRTreactionTypes.pdf true

# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done

plotNupackHist $nupackDataDir/L1-entropyReactionTypes-1-22-39.p     hist-L1-entropyReactionTypes-1-22-39.pdf # a
plotNupackHist $nupackDataDir/L1-entropyReactionTypes-1-24-20.p     hist-L1-entropyReactionTypes-1-24-20.pdf # b
plotNupackHist $nupackDataDir/L1-meanStruct-0-23-5.p                hist-L1-meanStruct-0-23-5.pdf # c
plotNupackHist $nupackDataDir/L1-meanStruct-2-13-3.p                hist-L1-meanStruct-2-13-3.pdf # d

plotNupackHist $nupackDataDir/L2-meanStruct-2-31-18.p               hist-L2-meanStruct-2-31-18.pdf # g
plotNupackHist $nupackDataDir/L2-meanStruct-1-36-12.p               hist-L2-meanStruct-1-36-12.pdf # h
plotNupackHist $nupackDataDir/L2-entropyReactionTypes-1-36-11.p     hist-L2-entropyReactionTypes-1-36-11.pdf # e
plotNupackHist $nupackDataDir/L2-entropyReactionTypes-0-21-5.p      hist-L2-entropyReactionTypes-0-21-5.pdf # f

plotNupackHist $nupackDataDir/L3-entropyReactionTypes-0-25-2.p      hist-L3-entropyReactionTypes-0-25-2.pdf # i
plotNupackHist $nupackDataDir/L3-entropyReactionTypes-1-28-33.p     hist-L3-entropyReactionTypes-1-28-33.pdf # j
plotNupackHist $nupackDataDir/L3-entropyReactionTypes-1-29-46.p     hist-L3-entropyReactionTypes-1-29-46.pdf # k
plotNupackHist $nupackDataDir/L3-meanStruct-1-30-35.p               hist-L3-meanStruct-1-30-35.pdf # l

# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done


plotPepperHist peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64/final_20191108042748.p pepperhist-L1-entropyReactionTypes-1-22-39.pdf "1,22,39" L1 # a
plotPepperHist peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64/final_20191108042748.p pepperhist-L1-entropyReactionTypes-1-24-20.pdf "1,24,20" L1 # b
plotPepperHist peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64/final_20190925070629.p pepperhist-L1-meanStruct-0-23-5.pdf "0,23,5" L1 # c
plotPepperHist peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64/final_20190925070629.p pepperhist-L1-meanStruct-2-13-3.pdf "2,13,3" L1 # d

plotPepperHist peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20190925071128.p pepperhist-L2-meanStruct-2-31-18.pdf "2,31,18" L2 # g
plotPepperHist peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20190925071128.p pepperhist-L2-meanStruct-1-36-12.pdf "1,36,12" L2 # h
plotPepperHist peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043128.p pepperhist-L2-entropyReactionTypes-1-36-11.pdf "1,36,11" L2 # e
plotPepperHist peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043128.p pepperhist-L2-entropyReactionTypes-0-21-5.pdf "0,21,5" L2 # f

plotPepperHist peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043324.p pepperhist-L3-entropyReactionTypes-0-25-2.pdf "0,25,2" L3 # i
plotPepperHist peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043324.p pepperhist-L3-entropyReactionTypes-1-28-33.pdf "1,28,33" L3 # j
plotPepperHist peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20191108043324.p pepperhist-L3-entropyReactionTypes-1-29-46.pdf "1,29,46" L3 # k
plotPepperHist peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7/final_20190926011251.p pepperhist-L3-meanStruct-1-30-35.pdf "1,30,35" L3 # l

# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done


plotMapNupack peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 nupack-all-5-L1/L1-meanStruct.p nupack-L1-meanStruct.pdf false 0.0 1.6
plotMapNupack peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 nupack-all-5-L1/L1-entropyReactionTypes.p nupack-L1-entropyReactionTypes.pdf false 0.0 1.6
plotMapNupack peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 nupack-all-5-L1/L1-meanStruct.p nupack-L1-combined.pdf false 0.0 1.6 nupack-all-5-L1/L1-entropyReactionTypes.p

plotMapNupack peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 nupack-all-5-L2/L2-meanStruct.p nupack-L2-meanStruct.pdf false 0.0 1.6
plotMapNupack peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 nupack-all-5-L2/L2-entropyReactionTypes.p nupack-L2-entropyReactionTypes.pdf false 0.0 1.6
plotMapNupack peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 nupack-all-5-L2/L2-meanStruct.p nupack-L2-combined.pdf false 0.0 1.6 nupack-all-5-L2/L2-entropyReactionTypes.p

plotMapNupack peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 nupack-all-5-L3/L3-meanStruct.p nupack-L3-meanStruct.pdf false 0.0 1.6
plotMapNupack peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 nupack-all-5-L3/L3-entropyReactionTypes.p nupack-L3-entropyReactionTypes.pdf false 0.0 1.6
plotMapNupack peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 nupack-all-5-L3/L3-meanStruct.p nupack-L3-combined.pdf false 0.0 1.6 nupack-all-5-L3/L3-entropyReactionTypes.p

plotMapNupack peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 nupack-all-5-L1/L1-meanStruct.p nupack-cbar-meanStruct.pdf true 0.0 1.6
plotMapNupack peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 nupack-all-5-L1/L1-entropyReactionTypes.p nupack-cbar-entropyReactionTypes.pdf true 0.0 1.6
plotMapNupack peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 nupack-all-5-L1/L1-meanStruct.p nupack-cbar-combined.pdf true 0.0 1.6 nupack-all-5-L1/L1-entropyReactionTypes.p


# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done

plotConvergence peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-L1-MSS
plotConvergence peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-L1-ERT
plotConvergence peppercorn30x400x2000-L1-largestStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-L1-LS
plotConvergence peppercorn30x400x2000-L1-entropyComplexSize0.0x4.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64 peppercorn-L1-ECS

plotConvergence peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L2-MSS
plotConvergence peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L2-ERT
plotConvergence peppercorn30x400x2000-L2-largestStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L2-LS
plotConvergence peppercorn30x400x2000-L2-entropyComplexSize0.0x4.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L2-ECS

plotConvergence peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L3-MSS
plotConvergence peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L3-ERT
plotConvergence peppercorn30x400x2000-L3-largestStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L3-LS
plotConvergence peppercorn30x400x2000-L3-entropyComplexSize0.0x4.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7 peppercorn-L3-ECS

# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done



plotConvergence seqA-GA100000-0.80          seqA-GA
plotConvergence seqA-random100000-0.80      seqA-random
plotConvergence seqB-GA100000-0.80          seqB-GA
plotConvergence seqB-random100000-0.80      seqB-random
plotConvergence seqC-GA100000-0.80          seqC-GA
plotConvergence seqC-random100000-0.80      seqC-random
plotConvergence seqD-GA100000-0.80          seqD-GA
plotConvergence seqD-random100000-0.80      seqD-random
plotConvergence seqE-GA100000-0.50          seqE-GA
plotConvergence seqE-random100000-0.50      seqE-random
plotConvergence seqF-GA100000-0.50          seqF-GA
plotConvergence seqF-random100000-0.50      seqF-random
plotConvergence seqG-GA100000-0.50          seqG-GA
plotConvergence seqG-random100000-0.50      seqG-random
plotConvergence seqH-GA100000-0.50          seqH-GA
plotConvergence seqH-random100000-0.50      seqH-random
plotConvergence seqI-GA100000-0.85          seqI-GA
plotConvergence seqI-random100000-0.85      seqI-random
plotConvergence seqJ-GA100000-0.85          seqJ-GA
plotConvergence seqJ-random100000-0.85      seqJ-random
plotConvergence seqK-GA100000-0.85          seqK-GA
plotConvergence seqK-random100000-0.85      seqK-random
plotConvergence seqL-GA100000-0.85          seqL-GA
plotConvergence seqL-random100000-0.85      seqL-random

plotConvergenceSeq seqA-random100000-0.80 seqA-GA100000-0.80 seqA
plotConvergenceSeq seqB-random100000-0.80 seqB-GA100000-0.80 seqB
plotConvergenceSeq seqC-random100000-0.80 seqC-GA100000-0.80 seqC
plotConvergenceSeq seqD-random100000-0.80 seqD-GA100000-0.80 seqD
plotConvergenceSeq seqE-random100000-0.50 seqE-GA100000-0.50 seqE
plotConvergenceSeq seqF-random100000-0.50 seqF-GA100000-0.50 seqF
plotConvergenceSeq seqG-random100000-0.50 seqG-GA100000-0.50 seqG
plotConvergenceSeq seqH-random100000-0.50 seqH-GA100000-0.50 seqH
plotConvergenceSeq seqI-random100000-0.85 seqI-GA100000-0.85 seqI
plotConvergenceSeq seqJ-random100000-0.85 seqJ-GA100000-0.85 seqJ
plotConvergenceSeq seqK-random100000-0.85 seqK-GA100000-0.85 seqK
plotConvergenceSeq seqL-random100000-0.85 seqL-GA100000-0.85 seqL


# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done


./scripts/Cleaned_up_CRN_read.py --computeMFE -c conf/conf_nupack8.yaml
./scripts/graphAnalyses.py -i results/crn -o results/graphAnalyses --cutoff 6 &
./scripts/graphAnalyses.py -i results/crn -o results/graphAnalyses50 --cutoff 6 --maxONodes 50 &
pids+=($!)


# Wait for plots to finish
for i in "${pids[@]}"; do
    wait $i
done


cd figs
pdflatex resultsPeppercorn.tex
pdflatex resultsPeppercorn2.tex
pdflatex resultsNupack.tex
pdflatex resultsExpe.tex
pdflatex results3DStructs.tex
pdflatex resultsCRNdegrees.tex
pdflatex resultsCRNL1.tex
pdflatex resultsCRNL2.tex
pdflatex resultsCRNL3.tex
pdflatex resultsCRNL123.tex
pdflatex resultsConvergenceDomainLevel.tex
pdflatex resultsConvergenceSeqLevel.tex
cd ..




# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
