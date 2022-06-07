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

def Remove_Nodes_With_Exclusion(orderid, inputnetwork, world_rank, updateindex, excluded):
	from random import randint

	nodenames = []
	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/network_' + str(updateindex) + '.ids', 'r') as f:
		for line in f:
			l = line.strip().split('\t')
			nodenames.append(l[0].strip())

	deletednode = randint(0, len(nodenames) - 1)
	while nodenames[deletednode] in excluded:
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
		startindex = 0
		deletednode = I[0]
		while nodenames[deletednode] in excluded:
			startindex += 1
			deletednodes = I[startindex]
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

	return (len(newnodes), edgecount)

def Remove_Nodes_With_Exclusion_Alt(orderid, inputnetwork, world_rank, updateindex, excluded):
	from random import randint

	nodenames = []
	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/network_' + str(updateindex) + '.ids', 'r') as f:
		for line in f:
			l = line.strip().split('\t')
			nodenames.append(l[0].strip())

	attempts = 0
	properflag = 0
	while attempts <= 50 and properflag == 0:
		deletednode = randint(0, len(nodenames) - 1)
		while nodenames[deletednode] in excluded:
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
			startindex = 0
			deletednode = I[0]
			while nodenames[deletednode] in excluded:
				startindex += 1
				deletednodes = I[startindex]
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
		properflag = 1
		for node in excluded:
			if node not in newnodes:
				properflag = 0
				break

		attempts += 1
	
	return (len(newnodes), edgecount, properflag)

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

def Remove_Edges_With_Inclusions(orderid, inputnetwork, world_rank, updateindex, included):
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
	deletededge = -1
	inclsig = 0
	startindex = 0
	nodecount = 0
	itercount = 0
	sig = 0
	while deletededge == -1 or inclsig == 0:
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
			deletededge = I[startindex]

		edgecount = 0
		edgeid = 0
		newnodes = set()
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
					newnodes.add(nodenames[i])
					newnodes.add(nodenames[j])
					edgecount += 1
					edgeid += 1
		if edgecount - len(edgeids) != -1:
			print('Cowhouses')
		inclsig = 1
		for node in included:
			if node not in newnodes:
				inclsig = 0
				break
		nodecount = len(newnodes)

		itercount += 1
		if itercount > 100:
			sig = -1
			break

		startindex += 1

	return (nodecount, edgecount, sig)

def Remove_Multiple_Edges_With_Inclusions(orderid, inputnetwork, world_rank, updateindex, included, number_deleted):
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
	deletededge = []
	inclsig = 0
	startindex = 0
	nodecount = 0
	itercount = 0
	sig = 0
	while len(deletededge) == 0 or inclsig == 0:
#		deletededge = edgeids[randint(0, len(edgeids) - 1)]
		RDNT = [randint(0, len(edgeids) -1) for i in range(number_deleted)]
		deletededge = [edgeids[index] for index in RDNT]

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
#			deletededge = I[startindex]
			deletededge = I[:number_deleted]

		edgecount = 0
		edgeid = 0
		newnodes = set()
		with open('updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex + 1) + '.topo', 'w') as f:
			f.write('Source\tTarget\tType\n')
			for i in range(len(T)):
				for j in range(len(T)):
					if T[i][j] == 0:
						continue
					if edgeid in deletededge:
						edgeid += 1
						continue
					f.write(nodenames[i] + '\t' + nodenames[j] + '\t' + str(T[i][j]) + '\n')
					newnodes.add(nodenames[i])
					newnodes.add(nodenames[j])
					edgecount += 1
					edgeid += 1
		if edgecount - len(edgeids) != -1:
			print('Cowhouses')
		inclsig = 1
		for node in included:
			if node not in newnodes:
				inclsig = 0
				break
		nodecount = len(newnodes)

		itercount += 1
		if itercount > 100:
			sig = -1
			break

		startindex += 1

	return (nodecount, edgecount, sig)


def Merge_Nodes(mergeid, inputnetwork, world_rank, updateindex):
	from random import random, shuffle

	named_nodeids = {}
	named_idnodes = {}
	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/network_' + str(updateindex) + '.ids', 'r') as f:
		for line in f:
			l = line.strip().split('\t')
			named_nodeids[l[0].strip()] = int(l[1].strip())
			named_idnodes[int(l[1].strip())] = l[0].strip()
	nodeids = {}
	idnodes = {}
	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/unnamednetwork_' + str(updateindex) + '.ids', 'r') as f:
		for line in f:
			l = line.strip().split('\t')
			nodeids[l[0].strip()] = int(l[1].strip())
			idnodes[int(l[1].strip())] = l[0].strip()
	numnodes = len(nodeids)
	network = []
	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/unnamednetwork_' + str(updateindex) + '.topo', 'r') as f:
		count = 0
		for line in f:
			if count == 0:
				count += 1
				continue
			l = line.strip().split('\t')
			network.append((nodeids[l[0].strip()], nodeids[l[1].strip()], int(l[2].strip())))
	linkages = []
	clusters = {}
	clusterindex = numnodes
	with open('linkages/RUN_' + str(world_rank) + '/linkage_' + str(updateindex) + '.log', 'r') as f:
		for line in f:
			l = line.strip().split('\t')
			node0 = int(l[0].strip()) - 1
			node1 = int(l[1].strip()) - 1
			if node0 < numnodes and node1 < numnodes:
				linkages.append((node0, node1))
				if node0 in clusters or node1 in clusters:
					print('MATLAB is at it. Once again.')
				clusters[node0] = clusterindex
				clusters[node1] = clusterindex
				named_idnodes[clusterindex] = named_idnodes[node0] + '::' + named_idnodes[node1]
				clusterindex += 1
	if mergeid == 1:
		l0 = [x for x, _ in linkages]
		l1 = [x for _, x in linkages]
		shuffle(l0)
		shuffle(l1)
		linkages = [(l0[i], l1[i]) for i in range(len(l0))]
		clusters = {}
		clusterindex = numnodes
		for i in range(len(linkages)):
			clusters[linkages[i][0]] = clusterindex
			clusters[linkages[i][1]] = clusterindex
			named_idnodes[clusterindex] = named_idnodes[linkages[i][0]] + '::' + named_idnodes[linkages[i][1]]
			clusterindex += 1

	updatednetwork = []
	for i in range(len(network)):
		node0 = network[i][0]
		node1 = network[i][1]
		typ = network[i][2]
		if node0 in clusters and node1 in clusters:
			if node0 != node1:
				updatednetwork.append((clusters[node0], clusters[node1], typ))
			else:
				updatednetwork.append((clusters[node0], clusters[node1], typ))
		elif node0 in clusters and node1 not in clusters:
			updatednetwork.append((clusters[node0], node1, typ))
		elif node0 not in clusters and node1 in clusters:
			updatednetwork.append((node0, clusters[node1], typ))
		else:
			updatednetwork.append((node0, node1, typ))
	Counts = {}
	for i in range(len(updatednetwork)):
		if updatednetwork[i] in Counts:
			Counts[updatednetwork[i]] += 1
		else:
			Counts[updatednetwork[i]] = 1
	Repeats = {}
	for i in range(len(updatednetwork)):
		if Counts[updatednetwork[i]] > 1:
			if updatednetwork[i][0] == updatednetwork[i][1] and updatednetwork[i][0] < numnodes:
				print('Level 5.')
			if updatednetwork[i] not in Repeats:
				Repeats[updatednetwork[i]] = []
			Repeats[updatednetwork[i]].append(updatednetwork[i][2])
	nodeset = set()
	Pairs_Added = []
	with open('updatednetworks/RUN_' + str(world_rank) + '/unnamednetwork_' + str(updateindex + 1) + '.topo', 'w') as f, open('updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex + 1) + '.topo', 'w') as g:
		f.write('Source\tTarget\tType\n')
		g.write('Source\tTarget\tType\n')
		for i in range(len(updatednetwork)):
			if (updatednetwork[i][0], updatednetwork[i][1]) in Pairs_Added:
				continue
			Pairs_Added.append((updatednetwork[i][0], updatednetwork[i][1]))
			if updatednetwork[i] not in Repeats:
				f.write('C' + str(updatednetwork[i][0]) + '\t' + 'C' + str(updatednetwork[i][1]) + '\t' + str(updatednetwork[i][2]) + '\n')
				g.write(named_idnodes[updatednetwork[i][0]] + '\t' + named_idnodes[updatednetwork[i][1]] + '\t' + str(updatednetwork[i][2]) + '\n')
				nodeset.add('C' + str(updatednetwork[i][0]))
				nodeset.add('C' + str(updatednetwork[i][1]))
			else:
				onecount = sum([1 for val in Repeats[updatednetwork[i]] if val == 1])
				twocount = sum([1 for val in Repeats[updatednetwork[i]] if val == 2])
				if onecount > twocount:
					f.write('C' + str(updatednetwork[i][0]) + '\t' + 'C' + str(updatednetwork[i][1]) + '\t' + str(1) + '\n')
					g.write(named_idnodes[updatednetwork[i][0]] + '\t' + named_idnodes[updatednetwork[i][1]] + '\t' + str(1) + '\n')
					nodeset.add('C' + str(updatednetwork[i][0]))
					nodeset.add('C' + str(updatednetwork[i][1]))
				elif onecount < twocount:
					f.write('C' + str(updatednetwork[i][0]) + '\t' + 'C' + str(updatednetwork[i][1]) + '\t' + str(2) + '\n')
					g.write(named_idnodes[updatednetwork[i][0]] + '\t' + named_idnodes[updatednetwork[i][1]] + '\t' + str(2) + '\n')
					nodeset.add('C' + str(updatednetwork[i][0]))
					nodeset.add('C' + str(updatednetwork[i][1]))
				else:
					if random() < 0.5:
						f.write('C' + str(updatednetwork[i][0]) + '\t' + 'C' + str(updatednetwors[i][1]) + '\t' + str(1) + '\n')
						g.write(named_idnodes[updatednetwork[i][0]] + '\t' + named_idnodes[updatednetwors[i][1]] + '\t' + str(1) + '\n')
						nodeset.add('C' + str(updatednetwork[i][0]))
						nodeset.add('C' + str(updatednetwork[i][1]))
					else:
						f.write('C' + str(updatednetwork[i][0]) + '\t' + 'C' + str(updatednetwork[i][1]) + '\t' + str(2) + '\n')
						g.write(named_idnodes[updatednetwork[i][0]] + '\t' + named_idnodes[updatednetwork[i][1]] + '\t' + str(2) + '\n')
						nodeset.add('C' + str(updatednetwork[i][0]))
						nodeset.add('C' + str(updatednetwork[i][1]))

	return len(nodeset)

if __name__ == '__main__':
	Included = []
	with open('Included.log', 'r') as f:
		for line in f:
			if len(line.strip()) > 0:
				Included.append(line.strip())
	print(len(Included))
	N = Remove_Edges_With_Inclusions(0, 'terenuma', 0, 0, Included)
	print(N)
#def Merge_Nodes_With_Exclusions(mergeid, inputnetwork, world_rank, updateindex):
#	from random import random, shuffle
#
#	named_nodeids = {}
#	named_idnodes = {}
#	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/network_' + str(updateindex) + '.ids', 'r') as f:
#		for line in f:
#			l = line.strip().split('\t')
#			named_nodeids[l[0].strip()] = int(l[1].strip())
#			named_idnodes[int(l[1].strip())] = l[0].strip()
#	nodeids = {}
#	idnodes = {}
#	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/unnamednetwork_' + str(updateindex) + '.ids', 'r') as f:
#		for line in f:
#			l = line.strip().split('\t')
#			nodeids[l[0].strip()] = int(l[1].strip())
#			idnodes[int(l[1].strip())] = l[0].strip()
#	numnodes = len(nodeids)
#	network = []
#	with open('RACIPE_Output/RUN_' + str(world_rank) + '/RUN_' + str(updateindex) + '/unnamednetwork_' + str(updateindex) + '.topo', 'r') as f:
#		count = 0
#		for line in f:
#			if count == 0:
#				count += 1
#				continue
#			l = line.strip().split('\t')
#			network.append((nodeids[l[0].strip()], nodeids[l[1].strip()], int(l[2].strip())))
#	linkages = []
#	clusters = {}
#	clusterindex = numnodes
#	with open('linkages/RUN_' + str(world_rank) + '/linkage_' + str(updateindex) + '.log', 'r') as f:
#		for line in f:
#			l = line.strip().split('\t')
#			node0 = int(l[0].strip()) - 1
#			node1 = int(l[1].strip()) - 1
#			if node0 < numnodes and node1 < numnodes:
#				linkages.append((node0, node1))
#				if node0 in clusters or node1 in clusters:
#					print('MATLAB is at it. Once again.')
#				clusters[node0] = clusterindex
#				clusters[node1] = clusterindex
#				named_idnodes[clusterindex] = named_idnodes[node0] + '::' + named_idnodes[node1]
#				clusterindex += 1
#	if mergeid == 1:
#		l0 = [x for x, _ in linkages]
#		l1 = [x for _, x in linkages]
#		shuffle(l0)
#		shuffle(l1)
#		linkages = [(l0[i], l1[i]) for i in range(len(l0))]
#		clusters = {}
#		clusterindex = numnodes
#		for i in range(len(linkages)):
#			clusters[linkages[i][0]] = clusterindex
#			clusters[linkages[i][1]] = clusterindex
#			named_idnodes[clusterindex] = named_idnodes[linkages[i][0]] + '::' + named_idnodes[linkages[i][1]]
#			clusterindex += 1
#
#	updatednetwork = []
#	for i in range(len(network)):
#		node0 = network[i][0]
#		node1 = network[i][1]
#		typ = network[i][2]
#		if node0 in clusters and node1 in clusters:
#			if node0 != node1:
#				updatednetwork.append((clusters[node0], clusters[node1], typ))
#			else:
#				updatednetwork.append((clusters[node0], clusters[node1], typ))
#		elif node0 in clusters and node1 not in clusters:
#			updatednetwork.append((clusters[node0], node1, typ))
#		elif node0 not in clusters and node1 in clusters:
#			updatednetwork.append((node0, clusters[node1], typ))
#		else:
#			updatednetwork.append((node0, node1, typ))
#	Counts = {}
#	for i in range(len(updatednetwork)):
#		if updatednetwork[i] in Counts:
#			Counts[updatednetwork[i]] += 1
#		else:
#			Counts[updatednetwork[i]] = 1
#	Repeats = {}
#	for i in range(len(updatednetwork)):
#		if Counts[updatednetwork[i]] > 1:
#			if updatednetwork[i][0] == updatednetwork[i][1] and updatednetwork[i][0] < numnodes:
#				print('Level 5.')
#			if updatednetwork[i] not in Repeats:
#				Repeats[updatednetwork[i]] = []
#			Repeats[updatednetwork[i]].append(updatednetwork[i][2])
#	nodeset = set()
#	Pairs_Added = []
#	with open('updatednetworks/RUN_' + str(world_rank) + '/unnamednetwork_' + str(updateindex + 1) + '.topo', 'w') as f, open('updatednetworks/RUN_' + str(world_rank) + '/network_' + str(updateindex + 1) + '.topo', 'w') as g:
#		f.write('Source\tTarget\tType\n')
#		g.write('Source\tTarget\tType\n')
#		for i in range(len(updatednetwork)):
#			if (updatednetwork[i][0], updatednetwork[i][1]) in Pairs_Added:
#				continue
#			Pairs_Added.append((updatednetwork[i][0], updatednetwork[i][1]))
#			if updatednetwork[i] not in Repeats:
#				f.write('C' + str(updatednetwork[i][0]) + '\t' + 'C' + str(updatednetwork[i][1]) + '\t' + str(updatednetwork[i][2]) + '\n')
#				g.write(named_idnodes[updatednetwork[i][0]] + '\t' + named_idnodes[updatednetwork[i][1]] + '\t' + str(updatednetwork[i][2]) + '\n')
#				nodeset.add('C' + str(updatednetwork[i][0]))
#				nodeset.add('C' + str(updatednetwork[i][1]))
#			else:
#				onecount = sum([1 for val in Repeats[updatednetwork[i]] if val == 1])
#				twocount = sum([1 for val in Repeats[updatednetwork[i]] if val == 2])
#				if onecount > twocount:
#					f.write('C' + str(updatednetwork[i][0]) + '\t' + 'C' + str(updatednetwork[i][1]) + '\t' + str(1) + '\n')
#					g.write(named_idnodes[updatednetwork[i][0]] + '\t' + named_idnodes[updatednetwork[i][1]] + '\t' + str(1) + '\n')
#					nodeset.add('C' + str(updatednetwork[i][0]))
#					nodeset.add('C' + str(updatednetwork[i][1]))
#				elif onecount < twocount:
#					f.write('C' + str(updatednetwork[i][0]) + '\t' + 'C' + str(updatednetwork[i][1]) + '\t' + str(2) + '\n')
#					g.write(named_idnodes[updatednetwork[i][0]] + '\t' + named_idnodes[updatednetwork[i][1]] + '\t' + str(2) + '\n')
#					nodeset.add('C' + str(updatednetwork[i][0]))
#					nodeset.add('C' + str(updatednetwork[i][1]))
#				else:
#					if random() < 0.5:
#						f.write('C' + str(updatednetwork[i][0]) + '\t' + 'C' + str(updatednetwors[i][1]) + '\t' + str(1) + '\n')
#						g.write(named_idnodes[updatednetwork[i][0]] + '\t' + named_idnodes[updatednetwors[i][1]] + '\t' + str(1) + '\n')
#						nodeset.add('C' + str(updatednetwork[i][0]))
#						nodeset.add('C' + str(updatednetwork[i][1]))
#					else:
#						f.write('C' + str(updatednetwork[i][0]) + '\t' + 'C' + str(updatednetwork[i][1]) + '\t' + str(2) + '\n')
#						g.write(named_idnodes[updatednetwork[i][0]] + '\t' + named_idnodes[updatednetwork[i][1]] + '\t' + str(2) + '\n')
#						nodeset.add('C' + str(updatednetwork[i][0]))
#						nodeset.add('C' + str(updatednetwork[i][1]))
#
#	return (len(nodeset), len(linkages))
