def Generate_Random_Networks(inputfile, outputfile):
	from math import floor, log
	import random

	R = []
	with open(inputfile, 'r') as f:
		count = 0
		for line in f:
			if count == 0:
				count += 1
				continue
			l = line.strip().split('\t')
			R.append([l[0].strip(), l[1].strip(), l[2].strip()])

	R_new = []
	E = []
	for j in range(len(R)):
		R_new.append([R[j][0], R[j][1], R[j][2]])
		E.append(R[j][0] + '**>' + R[j][1])
	N = int(floor(log(1e7)*len(R_new) / 2))
	N = N*10
	for j in range(N):
		edge1 = random.randint(0, len(R_new) - 1)
		edge2 = edge1
		while edge2 == edge1:
			if len(R) == 1:
				break
			edge2 = random.randint(0, len(R_new) - 1)
		target1 = R_new[edge1][1]
		target2 = R_new[edge2][1]
		old_edge_1 = R_new[edge1][0] + '**>' + R_new[edge1][1]
		old_edge_2 = R_new[edge2][0] + '**>' + R_new[edge2][1]
		new_edge_1 = R_new[edge1][0] + '**>' + target2
		new_edge_2 = R_new[edge2][0] + '**>' + target1
		if new_edge_1 not in E and new_edge_2 not in E:
			R_new[edge1][1] = target2
			R_new[edge2][1] = target1
			E.remove(old_edge_1)
			E.remove(old_edge_2)
			E.append(new_edge_1)
			E.append(new_edge_2)

	if len(R) != len(E):
		print('Was I supposed to tackle her?')

	with open(outputfile, 'w') as f:
		f.write('Source\tTarget\tType\n')
		for j in range(len(R_new)):
			f.write(R_new[j][0] + '\t' + R_new[j][1] + '\t' + R_new[j][2] + '\n')

def Process_RACIPE_Output(filename):
	IDs = {}
	Names = {}
	flag = 0
	numlines = 0
	with open(filename + '.cfg', 'r') as f:
		for line in f:
			if flag == 1:
				l = line.strip().split('\t')
				geneid = int(l[0].strip())
				if geneid > numlines:
					break
				gene = l[1].strip()
				IDs[geneid - 1] = gene
				Names[gene] = geneid - 1
			if 'NumberOfGenes' in line:
				flag = 1
				l = line.strip().split('\t')
				numlines = int(l[1].strip())
	with open(filename + '.ids', 'w') as f:
		for i in range(len(IDs)):
			f.write(IDs[i] + '\t' + str(i) + '\n')
	count = 0
	T = []
	for i in range(len(IDs)):
		T.append([])
		for j in range(len(IDs)):
			T[i].append(0)
	Links = []
	with open(filename + '.topo', 'r') as f:
		for line in f:
			if count == 0:
				count += 1
				continue
			l = line.strip().split('\t')
			source = l[0].strip()
			target = l[1].strip()
			T[Names[source]][Names[target]] = int(l[2].strip())
	L = []
	for i in range(len(IDs)):
		L.append([])
		for j in range(len(IDs)):
			L[i].append(0)
	linkindex = 2*len(IDs)
	with open(filename + '.prs', 'r') as f:
		for line in f:
			if 'Trd_of_' not in line:
				continue
			l = line.strip().split('\t')
			linkname = l[0].strip()
			index1 = linkname.index('_of_')
			index2 = linkname.index('To')
			source = linkname[index1 + 4:index2]
			target = linkname[index2 + 2:]
			L[Names[source]][Names[target]] = linkindex
			linkindex += 3
	with open(filename + '_T_matrix.log', 'w') as f:
		for i in range(len(T)):
			for j in range(len(T[i])):
				if j == len(T[i]) - 1:
					f.write(str(T[i][j]))
				else:
					f.write(str(T[i][j]) + '\t')
			f.write('\n')
	with open(filename + '_L_matrix.log', 'w') as f:
		for i in range(len(L)):
			for j in range(len(L[i])):
				if j == len(L[i]) - 1:
					f.write(str(L[i][j]))
				else:
					f.write(str(L[i][j]) + '\t')
			f.write('\n')

def Write_Steady_States(RACIPE_Folder, networkname, outputfolder, outputname):
	import os

	nodes = set()
	linecount = 0
	with open(RACIPE_Folder + '/' + networkname + '.topo', 'r') as f:
		for line in f:
			if linecount == 0:
				linecount += 1
				continue
			l = line.strip().split('\t')
			nodes.add(l[0].strip())
			nodes.add(l[1].strip())
	numnodes = len(nodes)
	S = []
	numstates = []
	setid = []
	count = 0
	for filename in os.listdir(RACIPE_Folder):
		if 'solution' not in filename:
			continue
		with open(RACIPE_Folder + '/' + filename, 'r') as f:
			for line in f:
				if 'nan' in line.strip():
					continue
				l = line.strip().split('\t')
				if (len(l) - 2) % numnodes != 0:
					print('A pharmacist.')
					return(1)
				numstates.append((len(l) - 2) / numnodes)
				setid.append(int(l[0].strip()))
				S.append([])
				for i in range(2, len(l)):
					S[count].append(float(l[i]))
					if len(S[count]) == numnodes and i != len(l) - 1:
						count += 1
						S.append([])
						setid.append(int(l[0].strip()))
				count += 1
	if len(setid) != len(S):
		print('Goliath National Bank')
	with open(outputfolder + '/' + outputname, 'w') as f:
		for i in range(len(S)):
			f.write(str(setid[i]) + ' ')
			for j in range(len(S[i])):
				f.write(str(S[i][j]) + ' ')
			f.write('\n')

	return(0)

def Steadystates_PCA(filename, skipcount):
	import numpy as np
	from sklearn.decomposition import PCA

	S = []
	count = 0
	with open(filename, 'r') as f:
		for line in f:
			l = line.strip().split(' ')
			S.append([])
			for i in range(skipcount, len(l)):
				S[count].append(float(l[i].strip()))
			count += 1
	states = np.array(S)
	pca = PCA(n_components = min(len(S), len(S[0])))
	pca.fit(states)

	return(pca.explained_variance_ratio_)

def Steadystates_PCA_Norm(filename, skipcount):
	import numpy as np
	from sklearn.decomposition import PCA
	from scipy.stats import zscore

	S = []
	count = 0
	with open(filename, 'r') as f:
		for line in f:
			l = line.strip().split(' ')
			S.append([])
			for i in range(skipcount, len(l)):
				S[count].append(float(l[i].strip()))
			count += 1
	states = np.array(S)
	states = zscore(S)
	pca = PCA(n_components = min(len(S), len(S[0])))
	pca.fit(states)

	return(pca.explained_variance_ratio_)


def Write_IDS_File(topofile, outputfile):
	IDs = []
	with open(topofile, 'r') as f:
		count = 0
		for line in f:
			if count == 0:
				count += 1
				continue
			l = line.strip().split('\t')
			if l[0].strip() not in IDs:
				IDs.append(l[0].strip())
			if l[1].strip() not in IDs:
				IDs.append(l[1].strip())
	with open(outputfile, 'w') as f:
		for i in range(len(IDs)):
			f.write(IDs[i] + '\t' + str(i) + '\n')
