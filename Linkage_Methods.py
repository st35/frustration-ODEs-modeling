def Get_Clusters(inputnetworkid, updateindex, excludedids, numnodes):
	import numpy as np
	from scipy.spatial.distance import pdist
	from scipy.cluster.hierarchy import linkage

	newids = {}
	newidsrev = {}
	index = 0
	for i in range(numnodes):
		if i in excludedids:
			continue
		newids[i] = index
		newidsrev[index] = i
		index += 1
	print(newidsrev)
	D = []
	index = 0
	with open('steadystates/RUN_' + str(inputnetworkid) + '/network_' + str(updateindex) + '.log', 'r') as f:
		for line in f:
			l = line.strip().split(' ')
			D.append([])
			for i in range(1, len(l)):
				if i - 1 not in excludedids:
					D[index].append(float(l[i].strip()))
			index += 1
	if len(D) == 0 or len(D[0]) < 2:
		return -1
	M = np.transpose(np.array(D))

	dist = pdist(M, metric = 'correlation')
	L = linkage(dist)

	with open('linkages/RUN_' + str(inputnetworkid) + '/linkage_' + str(updateindex) + '.log', 'w') as f:
		for i in range(L.shape[0]):
			if L[i][0] < M.shape[0] and L[i][1] < M.shape[0]:
					f.write(str(newidsrev[int(L[i][0])] + 1) + '\t' + str(newidsrev[int(L[i][1])] + 1) + '\n')

	return 1

if __name__ == "__main__":
	exclnodes = []
	with open('Excluded.log', 'r') as f:
		for line in f:
			exclnodes.append(line.strip())
	excludedids = []
	with open('RACIPE_Output/RUN_' + str(inputnetworkid) + '/linkage_' + str(updateindex) + '.log', 'r') as f:
		for line in f:
			l = line.strip().split('\t')
			if l[0] in exclnodes:
				excludedids.append(int(l[1].strip()))
	Get_Clusters(0, 0, [], 26)
