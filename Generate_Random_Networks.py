def Get_Network_Features(filename):
	count = 0
	E = []
	flag = 0
	indegree = {}
	outdegree = {}
	actcount = 0
	inhcount = 0
	with open(filename, 'r') as f:
		for line in f:
			if count == 0:
				count += 1
				continue
			l = line.strip().split('\t')
			source = l[0].strip()
			target = l[1].strip()
			typ = l[2].strip()
			edge = source + '-->' + target + '--->' + typ
			if edge not in E:
				E.append(edge)
			else:
				flag = 1
			if source not in outdegree:
				outdegree[source] = 1
			else:
				outdegree[source] += 1
			if target not in indegree:
				indegree[target] = 1
			else:
				indegree[target] += 1
			if typ == '1':
				actcount += 1
			elif typ == '2':
				inhcount += 1

	return flag, indegree, outdegree, actcount, inhcount

import random
from datetime import datetime
random.seed(datetime.now())

import sys
networkid = sys.argv[1].strip()
N = int(sys.argv[2].strip())

from shutil import copyfile

copyfile('networkfiles/' + networkid + '.topo', 'randomnetworks/' + networkid + '/' + networkid + '_0.topo')

origflag, origin, origout, origact, originh = Get_Network_Features('randomnetworks/' + networkid + '/' + networkid + '_0.topo')

from Util_Methods import *

for i in range(N):
	Generate_Random_Networks('networkfiles/' + networkid + '.topo', 'randomnetworks/' + networkid + '/' + networkid + '_' + str(i + 1) + '.topo')
	flag, indegree, outdegree, actcount, inhcount = Get_Network_Features('randomnetworks/' + networkid + '/' + networkid + '_' + str(i + 1) + '.topo')
	valid = 1
	if flag == 1:
		valid = 0
	for node in origin:
		if origin[node] != indegree[node]:
			valid = 0
	for node in origout:
		if origout[node] != outdegree[node]:
			valid = 0
	if origact != actcount or originh != inhcount:
		valid = 0
	if valid == 0:
		print('Gavin Belson v. Peter Gregory')
