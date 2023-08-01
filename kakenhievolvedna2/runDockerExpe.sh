#!/bin/bash

configFile=${1:-}#conf file is here
executionMode=${2:-"normal"}
memoryLimit=60G
#resultsPath=$(pwd)/results
resultsPathInContainer=/home/user/results
finalresultsPath=$(pwd)/results
finalresultsPathInContainer=/home/user/finalresults
imageName=${3:-"localhost:5000/kakenhievolvedna"} #${3:-"kakenhievolvedna"} #localhost:5000/kakenhievolvedna
uid=$(id -u)
confPath=$(pwd)/conf
confPathInContainer=/home/user/kakenhievolvedna/conf

if [ ! -d $finalresultsPath ]; then
    mkdir -p $finalresultsPath
    cp $confPath/$configFile $finalresultsPath
    #result dir is created
fi

inDockerGroup=`id -Gn | grep docker`
if [ -z "$inDockerGroup" ]; then
    sudoCMD="sudo"
else
    sudoCMD=""
fi
dockerCMD="$sudoCMD docker"

if [ -d "$confPath" ]; then
    confVolParam="-v $confPath:$confPathInContainer"
else
    confVolParam=""
fi

if [ "$executionMode" = "normal" ]; then
    exec $dockerCMD run -i -m $memoryLimit --rm --mount type=tmpfs,tmpfs-size=8589934592,target=$resultsPathInContainer --mount type=bind,source=$finalresultsPath,target=$finalresultsPathInContainer $confVolParam $imageName  "$uid" "normal" "-c $configFile -p multithreading"
    #exec $dockerCMD run -i -m $memoryLimit --rm -v $resultsPath:$resultsPathInContainer $confVolParam $imageName  "$uid" "normal" "-c $configFile"
elif [ "$executionMode" = "cluster" ]; then
    # Create host file
    hostsNames=${4:-"shoal1,shoal2,shoal3,shoal4,shoal5,shoal6,shoal7,shoal8"}
    hostsFilename=$finalresultsPath/hosts
    declare -a hosts
    IFS="," read -r -a hosts <<< "$hostsNames"
    echo -n > $hostsFilename
    for h in "${hosts[@]}"; do
        echo "kakenhievolvedna-$h 8" >> $hostsFilename # Only one thread per host, to launch daccad
    done

    # Create network
    $dockerCMD network create --driver=overlay --attachable net-kakenhievolvedna
    sleep 1

    # Launch a client on each node
    for h in "${hosts[@]}"; do
        name=kakenhievolvedna-$h
        rm $finalresultsPath/stop-$h
        ssh $h "$dockerCMD run -di --name $name --network net-kakenhievolvedna -m $memoryLimit --rm --mount type=tmpfs,tmpfs-size=8589934592,target=$resultsPathInContainer --mount type=bind,source=$finalresultsPath,target=$finalresultsPathInContainer $confVolParam  $imageName $uid client $resultsPathInContainer/stop-$h"
    done
    sleep 1

    # Launch a server node
    $dockerCMD run -i --name kakenhievolvedna-main --network net-kakenhievolvedna -m $memoryLimit --rm --mount type=tmpfs,tmpfs-size=8589934592,target=$resultsPathInContainer --mount type=bind,source=$finalresultsPath,target=$finalresultsPathInContainer $confVolParam  $imageName "$uid" "server" $resultsPathInContainer/hosts "-c $configFile -p scoop"

    # Quit all client nodes
    for h in "${hosts[@]}"; do
        echo -n > $finalresultsPath/stop-$h
    done

    # Remove network
    $dockerCMD network rm net-kakenhievolvedna
fi

# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
