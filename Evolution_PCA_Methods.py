from Util_Methods import *
from Boolean_Dynamics_Methods import *

def PCA_On_RACIPE(RACIPE_Folder, numnodes):
	import os
	import numpy as np
	from sklearn.decomposition import PCA

	S = []
	count = 0
	for filename in os.listdir(RACIPE_Folder):
		if 'solution' not in filename:
			continue
		with open(RACIPE_Folder + '/' + filename, 'r') as f:
			for line in f:
				l = line.strip().split('\t')
				if (len(l) - 2) % numnodes != 0:
					print('Tell me why')
					return(-1.0)
				S.append([])
				for i in range(2, len(l)):
					S[count].append(float(l[i]))
					if len(S[count]) == numnodes and i != len(l) - 1:
						count += 1
						S.append([])
				count += 1
	flag = 0
	for i in range(len(S)):
		if len(S[i]) != numnodes:
			flag = 1
	if flag == 1:
		print('Marty and Cohle')
	states = np.array(S)
	pca = PCA(n_components = min(len(S), numnodes))
	pca.fit(states)

	return(pca.explained_variance_ratio_[0])

def Get_PCA_Score(P, RACIPE_Folder):
	S = []
	for i in range(len(P)):
		numnodes = len(P[i].nodenames)
		S.append(PCA_On_RACIPE(RACIPE_Folder + '/RUN_' + str(i), numnodes))

	return(S)


def Get_Next_Generation(scores, P, chosenfrac, mutprob):
	from random import randint, random
	from copy import deepcopy

	I = [i for i in range(len(scores))]
	SI = [x for _, x in sorted(zip(scores, I), reverse = True, key = lambda pair: pair[0])]
	scores = sorted(scores)
	chosen = int(chosenfrac*len(P))
	SP = [deepcopy(P[i]) for i in range(len(P))]
	P.clear()
	while len(P) < len(SP):
		P.append(deepcopy(SP[SI[randint(0, chosen - 1)]]))
	for i in range(len(P)):
		if random() < mutprob:
			Swap_Targets(P[i])

def Evolution_Based_On_PCA(networkname, startgen, numgen, popsize, chosenfrac, mutprob, world_rank):
	import time
	import os
	import subprocess
	from shutil import copy
	if world_rank == 0:
		start_time = time.time()
		from pathlib import Path
		P = []
		if startgen > 0:
			RACIPE_Folder = 'RACIPE_Output'
			for i in range(popsize):
				P.append(Read_Network('RACIPE_Output/RUN_' + str(i) + '/network_' + str(i) + '.topo'))
			scores = Get_PCA_Score(P, RACIPE_Folder)
			Get_Next_Generation(scores, P, chosenfrac, mutprob)
		if startgen == 0:
			for i in range(popsize):
				Path('RACIPE_Output/RUN_' + str(i)).mkdir()
			for i in range(popsize):
				Generate_Random_Networks('../../networkfiles/' + networkname + '.topo', 'RACIPE_Output/RUN_' + str(i) + '/network_' + str(i) + '.topo')
			for i in range(popsize):
				P.append(Read_Network('RACIPE_Output/RUN_' + str(i) + '/network_' + str(i) + '.topo'))
		pcafile = open('outputfiles/PCA_score.log', 'a')
		frustfile = open('outputfiles/frustration.log', 'a')
		T = 0 if startgen == 0 else startgen + 1
		while (T - startgen) <= numgen:
			for i in range(popsize):
				if T > 0:
					for filename in os.listdir('RACIPE_Output/RUN_' + str(i)):
						subprocess.run(['rm', filename], cwd = 'RACIPE_Output/RUN_' + str(i))
				copy('../../code/RACIPE', 'RACIPE_Output/RUN_' + str(i))
				Write_Network(P[i], 'RACIPE_Output/RUN_' + str(i) + '/network_' + str(i) + '.topo')
				with open('RACIPE_Output/RUN_' + str(i) + '/status.log', 'w') as f:
					f.write('Ready for generation ' + str(T) + '.\n')
			while True:
				time.sleep(5.0)
				flag = 0
				for i in range(popsize):
					if not os.path.isfile('RACIPE_Output/RUN_' + str(i) + '/slurm.out'):
						flag = 1
				if flag == 0:
					break
			RACIPE_Folder = 'RACIPE_Output'
			scores = Get_PCA_Score(P, RACIPE_Folder)
			F = []
			for i in range(len(P)):
				F.append(Get_Frustration_Score(P[i], 50))
			pcafile.write(str(T) + ' ')
			frustfile.write(str(T) + ' ')
			for i in range(len(P)):
				pcafile.write(str(scores[i]) + ' ')
				frustfile.write(str(F[i]) + ' ')
			pcafile.write('\n')
			frustfile.write('\n')
			if T % 10 == 0:
				Path('generationfiles/RUN_' + str(T)).mkdir()
				for i in range(len(P)):
					Write_Network(P[i], 'generationfiles/RUN_' + str(T) + '/network_' + str(i) + '.topo')
			Get_Next_Generation(scores, P, chosenfrac, mutprob)
			curr_time = time.time()
			if (start_time - curr_time) / 3600.0 > 23.0:
				break
			T += 1
		for i in range(popsize):
			with open('RACIPE_Output/RUN_' + str(i) + '/endstatus.log', 'w') as f:
				f.write('That\'s all folks!\n')
		time.sleep(300.0)
		for i in range(popsize):
			subprocess.run(['rm', 'endstatus.log'], cwd = 'RACIPE_Output/RUN_' + str(i))
		pcafile.close()
		frustfile.close()
	else:
		RACIPE_Folder = 'RACIPE_Output/RUN_' + str(world_rank - 1)
		while True:
			if not os.path.isfile(RACIPE_Folder + '/status.log'):
				time.sleep(5.0)
			else:
				RACIPE_Output = subprocess.run(['./RACIPE', 'network_' + str(world_rank - 1) + '.topo', '-num_paras', '50', '-num_ode', '10', '-seed', str(world_rank - 1)], cwd = RACIPE_Folder, capture_output = True, text = True)
				with open(RACIPE_Folder + '/slurm.out', 'w') as f:
					f.write(RACIPE_Output.stdout)
				subprocess.run(['rm', 'status.log'], cwd = RACIPE_Folder)
			if os.path.isfile(RACIPE_Folder + '/endstatus.log'):
				break
