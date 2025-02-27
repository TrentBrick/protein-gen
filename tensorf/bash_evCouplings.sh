#!/bin/bash
#SBATCH -c 4                               # Request one core
#SBATCH -N 1                               # Request one node (if you request m$
                                           # -N 1 means all cores will be on th$
#SBATCH -t 2-11:59                         # Runtime in D-HH:MM format
#SBATCH -p gpu                           # Partition to run in
#SBATCH --gres=gpu:1
#SBATCH --mem=30G                          # Memory total in MB (for all cores)
#SBATCH -o slurm_files/slurm-%j.out                 # File to which STDOUT + ST$
hostname
pwd
module load gcc/6.2.0 cuda/9.0
srun stdbuf -oL -eL ~/anaconda3/bin/python run.py evCouplings.py NVP_GPU_Train \
 --epochsML 1000 --epochsKL 2000 --batchsize_KL 256 --batchsize_ML 64 --ML_weight 1.0 \
 --lr 0.000001  --model_architecture RRRRRRRRRRR --save_partway_inter 0.1
