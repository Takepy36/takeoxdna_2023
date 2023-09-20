
# Automated Exploration of DNA-based Structure Self-Assembly Networks

This is the source code of the article "Automated Exploration of DNA-based Structure Self-Assembly Networks" published in the Royal Society Open Science Journal.

### Abstract
Finding DNA sequences capable of folding into specific nanostructures is a hard problem, as it involves very large search spaces and complex non-linear dynamics. Typical methods to solve it aim to reduce the search space by minimizing unwanted interactions through restrictions on the design (e.g. staples in DNA origami or voxel-based designs in DNA Bricks).
Here, we present a novel methodology that aims to reduce this search space by identifying the relevant properties of a given assembly system to the emergence of various families of structures (e.g. simple structures, polymers, branched structures).
For a given set of DNA strands, our approach automatically finds Chemical Reaction Networks (\CRNs) that generate sets of structures exhibiting ranges of specific user-specified properties, such as length and type of structures or their frequency of occurrence.
For each set, we enumerate the possible DNA structures that can be generated through domain-level interactions, identify the most prevalent structures, find the best-performing sequence sets to the emergence of target structures, and assess \CRNs robustness to the removal of reaction pathways.
Our results suggest a connection between the characteristics of DNA strands and the distribution of generated structure families.

### To clone this repository

```bash
git clone https://bitbucket.org/leo-cazenille/kakenhievolvedna.git
```


## Installation

Note: we strongly recommend launching our scripts through Singularity or Docker (cf sections below for more details). However, if you still wish to launch these scripts directly on a normal system, here are installation instructions:

First, download NUPACK version 3.2.2, and put it in the root directory of the local clone of the "kakenhievolvedna" git repository. You can find it on [NUPACK official website](http://www.nupack.org/downloads).
Then you will need to install it on your computer:
```bash
tar xvf nupack3.2.2.tar.gz
cd nupack3.2.2
mkdir build && cd build
cmake .. && make -j 20
make install
```

All scripts need Python 3.6+. To install the required libraries:
**Be aware that, for result reproducibility, exact versions are specified. It is recommended to use the following command with a virtualenv.**
```bash
pip3 install -r requirements.txt
```



## Usage

### Quickstart
After all dependencies are installed (including peppercorn and NUPACK), you should be able to launch the Python scripts of this repository.

Each experiment/simulation is described in a configuration file in the "conf/" directory. This includes the domain-level and sequence-level optimization and analyses.
To launch an experiment given a configuration file, you can use the following command:
```bash
./scripts/illuminate.py -c conf/peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7.yaml -p multithreading
```

To launch all experiments used in the RSOS paper, you can use the following command:
```bash
./scripts/runAllExpes.sh
```
Then, the following command can be used to generate all analyses/plots:
```bash
./scripts/mkAllPlots.sh
```



### With Singularity

Use the following command to build a Singularity image:
```bash
sudo singularity build kakenhievolvedna.sif Singularity.def
```
Note that the current directory should be the main directory of the repository, and that the "nupack3.2.2.tar.gz" should exist in this directory (as detailed in the "Installation" section).

You can then launch the "illuminate.py" script, from the Singularity container (cf the "Quickstart" section above for a list of command parameters):
```bash
singularity run --app illuminate kakenhievolvedna.sif -c conf/peppercorn30x400x2000-L2-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--SparseBinaryGA3-300000x40-0.5x0.5x1x2-7.yaml -p multithreading
```

To launch all experiments used in the RSOS paper, you can use the following command:
```bash
singularity run --app runAllExpes kakenhievolvedna.sif
```
Then, the following command can be used to generate all analyses/plots:
```bash
singularity run --app mkAllPlots kakenhievolvedna.sif
```


### With Docker

First, build the docker image (here named "kakenhievolvedna:latest"):
```bash
docker build --no-cache -t kakenhievolvedna:latest .
```

Then, you can use the script "runDockerExpe.sh" to launch an experiment corresponding to a given yaml configuration file:
```bash
./runDockerExpe.sh conf/peppercorn30x400x2000-L1-meanStruct1x30-nbActive2x7-log10ReactionCount1.0x5.0-length1x550-Grid3x50x55--Greycode-65536x64.yaml normal kakenhievolvedna:latest
```
Results are copied to the "results/" directory.




## Authors
 * Leo Cazenille: Main author and maintainer.
    * [ResearchGate](https://www.researchgate.net/profile/Leo_Cazenille) 
    * email: leo "dot" cazenille "at" gmail "dot" com
 * Nathanael Aubert-Kato: Main author and maintainer.
    * [ResearchGate](https://www.researchgate.net/profile/Nathanael-Aubert-Kato)
    * email: naubertkato "at" is "dot" ocha "dot" ac "dot" jp


## Data and Supplementary Information
https://drive.google.com/drive/folders/1clCTjxu3e9MfNujxZRn4QmEO9ov-aBe8?usp=sharing


## Citing

```bibtex
@article{,
  title={Automated Exploration of DNA-based Structure Self-Assembly Networks},
  author={Cazenille, L and Baccouche, A and Aubert-Kato, N},
  journal={Royal Society open science},
  volume={?},
  number={?},
  pages={?},
  year={2021},
  publisher={The Royal Society Publishing}
}
```

