from Util_Methods import *
from Boolean_Dynamics_Methods import *

def Evolution_Simulation_F_Based_Selection(networkname, world_rank, startgen, numgen, popsize, chosenfrac, mutprob):
	from pathlib import Path
	from copy import deepcopy
	from random import randint, random

	P = []

	if startgen == 0:
		Path('generationfiles/RUN_' + str(world_rank)).mkdir()
		Path('generationfiles/RUN_' + str(world_rank) + '/RUN_' + str(0)).mkdir()
		for i in range(popsize):
			Generate_Random_Networks('../../networkfiles/' + networkname + '.topo', 'generationfiles/RUN_' + str(world_rank) + '/RUN_' + str(0) + '/network_' + str(i) + '.topo')
		for i in range(popsize):
			P.append(Read_Network('generationfiles/RUN_' + str(world_rank) + '/RUN_' + str(0) + '/network_' + str(i) + '.topo'))
		frustration_file = open('generationfiles/RUN_' + str(world_rank) + '/frustration.log', 'w')
	else:
		for i in range(popsize):
			P.append(Read_Network('generationfiles/RUN_' + str(world_rank) + '/RUN_' + str(startgen) + '/network_' + str(i) + '.topo'))
		frustration_file = open('generationfiles/RUN_' + str(world_rank) + '/frustration.log', 'a')

	T = 0 if startgen == 0 else startgen + 1
	while (T - startgen) <= numgen:
		F = []
		for i in range(len(P)):
			F.append(Get_Frustration_Score(P[i], 50))
		if T % 50 == 0 and T != 0:
			Path('generationfiles/RUN_' + str(world_rank) + '/RUN_' + str(T)).mkdir()
			for i in range(len(P)):
				Write_Network(P[i], 'generationfiles/RUN_' + str(world_rank) + '/RUN_' + str(T) + '/network_' + str(i) + '.topo')
		if T % 5 == 0:
			frustration_file.write(str(T) + ' ')
			for i in range(len(F)):
				frustration_file.write(str(F[i]) + ' ')
			frustration_file.write('\n')
				
		I = [i for i in range(len(F))]
		SI = [x for _, x in sorted(zip(F, I), key = lambda pair: pair[0])]
		F = sorted(F)
		chosen = int(chosenfrac*len(P))
		SP = [deepcopy(P[i]) for i in range(len(P))]
		P.clear()
		while len(P) < len(SP):
			P.append(deepcopy(SP[SI[randint(0, chosen - 1)]]))
		for i in range(len(P)):
			if random() < mutprob:
				Swap_Targets(P[i])
		T += 1
