import numpy as np
import os
import shutil

rootdir = r'./uniqk'  
target  = 'vasp_calculation_dir'
def findfiletree(files, rootdir):
    #找到rootdir下所有poscar,返回路径列表filelist
    filelist=os.listdir(rootdir)
    for file in filelist:
        filestr=rootdir+'/'+file
        if os.path.isfile(filestr):
            filename=os.path.split(filestr)[1]
            if filename=='POSCAR':
                files.append(filestr)
        elif os.path.isdir(filestr):
            findfiletree(files,filestr)
filelist=[]
findfiletree(filelist,rootdir)
print(len(filelist))
print(np.array(filelist[:5]))

for num, i in enumerate(filelist):
    path = os.path.split(i)[0]
    new_name  = os.path.split(path)[1]
    new_name1 = str('%03d'%(num+1)) +str(new_name)
    new_dir = "./%s/%s"%(target, new_name1)
    shutil.copytree(path, new_dir)

    

    
    






