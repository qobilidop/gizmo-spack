#!/bin/bash
# usage: sbatch job/bridges.sh
# https://www.psc.edu/bridges/user-guide/running-jobs#rm-summary
#SBATCH -J toy-box
#SBATCH -p RM-small
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH -t 8:00:00
#SBATCH -o gizmo.log
#SBATCH -D .
set -e
spack env activate gizmo
module list
set -x

# https://www.psc.edu/bridgwes/user-guide/sample-batch-scripts#mpi
export I_MPI_JOB_RESPECT_PROCESS_PLACEMENT=0
export MPIRUN="mpirun -n $SLURM_NTASKS -ppn $SLURM_NTASKS_PER_NODE"
if [[ -d output/restartfiles ]]; then
    GIZMO_RUN_MODE=1
else
    GIZMO_RUN_MODE=
fi
export GIZMO_RUN_MODE

pwd
date
make run-gizmo
date
