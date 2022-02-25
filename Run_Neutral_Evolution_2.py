import sys
networkname = sys.argv[1].strip()
startgen = int(sys.argv[2].strip())

from mpi4py import MPI

comm = MPI.COMM_WORLD
world_rank = comm.Get_rank()

from time import time
from random import seed
seed(int(time()) + world_rank)

from Evolution_Methods import *

numgen = 250
popsize = 500
chosenfrac = 1.0
mutprob = 0.05

Evolution_Simulation_F_Based_Selection(networkname, world_rank, startgen, numgen, popsize, chosenfrac, mutprob)
