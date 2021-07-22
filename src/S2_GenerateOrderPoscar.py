
import numpy as np
import os
from itertools import combinations
import shutil
import re
from pymatgen.core.structure import Structure

pattern = '[0-9]*[a-zA-Z]?'
num_line_idx = 6
num_space = ' '
origin_site = "Li"
line_beg = 8 
rootdir = r'./poscars'
target = './concs'

def get_2mani(mani):
        #输出每组乌科夫位置的行号以及组合情况
        pattern1 = '[0-9]*'
        mani_set = []
        for i in range(1,len(mani)):
            mani_set_temp = combinations(mani, i)
            mani_set.extend(list(mani_set_temp))
        mani_num = [re.match(pattern1, i).group() for i in mani]
        mani_num = [int(i) for i in mani_num]
        mani_num = np.cumsum(mani_num)
        mani_num = mani_num.tolist()
        mani_num[0:0] = [0]
        mani_lin = [np.arange(mani_num[i-1]+1, mani_num[i]+1).tolist()
                    for i in range(1,len(mani_num))]
        return mani_set, mani_lin
		
def write_poscar_2(data, symbol, order_):
        order_ = str('%04d'%order_)
        
        poscarname = name1+ '_'+  order_ + '_' + ''.join(symbol)
        
        poscar_path_parent = target + '/'+ '%s/%s'%(name1, poscarname)
        poscar_path_all = target + '/'+ '%s/%s/%s'%(name1, poscarname, 'POSCAR')
        
        if not os.path.exists(poscar_path_parent):
                os.makedirs(poscar_path_parent)
        print(poscar_path_parent)

        with open(poscar_path_all, 'w') as f9:
                for line in data:
                        f9.write(line)
        return poscar_path_parent      
		
def write_poscar_3(data, symbolss, order_, mmk):
        order_ = str('%04d-%03d'%(order_, mmk))
        poscarname = name1+ '_'+  order_ + '_' + '-'.join(symbolss)
        poscar_path_parent = target + '/'+ '%s/%s'%(name1, poscarname)
        poscar_path_all = target + '/'+ '%s/%s/%s'%(name1, poscarname, 'POSCAR')
        if not os.path.exists(poscar_path_parent):
            os.makedirs(poscar_path_parent)
        with open(poscar_path_all, 'w') as f9:
            for line in data:
                f9.write(line)
        return poscar_path_parent 

a = int(input("oredring of 2 elements or 3 elements: "))
if (a == 2):
    Li_La_Va = 0
elif (a == 3):
    Li_La_Va = 1
else:
    pass
if (Li_La_Va == 1):
    b = str(input("the second element except Li:"))
    substi_site = b
    assert (len(b) < 3)

filelist = []
for i in os.listdir(rootdir):
        path1 = rootdir + '/' + i
        if i.startswith('POSCAR'):
                filelist.append(path1)

for i in filelist:
        with open(i) as f:
                file1 = f.readlines()
                file_ori = np.array(file1)
        name1 = os.path.split(i)[1]
        print('==========================================================')
        print(name1)
        filename2lst = name1.split('_')
        mani_lst = re.findall(pattern, filename2lst[-1],re.I)
        mani_lst.pop()
        total_lin_num = sum([int(item[:-1]) for item in mani_lst])
        if total_lin_num % int(name1[13]) != 0: 
            raise ValueError('atom number / k value')
        total_lin_num = total_lin_num
        line_end = total_lin_num + line_beg
        label = ['o','p','q','r','s','t','u','v','w','x','y','z','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        mani_list_temp = [mani_lst[i] + label[i] for i in range(len(mani_lst))]
        mani_set, mani_lin = get_2mani(mani_list_temp)
        mani_set1, mani_lin1 = get_2mani(mani_list_temp)
        lin_combi = []
        for i in mani_set:
            lin_idx_temp = [mani_list_temp.index(j) for j in i]
            lin_idx = np.array(mani_lin)[lin_idx_temp].tolist()
            lin_idx = np.concatenate(lin_idx, axis=0)-1
            lin_idx = sorted(lin_idx)
            lin_combi.append(lin_idx)
            lin_combi_sort = sorted(lin_combi ,key=len)
        count = 0
        for i, lin_idx in enumerate(lin_combi_sort):
          if (Li_La_Va == 0):    
            file = file_ori.copy()
            num_line = file[num_line_idx]
            to_num  = num_line.lstrip().split(num_space)
            to_num[0] = str(len(lin_idx))
            new_line ='   ' + '  '.join(to_num)
            file[num_line_idx] = new_line   
            all_sites = file[line_beg:line_end]
            pat_sites = all_sites[lin_idx].tolist()
            if len(all_sites) != total_lin_num:
                raise AttributeError('索引出来的原子数和设置的原子数不等')
            file = file.tolist()
            file[line_beg:line_end] = []             
            file[line_beg:line_beg] = pat_sites       
            symbol_index = lin_combi.index(lin_idx)
            symbol = mani_set1[symbol_index]
            poscarnamex = write_poscar_2(file,symbol, i+1)
          else: 
            count = i
            symbol_index = lin_combi.index(lin_idx)
            symbol = mani_set1[symbol_index]
            total_num = sum([int(nnn[:-2]) for nnn in mani_list_temp])
            va = list(set(mani_list_temp) - set(symbol))
            va_num    = sum([int(nnn[:-2]) for nnn in va])
            if (len(symbol) > 1):
                mani_li_ti = []   
                for i in range(1,len(symbol)):
                    mani_set_temp_li_ti = combinations(symbol, i)
                    mani_li_ti.extend(list(mani_set_temp_li_ti))
                lin_combi_li_ti = []
                for i in mani_li_ti:
                    lin_idx_temp_li_ti = [mani_list_temp.index(j) for j in i]
                    lin_idx_li_ti = np.array(mani_lin)[lin_idx_temp_li_ti].tolist()
                    lin_idx_li_ti = np.concatenate(lin_idx_li_ti, axis=0)-1
                    lin_idx_li_ti = sorted(lin_idx_li_ti)
                    lin_combi_li_ti.append(lin_idx_li_ti)               
                    lin_combi_sort_li_ti = sorted(lin_combi_li_ti ,key=len)
                all_line_li_ti = np.unique(np.concatenate(lin_combi_li_ti, axis=0))
                lin_combi_ti = [list(set(all_line_li_ti)-set(mmm)) for mmm in lin_combi_li_ti]
                mix_li_num = [len(mmm) for mmm in lin_combi_li_ti]
                mix_ti_num = [len(mmm) for mmm in lin_combi_ti]
                va_num = va_num
                if len(mix_li_num) != len(mix_ti_num):
                    raise AttributeError('li = la')

                li_ti_va = []; li_ti_va_ratio = []
                for mmk in range(len(mix_li_num)):
                    file = file_ori.copy()
                    li_number = mix_li_num[mmk]
                    ti_number = mix_ti_num[mmk]
                    all_number = li_number + ti_number + va_num
                    
                    li_ration = li_number / all_number
                    ti_ration = ti_number / all_number
                    va_ration = va_num / all_number
                    La_prec = 0.005
                    if ((-La_prec) < ti_ration - (2/3 - li_ration/3) < La_prec):
                        li_ti_va.append([li_number, ti_number, va_num])
                        li_ti_va_ratio.append([li_ration, ti_ration, va_ration])
                        file[num_line_idx-1] = file[num_line_idx-1].replace(origin_site, "%s  %s  "%(origin_site, substi_site))
                        num_line = file[num_line_idx]
                        to_num  = num_line.lstrip().split(num_space)
                        to_num[0] = "%d%s%d"%(li_number, num_space ,ti_number)
                        new_line ='   ' + '  '.join(to_num)
                        file[num_line_idx] = new_line 
                        pat_li_sites = []
                        for ggg in lin_combi_li_ti[mmk]: 
                                pat_li_sites.append(file[ggg+line_beg])
                        pat_ti_sites = []
                        for ggg in lin_combi_ti[mmk]:    
                                pat_ti_sites.append(file[ggg+line_beg].replace(origin_site, substi_site))
                        all_sites = file[line_beg:line_end]
                        pat_sites = all_sites[lin_idx].tolist()

                        if len(all_sites) != total_lin_num:
                                raise AttributeError('索引出来的原子数和设置的原子数不等')
                        file = file.tolist()
                        file[line_beg:line_end] = []
                        file[line_beg:line_beg] = pat_ti_sites
                        file[line_beg:line_beg] = pat_li_sites
                        poscarnamex = write_poscar_3(file, [str(li_ration), str(ti_ration), str(va_ration)], count+1, mmk)

                if (len(li_ti_va) > 0):
                    li_ti_va = np.array(li_ti_va)
                    li_ti_va_ratio = np.array(li_ti_va_ratio)
                    print(np.array(list(zip(li_ti_va, li_ti_va_ratio))))


