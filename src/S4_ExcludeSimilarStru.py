
import os
import numpy as np
import re
import pandas as pd
import shutil

def read_data(rootdir_):
    data = pd.read_csv(rootdir,index_col=[0],names=['a','b','c','d'])
    data = data['a']
    print(data.values.shape)
    energy = data.values.ravel().tolist()[1:]
    file = data.index.values.tolist()[1:]
    return file, energy

def zip_file_eng(files, energys):
    file_ = []
    for i,file in enumerate(files):
        #设定精度
        file_.append([file, float('%.3f'%energys[i])])        
    return file_

def group_sort(file_eng_):
    file_eng_.sort(key = lambda x: x[1])
    return file_eng_

def group_filter(sort_data):
    sort_data = np.array(sort_data)
    new_data = []
    label = np.array(sort_data[:,1])
    x, index, fd = np.unique(label, return_index=True, return_inverse=True)
    b = sort_data[index]
    for j in b:
        new_data.append(j.tolist())
    return new_data, fd

def set_path(fil_eng):
    fil_eng = np.array(fil_eng)
    path_set = []
    poscar_subpath = fil_eng[:,0]
    file_orig = poscar_subpath
    poscar_path = ['./uniqk'+ i[7:] for i in poscar_subpath]
    if not (len(poscar_path) == len(fil_eng[:,1])):
        raise ValueError('长度不等') 
    path_set = zip(poscar_path, file_orig ,fil_eng[:,1])
    path_set = np.array(list(path_set))
    return path_set

def groupby_conc(path_sets):
    j = 0
    concs = []
    for i, path in enumerate(path_sets):
        poscarname = os.path.split(os.path.split(path[0])[0])[1]
        name_split = poscarname.split('_')
        full_sites = name_split[-3]; part_sites = name_split[-1]
        full_count = sum([int(k) for k in  filter(None, re.findall('[0-9]*', full_sites))])
        part_count = sum([int(k) for k in  filter(None, re.findall('[0-9]*', part_sites))])
        new_dir = path[0][:8] +  str('%.3f'%(part_count / full_count)) + path[0][7:]
        concs.append(str('%.3f'%(part_count / full_count)))
        new_path = os.path.split(new_dir)[0]
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        if True:
            shutil.copyfile(path[1], new_dir)
    return concs

if __name__ == '__main__':
    rootdir = r'./data/EwaldEnergy.csv'
    file, energy = read_data(rootdir)
    file_eng = zip_file_eng(file, energy)
    file_eng_sort = group_sort(file_eng)
    file_eng_uniq, inv_idx = group_filter(file_eng_sort)
    path_set = set_path(file_eng_uniq)
    concs = groupby_conc(path_set)
    print('  总长度：\n', len(file_eng_sort))
    print('筛后长度：\n', len(file_eng_uniq))


