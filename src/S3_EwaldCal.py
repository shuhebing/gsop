
import os
from pymatgen.core.structure import Structure
from pymatgen.analysis.ewald import EwaldSummation
import pandas as pd

rootdir = r'./concs'
def findfiletree(files, rootdir):
    filelist=os.listdir(rootdir)
    for file in filelist:
        filestr=rootdir+'/'+file
        if os.path.isfile(filestr):
            filename=os.path.split(filestr)[1]
            if os.path.splitext(filename)[0] == 'POSCAR':
                files.append(filestr)
        elif os.path.isdir(filestr):
            findfiletree(files,filestr)
filelist=[]
findfiletree(filelist,rootdir)
oxi_dic = {'Na':1,'B':3,'C':-2,'F':-1, 'Co':3, 'O':-2, 'Li':1}

data_S = pd.DataFrame()
print(len(filelist))
i=0
for file in filelist[:]:
    i+=1
    print('the order of this file is %d, filename is %s'%(i, file))
    structure = Structure.from_file(file)
    structure.add_oxidation_state_by_element(oxi_dic)
    matrix = EwaldSummation(structure).total_energy
    data_S[file] = ['%.5f'%matrix, '%.2f'%matrix, '%.1f'%matrix, '%.0f'%matrix,]
data_S.T.to_csv('./data/EwaldEnergy.csv')
print('Calculation Complished')





