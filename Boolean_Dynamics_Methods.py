class Network:
	def __init__(self, nodenames, T):
		flag = 0
		if len(T) != len(nodenames):
			flag = 1
		for i in range(len(T)):
			if len(T[i]) != len(nodenames):
				flag = 1
		self.nodenames = []
		self.T = []
		if flag == 1:
			print('What he believed to be igneous was in fact sedimentary.')
		else:
			self.nodenames = [] + nodenames
			for i in range(len(T)):
				self.T.append([] + T[i])
		self.numedges = 0
		for i in range(len(T)):
			for j in range(len(T)):
				if T[i][j] > 0:
					self.numedges += 1

def Read_Network(filename):
	nodenames = []
	with open(filename, 'r') as f:
		count = 0
		for line in f:
			if count == 0:
				count += 1
				continue
			l = line.strip().split('\t')
			source = l[0].strip()
			target = l[1].strip()
			if source not in nodenames:
				nodenames.append(source)
			if target not in nodenames:
				nodenames.append(target)
	T = []
	for i in range(len(nodenames)):
		T.append([])
		for j in range(len(nodenames)):
			T[i].append(0)
	with open(filename, 'r') as f:
		count = 0
		for line in f:
			if count == 0:
				count += 1
				continue
			l = line.strip().split('\t')
			source = l[0].strip()
			target = l[1].strip()
			typ = int(l[2].strip())
			sourceindex = nodenames.index(source)
			targetindex = nodenames.index(target)
			T[sourceindex][targetindex] = typ

	return(Network(nodenames, T))

def Write_Network(network, filename):
	with open(filename, 'w') as f:
		f.write('Source\tTarget\tType\n')
		for i in range(len(network.T)):
			for j in range(len(network.T[i])):
				if network.T[i][j] == 0:
					continue
				source = network.nodenames[i]
				target = network.nodenames[j]
				typ = str(network.T[i][j])
				f.write(source + '\t' + target + '\t' + typ + '\n')

def Swap_Targets(network):
	from random import randint

	numnodes = len(network.nodenames)
	edges = []
	for i in range(numnodes):
		for j in range(numnodes):
			if network.T[i][j] > 0:
				edges.append([i, j, network.T[i][j]])
	while True:
		index0 = randint(0, len(edges) - 1)
		index1 = randint(0, len(edges) - 1)
		while index0 == index1:
			index1 = randint(0, len(edges) - 1)
		edge0 = edges[index0]
		edge1 = edges[index1]
		newedge0 = edge0.copy()
		newedge1 = edge1.copy()
		newedge0[1] = edge1[1]
		newedge1[1] = edge0[1]
		innerflag = 0
		for i in range(len(edges)):
			if edges[i][0] == newedge0[0] and edges[i][1] == newedge0[1]:
				innerflag = 1
			if edges[i][0] == newedge1[0] and edges[i][1] == newedge1[1]:
				innerflag = 1
		if innerflag == 0:
			network.T[edge0[0]][edge0[1]] = 0
			network.T[edge1[0]][edge1[1]] = 0
			network.T[newedge0[0]][newedge0[1]] = newedge0[2]
			network.T[newedge1[0]][newedge1[1]] = newedge1[2]
		break

	numedges = 0
	for i in range(len(network.T)):
		for j in range(len(network.T[i])):
			if network.T[i][j] > 0:
				numedges += 1
	if numedges != network.numedges:
		print('Peter Gregory is dead.')

	return

def Get_Initial_Conditions(network):
	from random import randint

	numnodes = len(network.T)
	I = [randint(0, 1) for i in range(numnodes)]

	return(I)

def Simulate_Dynamics(network, state, numsteps):
	from random import randint

	if len(state) != len(network.nodenames):
		print('Figures, A Reprise.')
	errflag = 0
	for i in range(numsteps):
		nodetoupdate = randint(0, len(network.T) - 1)
		target = nodetoupdate
		inp = 0
		for i in range(len(network.T)):
			source = i
			if network.T[source][target] == 0:
				continue
			if network.T[source][target] == 1:
				if state[source] == 0:
					inp += (1)*(-1)
				elif state[source] == 1:
					inp += (1)*(1)
				else:
					errflag = 1
			elif network.T[source][target] == 2:
				if state[source] == 0:
					inp += (-1)*(-1)
				elif state[source] == 1:
					inp += (-1)*(1)
				else:
					errflag = 1
			else:
				errflag = 1
		if inp > 0:
			state[nodetoupdate] = 1
		elif inp < 0:
			state[nodetoupdate] = 0
		else:
			state[nodetoupdate] = state[nodetoupdate]

	if errflag == 1:
		print('Probably gonna call me crazy...')

def Calc_State_Frustration(network, state):
	F = 0.0
	if len(state) != len(network.nodenames):
		print('They are watching you right now.')
		return(-1.0)
	numedges = 0
	for i in range(len(network.T)):
		for j in range(len(network.T[i])):
			if network.T[i][j] == 0:
				continue
			numedges += 1
			s_i = -1 if state[i] == 0 else 1
			s_j = -1 if state[j] == 0 else 1
			J_ij = -1 if network.T[i][j] == 2 else 1
			fedge = J_ij*s_i*s_j
			if fedge < 0:
				F += 1.0
	if numedges != network.numedges:
		print('He shot Peter Gregory by accident?')
	F = F / float(numedges)

	return(F)

def Get_Frustration_Score(network, numiter):
	F = []
	for i in range(numiter):
		state = Get_Initial_Conditions(network)
		Simulate_Dynamics(network, state, 500)
		F.append(Calc_State_Frustration(network, state))

	return(min(F))
