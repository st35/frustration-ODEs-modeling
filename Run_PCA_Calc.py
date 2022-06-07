import sys
networkname = sys.argv[1]
numnets = int(sys.argv[2])

from Util_Methods import Steadystates_PCA

with open('outputfiles/' + networkname + '_PCA.log', 'w') as f:
	for i in range(numnets):
		print(i)
		p = Steadystates_PCA('steadystates/' + networkname + '_' + str(i) + '.log', 1)
		if networkname == 'PNASLarge':
			for i in range(100):
				f.write(str(p[i]) + '\t')
		else:
			for val in p:
				f.write(str(val) + ' ')
		f.write('\n')
