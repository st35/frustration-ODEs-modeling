import sys
networkname = sys.argv[1].strip()
startgen = int(sys.argv[2].strip())

from mpi4py import MPI

comm = MPI.COMM_WORLD
world_rank = comm.Get_rank()

from time import time
from random import seed
seed(int(time()) + world_rank)

from Evolution_PCA_Methods import *

numgen = 250
popsize = 127
chosenfrac = 0.05
mutprob = 0.05

Evolution_Based_On_PCA(networkname, startgen, numgen, popsize, chosenfrac, mutprob, world_rank)
