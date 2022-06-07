import sys

from pathlib import Path
from shutil import copy
import subprocess

from mpi4py import MPI

comm = MPI.COMM_WORLD
world_rank = comm.Get_rank()

inputnetwork = sys.argv[1]

from Util_Methods import *
from Update_Network_Methods import *
from Boolean_Dynamics_Methods import *
from Evolution_PCA_Methods import *
from Linkage_Methods import *

from time import time
from random import seed
seed(int(time()) + world_rank)

exclusions = []
with open('Excluded.log', 'r') as f:
	for line in f:
		exclusions.append(line.strip())

updateindex = 0

Path('./updatednetworks/RUN_' + str(world_rank)).mkdir()
copy('../../networkfiles/' + inputnetwork + '.topo', 'updatednetworks/RUN_' + str(world_rank) + '/unnamednetwork_' + str(updateindex) + '.topo')
copy('../../networkfiles/' + inputnetwork + '.topo', 'updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex) + '.topo')
Path('./RACIPE_Output/RUN_' + str(world_rank)).mkdir()
Path('./steadystates/RUN_' + str(world_rank)).mkdir()
Path('./linkages/RUN_' + str(world_rank)).mkdir()

outputfile = open('outputfiles/output_' + str(world_rank) + '.log', 'w')

while True:
	N = Read_Network('updatednetworks/RUN_' + str(world_rank) + '/unnamednetwork_' + str(updateindex) + '.topo')
	N2 = Read_Network('updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex) + '.topo')
	flag = 0
	if len(N.nodenames) != len(N2.nodenames):
		flag = 1
	if N.numedges != N2.numedges:
		flag = 1
	if flag == 0:
		for i in range(len(N.nodenames)):
			for j in range(len(N.nodenames)):
				if N.T[i][j] != N2.T[i][j]:
					flag = 1
	if flag == 1:
		print('Bob Vance. Vance refrigeration.')
		break
	RACIPE_Folder = 'RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex)
	Path(RACIPE_Folder).mkdir()
	copy('../../code/RACIPE', RACIPE_Folder)
	copy('updatednetworks/RUN_' + str(world_rank) + '/unnamednetwork_' + str(updateindex) + '.topo', RACIPE_Folder)
	copy('updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex) + '.topo', RACIPE_Folder)
	RACIPE_Output = subprocess.run(['./RACIPE', 'unnamednetwork_' + str(updateindex) + '.topo', '-num_paras', '100'], cwd = RACIPE_Folder, capture_output = True, text = True)
	with open(RACIPE_Folder + '/slurm.out', 'w') as f:
		f.write(RACIPE_Output.stdout)
	Write_IDS_File(RACIPE_Folder + '/' + 'network_' + str(updateindex) + '.topo', RACIPE_Folder + '/' + 'network_' + str(updateindex) + '.ids')
	Process_RACIPE_Output(RACIPE_Folder + '/unnamednetwork_' + str(updateindex))
	steadystates = Write_Steady_States(RACIPE_Folder, 'unnamednetwork_' + str(updateindex), 'steadystates/RUN_' + str(world_rank), 'network_' + str(updateindex) + '.log')

	PC_Score = PCA_On_RACIPE(RACIPE_Folder, len(N.nodenames))
	F_Score = Get_Frustration_Score(Read_Network('updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex) + '.topo'), 50)

#	matlabrun = subprocess.run(['sh', 'Run_Matlab.sh', str(world_rank), str(updateindex)], capture_output = True, text = True, cwd = './')

	excludedids = []
	for i in range(len(N.nodenames)):
		if N2.nodenames[i] in exclusions:
			excludedids.append(i)

	mergesig = Get_Clusters(world_rank, updateindex, excludedids, len(N2.nodenames))

	if mergesig == -1:
		break

	outputfile.write(str(len(N.nodenames)) + '\t' + str(N.numedges) + '\t' + str(PC_Score) + '\t' + str(F_Score) + '\n')

	mergeid = 0
	if world_rank > 0:
		mergeid = 1

	newnodecount = Merge_Nodes(mergeid, inputnetwork, world_rank, updateindex)

	if newnodecount < 2:
		break

	updateindex += 1

outputfile.close()
