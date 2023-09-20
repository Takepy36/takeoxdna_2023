#!/bin/bash

docker run -it --rm --name takecontainer_into_bash -v /clusterhome/atakeguchi/kakenhievolvedna2:/home/user/kakenhievolvedna2 -v /clusterhome/atakeguchi/oxDNA_python2:/home/user/oxDNA takeoxdna_into_bash /bin/bash
