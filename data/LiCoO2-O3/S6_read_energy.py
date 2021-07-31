import os
import pandas as pd
import re
from pymatgen.core.structure import Structure

#dir for first principle calculation
rootdir = r'vasp_calculation_dir'
#energy per unit cell : atom / atom_unit 
print("supercell size is determined by 
       (number of framwork atom)/(number of framwork atom per unit)")
atom      = str(input("symbol of framwork atom:"))
atom_unit = int(input("number of framwork atom:"))
#OUTCAR reached accuracy
pattern = r'reached required accuracy - stopping structural energy minimisation'
plott = 0
savefig = 0
#csv output
csv_out = 1
csv_name = "data/sys01"
migr = "Li"

def spg_ana(struct):
    sg = struct.get_space_group_info(symprec=i)
    return symm_dataset

def findfiletree(files, rootdir):
    filelist=os.listdir(rootdir)
    for file in filelist:
        filestr=rootdir+'/'+file
        if os.path.isfile(filestr):
            filename=os.path.split(filestr)[1]
            if os.path.splitext(filename)[0]=='OSZICAR':
                files.append(filestr)
        elif os.path.isdir(filestr):
            findfiletree(files,filestr)
filelist=[]
findfiletree(filelist,rootdir)

cols = ["spg","outcar_idx", "tot_dft", "concention", "multi", "unit_dft"]
#print(np.array(filelist))
data_S  = pd.DataFrame(index = cols)
data_S1 = pd.DataFrame(index = cols)    

for file in filelist:
    print();print(file)
    try:
        poscar = file[:-7] + 'POSCAR'
        contcar= file[:-7] + 'CONTCAR'
        stru = Structure.from_file(contcar)
        #Li concentration
        conc = '%.3f'%( len(stru.indices_from_symbol(migr))/ (len(stru.indices_from_symbol(atom)))/atom_unit)
        #supercell size
        multi = len(stru.indices_from_symbol(atom)) / atom_unit
        #symmetry
        symm_dataset = spg_ana(stru)
        spnum=symm_dataset["number"]
        print('spacegroup number:\n',spnum)
        #whether calculate finished
        outcar = file[:-7] + 'OUTCAR'
        with open(outcar) as foutcar:
            out = foutcar.read()
        indicator = re.search(pattern, out).group()
        if indicator == pattern:
            outcar_idx = "outcar correct"
        else:
            outcar_idx = "---"
        print(indicator)
        #total energy from OSZICAR
        with open(file) as f:
            data = f.readlines()
            print(data[-1])
            data_ = data[-1]
            data_ = data_[5:22]
            data__ = float(data_[3] + '0' + data_[4:])

        if data_.startswith('F'):
            data_S1[file] = [spnum, outcar_idx, data__, conc, multi, data__/multi]
            data_S[file]  = [spnum, outcar_idx, data__, conc, multi, data__/multi]
        else:
            data_S[file]  = [spnum, outcar_idx, 'None', conc, multi, 'None']
    except AttributeError as e:
        print(e,'\n')
        outcar_idx = "--"
        data_S[file] = [spnum, e, 'None',  conc, multi,  'None']
        continue
    except ValueError as e1:
        data_S[file] = ["None", e1, 'None',  'None', 'None',  'None']
        print(e1,'\n')
        continue
    except NameError as e2:
        print(e2,'\n')
        continue
    except IndexError as e3:
        print(e3,'\n')
        continue
    except FileNotFoundError as e4:
        print(e4,'\n')
        continue

data_S = data_S.T
data_S =  data_S.sort_values(by=["concention", "unit_dft"])
if csv_out:
    data_S.to_csv('%s.csv'%csv_name) 
print('Game Over')














