#!/bin/bash
export PATH=/usr/share/lmod/lmod/libexec:/opt/slurm/23.02.6/el9/bin:/opt/slurm/23.02.6/el9/sbin:$PATH
cd /home/bd67/scratch/dev/slurm_comunicator
PYTHONPATH=$(pwd)
echo $(date)
/software/Anaconda/build/bin/python3 -m slurm_comunicator.main
