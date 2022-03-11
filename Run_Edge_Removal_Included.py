from mpi4py import MPI

comm = MPI.COMM_WORLD
world_rank = comm.Get_rank()

from time import time
from random import seed
seed(int(time()) + world_rank)

import sys

from pathlib import Path
from shutil import copy
import subprocess

inputnetwork = sys.argv[1]

from Util_Methods import *
from Update_Network_Methods import *
from Boolean_Dynamics_Methods import *
from Evolution_PCA_Methods import *

Included = []
with open('Included.log', 'r') as f:
	for line in f:
		Included.append(line.strip())

updateindex = 0

Path('./updatednetworks/RUN_' + str(world_rank)).mkdir()
copy('../../networkfiles/' + inputnetwork + '.topo', 'updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex) + '.topo')
Path('./RACIPE_Output/RUN_' + str(world_rank)).mkdir()
Path('./sensitivities/RUN_' + str(world_rank)).mkdir()
Path('./steadystates/RUN_' + str(world_rank)).mkdir()

outputfile = open('outputfiles/' + inputnetwork + '_' + str(world_rank) + '.log', 'w')

while True:
	N = Read_Network('updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex) + '.topo')
	RACIPE_Folder = 'RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex)
	Path(RACIPE_Folder).mkdir()
	copy('../../code/RACIPE', RACIPE_Folder)
	copy('updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex) + '.topo', RACIPE_Folder)
	RACIPE_Output = subprocess.run(['./RACIPE', 'network_' + str(updateindex) + '.topo', '-num_paras', '100'], cwd = RACIPE_Folder, capture_output = True, text = True)
	with open(RACIPE_Folder + '/slurm.out', 'w') as f:
		f.write(RACIPE_Output.stdout)
	PC_Score = PCA_On_RACIPE(RACIPE_Folder, len(N.nodenames))
	Process_RACIPE_Output(RACIPE_Folder + '/network_' + str(updateindex))
	steadystates = Write_Steady_States(RACIPE_Folder, 'network_' + str(updateindex), 'steadystates/RUN_' + str(world_rank), 'network_' + str(updateindex) + '.log')

	F_Score = Get_Frustration_Score(Read_Network('updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex) + '.topo'), 50)

	outputfile.write(str(len(N.nodenames)) + ' ' + str(N.numedges) + ' ' + str(PC_Score) + ' ' + str(F_Score) + '\n')

	sensitivitycalc = subprocess.run(['../../code/Calculate_Sensitivities', 'network', str(world_rank), str(updateindex), '0'], capture_output = True, text = True)

	newnodecount, newedgecount, sig = Remove_Edges_With_Inclusions(0, inputnetwork, world_rank, updateindex, Included)

	print(str(newnodecount) + ' ' + str(newedgecount) + ' ' + str(sig))

	if newedgecount < 1 or newnodecount <= len(Included) or sig == -1:
		break

	updateindex += 1

outputfile.close()
