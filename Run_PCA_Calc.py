import sys
networkname = sys.argv[1]

from Util_Methods import Steadystates_PCA

with open('outputfiles/' + networkname + '_PCA.log', 'w') as f:
	for i in range(101):
		print(i)
		p = Steadystates_PCA('steadystates/' + networkname + '_' + str(i) + '.log', 1)
		for val in p:
			f.write(str(val) + '\t')
		f.write('\n')
