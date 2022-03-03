def Get_Randomized_Network_Properties(filename, RACIPE_Folder, world_rank):
	outputfile = RACIPE_Folder + '/network_' + str(world_rank) + '.topo'
	Generate_Random_Networks(filename, outputfile)
	N = Read_Network(outputfile)
	F_Score = Get_Frustration_Score(N, 50)
	Path(RACIPE_Folder + '/RUN_' + str(world_rank)).mkdir()
	RACIPE_Folder0 = RACIPE_Folder + '/RUN_' + str(world_rank)
	copy('../../code/RACIPE', RACIPE_Folder0)
	copy(outputfile, RACIPE_Folder0)
	RACIPE_Output = subprocess.run(['./RACIPE', 'network_' + str(world_rank) + '.topo', '-num_paras', '100'], cwd = RACIPE_Folder0, capture_output = True, text = True)
	with open(RACIPE_Folder0 + '/slurm.out', 'w') as f:
		f.write(RACIPE_Output.stdout)
	Process_RACIPE_Output(RACIPE_Folder0 + '/network_' + str(world_rank))
	PC_Score = PCA_On_RACIPE(RACIPE_Folder0, len(N.nodenames))

	return (F_Score, PC_Score)

from shutil import copy
import subprocess


from pathlib import Path

import sys
index = int(sys.argv[1])

from mpi4py import MPI

comm = MPI.COMM_WORLD
world_rank = comm.Get_rank()

from time import time, sleep
from random import seed
seed(int(time()) + world_rank)

from Util_Methods import *
from Boolean_Dynamics_Methods import *
from Evolution_PCA_Methods import *

if world_rank == 0:
	Path('./randnets/RUN_' + str(index)).mkdir()
	while True:
		flag = 0
		for i in range(1, 16):
			if not Path('randnets/RUN_' + str(index) + '/scores_' + str(i) + '.log').is_file():
				flag = 1
		print(flag)
		if flag == 1:
			sleep(2)
		else:
			with open('randnets/score_' + str(index) + '.log', 'w') as f:
				for i in range(1, 16):
					with open('randnets/RUN_' + str(index) + '/scores_' + str(i) + '.log', 'r') as g:
						for line in g:
							f.write(line.strip() + '\n')
			break
else:
	while True:
		if Path('./randnets/RUN_' + str(index)).is_dir():
			break
		else:
			sleep(2)
	F, P = Get_Randomized_Network_Properties('updatednetworks/RUN_0/network_' + str(index) + '.topo', 'randnets/RUN_' + str(index), world_rank)
	with open('randnets/RUN_' + str(index) + '/scores_' + str(world_rank) + '.log', 'w') as f:
		f.write(str(F) + '\t' + str(P) + '\n')
