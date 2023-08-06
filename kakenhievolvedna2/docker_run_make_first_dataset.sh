#!/bin/bash

nohup docker run --rm --name takeoxdna_make_dataset_container -v /clusterhome/atakeguchi/kakenhievolvedna2:/home/user/kakenhievolvedna2 -v /clusterhome/atakeguchi/oxDNA_python2:/home/user/oxDNA_python2 takeoxdna_make_dataset > takeoxdna_make_dataset_container_log.txt &