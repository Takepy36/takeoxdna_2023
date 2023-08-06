#!/bin/bash

nohup docker run --rm --name takecontainer_loop -v /clusterhome/atakeguchi/kakenhievolvedna2:/home/user/kakenhievolvedna2 -v /clusterhome/atakeguchi/oxDNA_python2:/home/user/oxDNA_python2 takeoxdna_test_loop /bin/bash &
