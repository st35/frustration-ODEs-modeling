import sys

networkname = sys.argv[1].strip()
networkid = int(sys.argv[2].strip())

import os
from pathlib import Path
from shutil import copy
import subprocess
from Util_Methods import *

RACIPE_Folder = './RACIPE_Output/RUN_' + str(networkid)

Path(RACIPE_Folder).mkdir()
copy('../../randomnetworks/' + networkname + '/' + networkname + '_' + str(networkid) + '.topo', RACIPE_Folder)
copy('../../code/RACIPE', RACIPE_Folder)

RACIPE_Output = subprocess.run(['./RACIPE', networkname + '_' + str(networkid) + '.topo', '-num_paras', '1000'], cwd = RACIPE_Folder, capture_output = True, text = True)
with open(RACIPE_Folder + '/slurm.out', 'w') as f:
	f.write(RACIPE_Output.stdout)
Process_RACIPE_Output(RACIPE_Folder + '/' + networkname + '_' + str(networkid))

steadystates = Write_Steady_States(RACIPE_Folder, networkname + '_' + str(networkid), 'steadystates', networkname + '_' + str(networkid) + '.log')
