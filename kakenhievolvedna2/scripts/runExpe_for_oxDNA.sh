#!/bin/bash
configurationDir=../conf/
logsDir=../logs/
mkdir -p $configurationDirmkdir -p $logsDir


function runExpe {
local conf
conf=$1
shift;
../scripts/illuminate.py -c $configurationDir/$conf.yaml -p multithreading | tee $logsDir/$conf_`hostname`.log
sleep 2
}
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set0/0_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set1/1_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set2/2_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set3/3_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set4/4_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set5/5_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set6/6_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set7/7_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set8/8_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set9/9_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set10/10_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set11/11_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set12/12_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set13/13_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set14/14_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set15/15_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set16/16_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set17/17_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set18/18_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set19/19_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set20/20_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set21/21_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set22/22_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set23/23_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set24/24_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set25/25_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set26/26_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set27/27_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set28/28_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set29/29_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set30/30_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set31/31_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set32/32_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set33/33_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set34/34_peppercorn.pil
runExpe 2022-12-19/20230711_1109/loop0/untrusted_strands_set35/35_peppercorn.pil
