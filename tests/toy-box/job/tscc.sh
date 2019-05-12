#!/bin/bash
# usage: qsub job/tscc.sh
#PBS -N toy-box
#PBS -q condo
#PBS -l nodes=2:ppn=16
#PBS -l walltime=8:00:00
#PBS -j oe
#PBS -o gizmo.log
#PBS -d .
set -e
spack env activate gizmo
module list
set -x

export MPIRUN="mpirun -npernode 16"
if [[ -d output/restartfiles ]]; then
    GIZMO_RUN_MODE=1
else
    GIZMO_RUN_MODE=
fi
export GIZMO_RUN_MODE

module list
pwd
date
make run-gizmo
date
