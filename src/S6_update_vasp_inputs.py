import numpy as np
import os
from pymatgen.core.structure import Structure
import shutil

kpoints_limit = int(input("input kpoints_limit (kpoints_limit // length of lattice vector) "))
rootdir = r'./vasp_calculation_dir'   #POSCAR所在路径

kpt_path = r'./vasp_inputs/KPOINTS'
incarc_path = r'./vasp_inputs/INCAR-c'
incar_path  = r'./vasp_inputs/INCAR'
potca_path  = r'./vasp_inputs/POTCAR'
vasp_path   = r'./vasp_inputs/vasp.lsf'

update_kpt   = 1
update_incar = 1
update_potcr = 1
update_lsf = 1
update_pos = False

def kpts_update(kpt_path, stru, new_path):
    kpt_content = open(kpt_path).readlines()
    strip = [i.rstrip() for i in kpt_content]
    if strip[2] == 'G':
        new_line = []
        abc = list(stru.lattice.abc)
        for j in abc:
            if j > kpoints_limit:
                new_line.append(kpoints_limit)
            else:
                new_line.append(j)
        new_line1 = []
        for k in new_line:
            temp = str('%.0f'%(kpoints_limit / k))
            new_line1.append(temp)
        new_line2 = '  '.join(new_line1)

        print(abc)
        print(new_line2)
    kpt_content[3] = new_line2 + '  \n'

    with open(new_path + '/KPOINTS', 'w') as f2:
        for ll in kpt_content:
            f2.write(ll)
    return

def findfiletree(files, rootdir):
    filelist=os.listdir(rootdir)
    for file in filelist:
        filestr=rootdir+'/'+file
        if os.path.isfile(filestr):
            filename=os.path.split(filestr)[1]
            if filename.startswith('POSCAR'):
                files.append(filestr)
        elif os.path.isdir(filestr):
            findfiletree(files,filestr)

filelist=[]
findfiletree(filelist,rootdir)

print(len(filelist))
print(np.array(filelist[:5]))

for i in filelist:
    stru = Structure.from_file(i)
    path = os.path.split(i)[0]

    if update_incar:
        shutil.copyfile(incar_path,  path + '/INCAR')
		
    if update_kpt:
        new_kpt_content = kpts_update(kpt_path, stru, path)

    if update_potcr:
        shutil.copyfile(potca_path, path + '/POTCAR')

    if update_lsf:
        shutil.copyfile(vasp_path, path + '/vasp.lsf')

    if update_pos:
        shutil.copyfile(i, path + './POSCAR')
    






