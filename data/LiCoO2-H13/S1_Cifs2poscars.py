import os
from pymatgen.core.structure import Structure

cif_dir    = r'./cifs'
poscar_dir = "poscars"

filelist = []
for i in os.listdir(cif_dir):
    path = cif_dir + '/' + i
    if i.endswith('.cif'):
        filelist.append(path)
for i in filelist:
    print("file in converting:",i)
    name1 = os.path.splitext(os.path.split(i)[1])[0]
    name1 = 'POSCAR' + name1[3:]
    stru = Structure.from_file(i)
    angle = stru.lattice.angles
    lengh = stru.lattice.abc
    stru.to(fmt='poscar', filename='./poscars/%s'%name1)
