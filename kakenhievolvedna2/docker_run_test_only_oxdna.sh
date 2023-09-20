#!/bin/bash

nohup docker run --rm --name takecontainer_test_only_oxdna -v /clusterhome/atakeguchi/kakenhievolvedna2:/home/user/kakenhievolvedna2 -v /clusterhome/atakeguchi/oxDNA_python2:/home/user/oxDNA takeimage_test_only_oxdna /bin/bash > test_loop_only_oxdna.log &
