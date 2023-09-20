#!/bin/bash

# Launch all experiment


configurationDir=conf/
logsDir=logs/

mkdir -p $configurationDir
mkdir -p $logsDir

function runExpe {
    local conf
    conf=$1
    shift;
    #nice -n 19 ./illuminate.py -c $configurationDir/$conf.yaml > $logsDir/$conf.log 2>&1 # & disown

#    ./runDockerExpe.sh $configurationDir/$conf.yaml normal localhost:5000/kakenhievolvedna | tee $logsDir/$conf/`hostname`.log
    ./scripts/illuminate.py -c $configurationDir/$conf.yaml -p multithreading | tee $logsDir/$conf_`hostname`.log
    sleep 2
}

# Sparse Random search
runExpe peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryRandom-300000x40-1x2-7
runExpe peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryRandom-300000x40-1x2-7
runExpe peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryRandom-300000x40-1x2-7
runExpe peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryRandom-300000x40-1x2-7

# L1
runExpe peppercorn30x400x2000-L1-largestStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64
runExpe peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64
runExpe peppercorn30x400x2000-L1-entropyComplexSize0.0x4.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64
runExpe peppercorn30x400x2000-L1-skewComplexSize0.0x10.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64
runExpe peppercorn30x400x2000-L1-mostCommonSize0x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64
runExpe peppercorn30x400x2000-L1-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64
runExpe peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10nbBindReactions0.0x5.0-log10nbBranchReactions0.0x5.0-Grid3x50x50--Greycode-65536x64

# L2
runExpe peppercorn30x400x2000-L2-largestStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7
runExpe peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7
runExpe peppercorn30x400x2000-L2-entropyComplexSize0.0x4.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7
runExpe peppercorn30x400x2000-L2-skewComplexSize0.0x10.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7
runExpe peppercorn30x400x2000-L2-mostCommonSize0x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7
runExpe peppercorn30x400x2000-L2-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7
runExpe peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10nbBindReactions0.0x5.0-log10nbBranchReactions0.0x5.0-Grid3x50x50--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7

# L3
runExpe peppercorn30x400x2000-L3-largestStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7
runExpe peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7
runExpe peppercorn30x400x2000-L3-entropyComplexSize0.0x4.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7
runExpe peppercorn30x400x2000-L3-skewComplexSize0.0x10.0-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7
runExpe peppercorn30x400x2000-L3-mostCommonSize0x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7
runExpe peppercorn30x400x2000-L3-entropyReactionTypes0x2-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7
runExpe peppercorn30x400x2000-L3-meanStruct1x30-nbActive2x7-log10nbBindReactions0.0x5.0-log10nbBranchReactions0.0x5.0-Grid3x50x50--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7


# A-L (random)
runExpe seqA-random100000-0.80
runExpe seqB-random100000-0.80
runExpe seqC-random100000-0.80
runExpe seqD-random100000-0.80
runExpe seqE-random100000-0.50
runExpe seqF-random100000-0.50
runExpe seqG-random100000-0.50
runExpe seqH-random100000-0.50
runExpe seqI-random100000-0.85
runExpe seqJ-random100000-0.85
runExpe seqK-random100000-0.85
runExpe seqL-random100000-0.85

# A-L (GA)
runExpe seqA-GA100000-0.80
runExpe seqB-GA100000-0.80
runExpe seqC-GA100000-0.80
runExpe seqD-GA100000-0.80
runExpe seqE-GA100000-0.50
runExpe seqF-GA100000-0.50
runExpe seqG-GA100000-0.50
runExpe seqH-GA100000-0.50
runExpe seqI-GA100000-0.85
runExpe seqJ-GA100000-0.85
runExpe seqK-GA100000-0.85
runExpe seqL-GA100000-0.85



# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
