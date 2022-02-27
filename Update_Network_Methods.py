def Remove_Nodes(orderid, inputnetwork, world_rank, updateindex):
	from random import randint

	nodenames = []
	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/network_' + str(updateindex) + '.ids', 'r') as f:
		for line in f:
			l = line.strip().split('\t')
			nodenames.append(l[0].strip())

	deletednode = randint(0, len(nodenames) - 1)
	if orderid != 0:
		S = []
		with open('sensitivities/RUN_' + str(world_rank) + '/sensitivity_' + str(updateindex) + '.log', 'r') as f:
			for line in f:
				S.append(float(line.strip()))
		I = []
		if orderid == -1:
			I = [] + [i[0] for i in sorted(enumerate(S), key = lambda x:x[1], reverse = True)]
		else:
			I = [] + [i[0] for i in sorted(enumerate(S), key = lambda x:x[1])]
		deletednode = I[0]

	T = []
	count = 0
	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/network_' + str(updateindex) + '_T_matrix.log', 'r') as f:
		for line in f:
			l = line.strip().split('\t')
			T.append([])
			for i in range(len(l)):
				T[count].append(int(l[i].strip()))
			count += 1

	edgecount = 0
	newnodes = set()
	with open('updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex + 1) + '.topo', 'w') as f:
		f.write('Source\tTarget\tType\n')
		for i in range(len(T)):
			for j in range(len(T)):
				if T[i][j] == 0:
					continue
				if i == deletednode or j == deletednode:
					continue
				f.write(nodenames[i] + '\t' + nodenames[j] + '\t' + str(T[i][j]) + '\n')
				newnodes.add(nodenames[i])
				newnodes.add(nodenames[j])
				edgecount += 1

	return edgecount

def Remove_Edges(orderid, inputnetwork, world_rank, updateindex):
	from random import randint

	nodenames = []
	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/network_' + str(updateindex) + '.ids', 'r') as f:
		for line in f:
			l = line.strip().split('\t')
			nodenames.append(l[0].strip())
	T = []
	count = 0
	edgeids = []
	edgeid = 0
	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/network_' + str(updateindex) + '_T_matrix.log', 'r') as f:
		for line in f:
			l = line.strip().split('\t')
			T.append([])
			for i in range(len(l)):
				T[count].append(int(l[i].strip()))
				if int(l[i].strip()) != 0:
					edgeids.append(edgeid)
					edgeid += 1
			count += 1
	deletededge = edgeids[randint(0, len(edgeids) - 1)]

	if orderid != 0:
		S = []
		count = 0
		with open('sensitivities/RUN_' + str(world_rank) + '/sensitivity_' + str(updateindex) + '.log', 'r') as f:
			for line in f:
				l = line.strip().split(' ')
				for i in range(len(l)):
					if T[count][i] > 0:
						S.append(float(l[i].strip()))
				count += 1
		I = []
		if orderid == -1:
			I = [] + [i[0] for i in sorted(enumerate(S), key = lambda x:x[1], reverse = True)]
		else:
			I = [] + [i[0] for i in sorted(enumerate(S), key = lambda x:x[1])]
		deletededge = I[0]


	edgecount = 0
	edgeid = 0
	with open('updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex + 1) + '.topo', 'w') as f:
		f.write('Source\tTarget\tType\n')
		for i in range(len(T)):
			for j in range(len(T)):
				if T[i][j] == 0:
					continue
				if edgeid == deletededge:
					edgeid += 1
					continue
				f.write(nodenames[i] + '\t' + nodenames[j] + '\t' + str(T[i][j]) + '\n')
				edgecount += 1
				edgeid += 1
	if edgecount - len(edgeids) != -1:
		print('Cowhouses')

	return edgecount
