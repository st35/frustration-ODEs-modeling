import random
from datetime import datetime
random.seed(datetime.now())

import sys
sys.path.append('../code')
networkid = sys.argv[1].strip()
N = int(sys.argv[2].strip())

from shutil import copyfile

copyfile('inputfiles/' + networkid + '.topo', 'randomnetworks/' + networkid + '/' + networkid + '_0.topo')

from Util_Methods import *

for i in range(N):
	Generate_Random_Networks('inputfiles/' + networkid + '.topo', 'randomnetworks/' + networkid + '/' + networkid + '_' + str(i + 1) + '.topo')
