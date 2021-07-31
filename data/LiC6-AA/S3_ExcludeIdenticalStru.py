# encoding: utf-8

import sys
import itertools
import os
import time
from operator import itemgetter
import xlwt
import math
import pymatgen as pmg
import pymatgen.analysis.structure_matcher as pmgmach
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from pymatgen.core.sites import PeriodicSite
from click.core import batch
import time
from collections import defaultdict



oxi_dic = {'Na':1,'B':3,'C':-2,'F':-1, 'Co':3, 'O':-2, 'Li':1, 'La':3, 'Ti':4}
#rootdir = os.getcwd()
def findfiletree(files, rootdir):
    filelist=os.listdir(rootdir)
    for file in filelist:
        filestr=rootdir+'/'+file
        if os.path.isfile(filestr):
            filename=os.path.split(filestr)[1]
            if os.path.splitext(filename)[0][:6] == 'POSCAR':
                files.append(filestr)
        elif os.path.isdir(filestr):
            findfiletree(files,filestr)




def write_group(group_keys, group_values):
    group_size = len(group_keys) 

    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('sheet 1')
    rows = 0
    for group_counter in range(group_size):
        sheet.write(rows, 0, group_keys[group_counter])
        sheet.write(rows, 1, group_counter)
        rows = rows + 1

        cols = len(group_values[group_counter])
        for values_counter in range(cols):
            sheet.write(rows, 0, group_values[group_counter][values_counter])
            sheet.write(rows, 1, group_counter)
            rows = rows + 1

    excelTime = time.strftime("%Y%m%d-%H%M%S")
    workbook.save('result_cifs' + excelTime + '.xls')


class Weighted_Union_Find:
    def __init__(self, edges=[['1', '1']]):

        self.father = {}
        self.size = {}
        self.node = []
        self.group = defaultdict(list)

        for i in range(len(edges)):
            self.node.append(edges[i][0])
            self.node.append(edges[i][1])
        self.node = set(tuple(self.node))
        self.node = list(self.node)
        self.count = len(self.node)
        for data in self.node:
            self.size[data] = 1
            self.father[data] = data

    def isConnected(self, p, q):
        t = self.node
        if p not in t:
            self.node.append(p)
            self.size[p] = 1
            self.father[p] = p
        if q not in t:
            self.node.append(q)
            self.size[q] = 1
            self.father[q] = q

        return self.find(p) == self.find(q)

    def find(self, p):
        while self.father[p] != p:
            self.father[p] = self.father[self.father[p]]  
            p = self.father[p]

        return p

    def union(self, p, q):
        pAncestor = self.find(p)
        qAncestor = self.find(q)
        if pAncestor == qAncestor:
            return
        if self.size[pAncestor] < self.size[qAncestor]:  
            self.father[pAncestor] = qAncestor
            self.size[qAncestor] += self.size[pAncestor]
        else:
            self.father[qAncestor] = pAncestor
            self.size[pAncestor] += self.size[qAncestor]
        self.count -= 1

    def getcount(self):
        return self.count


# batch read .cif filename
def batch_read_filename(
    path, filetype):  # collect the filename under the dir of path,the default value of filetype is '.cif'
    filenames = []
    for i in os.listdir(path):
        if filetype in i:
            # filenames.append(i.replace(filetype,''))
            filenames.append(i)
    return filenames


# write the result to excel file
def write_to_excel(results):  # to write the results into the excel
    # create a workbook,encoding:utf-8
    workbook = xlwt.Workbook(encoding='utf-8')
    # create a sheet
    sheet = workbook.add_sheet('sheet 1')
    # create style
    style = xlwt.XFStyle()
    # create and set font
    font = xlwt.Font()
    font.name = 'Times New Roman'
    # add font to style
    style.font = font
    # create alignment and set to center
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    # add alignment to style
    style.alignment = alignment
    # create another style style1
    style1 = xlwt.XFStyle()
    # create and set font1
    font1 = xlwt.Font()
    font1.name = 'Times New Roman'

    font1.bold = True
    style1.font = font1
    style1.alignment = alignment

    # set column name
    columnNames = ['filename1', 'filename2', 'isSimilar']
    # get column number
    columns = len(columnNames)
    # set column width and name
    for i in range(columns):
        sheet.col(i).width = 6000
        sheet.write(0, i, columnNames[i], style1)

    # set row number
    rows = len(results)
    # insert data
    for i in range(0, rows):
        for j in range(columns):
            sheet.write(i + 1, j, results[i].split('\t')[j], style)
    # save excel
    excelTime = time.strftime("%Y%m%d-%H%M%S")
    workbook.save('structure_matcher_result-' + excelTime + '.xls')


# ---------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------
def struc_matcher(infile, ltol=0.2, stol=1, atol=5):  # IGNORE:C0111
    try:
        path = infile
        filetype = ".cif"

        data_list = []
        composi = []
        all_true_file = []

        filenames = []
        findfiletree(filenames,path)
        print(filenames[:4])
        all_time = 0
        UF = Weighted_Union_Find()

        filenames = filenames
        for Counter in range(len(filenames)):

            infile = filenames[
                Counter]  # inflile is the real route of file
            print(Counter, infile, ' begin')
            try:  # read the first file
                stru = pmg.Structure.from_file(infile)

                data_list.append(stru)
            except:
                print('wrong1: ', infile)
                filenames[Counter] = '0'
                continue

        filenames = filter(lambda a: a != '0', filenames)
        list_filename = list(filenames)
        lenF = len(list_filename)
        #print(list_filename)

        pcomp = pmgmach.StructureMatcher(
            primitive_cell=False,
            attempt_supercell=True,
            ltol=0.1,
            stol=0.1,
            angle_tol=atol
        )  # tol=tolerance  primitive_cell attemppt_supercell???

        # processed_data_list=pcomp._process_species(data_list)        #preprocess

        def s_hash(s):  # itertools.groupby filter key/func
            x = pcomp._comparator.get_hash(s.composition)
            return x

        for i in range(lenF):
            _composition_after_hash = str(s_hash(data_list[i])).split('comp:')
            composi.append(_composition_after_hash)

        filename1_stru2_com3 = list(zip(list_filename, data_list, composi))

        t_begin = time.time()

        sorted_s_list = sorted(filename1_stru2_com3, key=lambda x: x[2])

        for k, g in itertools.groupby(sorted_s_list, key=lambda x: x[
                2]):  # k is the index ; g is a group which is grouped by k

            # set the para of comparing
            g = list(g)

            for FirstCounter in range(len(g)):

                stru1 = g[FirstCounter][1]
                infile1 = g[FirstCounter][0]
                for SecondCounter in range(FirstCounter + 1, len(g)):
                    stru2 = g[SecondCounter][1]
                    infile2 = g[SecondCounter][0]

                    res_ = str(pcomp.fit(stru1, stru2))

                    if res_ == 'True':
                        all_true_file.append(infile1)
                        all_true_file.append(infile2)

                        if UF.isConnected(infile1,
                                          infile2):  
                            pass

                        else: 
                            UF.union(infile1, infile2)

        all_true_file = list(set(all_true_file))
        # print(len(all_true_file))
        for filexi in all_true_file:
            rootx = UF.find(filexi)
            if rootx != filexi:
                UF.group[rootx].append(filexi)

        t_end = time.time()
        all_time = all_time + t_end - t_begin

        print('total time：', all_time)

        #        write_to_excel(results)
        group_keys = tuple(UF.group.keys())
        group_values = tuple(UF.group.values(
        ))  #    print(group_keys)        print(group_values)
        write_group(group_keys, group_values)

        print("Matcher completed!")

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0


# ----------------------------------------------------------------------------------------------------------------

# def del_similar():
#     path=input('please input the path(must be a directory) of the data to be processed\n')
#     struc_matcher(path)
#

# del_similar()
t_begin2 = time.time()
struc_matcher( r'../concs')
t_end2 = time.time()
print("all time with write", t_end2 - t_begin2)






