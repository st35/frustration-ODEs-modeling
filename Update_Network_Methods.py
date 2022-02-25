def Remove_Nodes(inputnetwork, world_rank, updateindex):
	from random import randint

	nodenames = []
	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/network_' + str(updateindex) + '.ids', 'r') as f:
		for line in f:
			l = line.strip().split('\t')
			nodenames.append(l[0].strip())

	deletednode = randint(0, len(nodenames) - 1)

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

def Remove_Edges(inputnetwork, world_rank, updateindex):
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
