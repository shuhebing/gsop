import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def formula(file_list, conc_list, enegy_list, conc_multi, Li1_energy, Li_content, Li0_energy, L0_content):
    conc_list = [float(kk) for kk in conc_list]
    Li1_energy = float(Li1_energy); Li0_energy = float(Li0_energy)
    assert len(conc_list) == len(enegy_list) == len(file_list)
    hull_list = []; conc1_list = []; file1_list = []
    for i, ene in enumerate(enegy_list):
        conc = conc_list[i] * conc_multi
        x = conc
        y = Li_content
        z = L0_content
        A = (z-x)/(z-y)
        B = (x-y)/(z-y)
        hull = float(ene) - float(A* Li1_energy) -float(B*Li0_energy)   #LixC6=ALiyC6+BLizC6
        if hull < 0.025:
            #print("conc = %03f, hull=%03f, file = %s"%(conc, hull, file_list[i]))
            file1_list.append(file_list[i])
            hull_list.append(hull)
            conc1_list.append(conc)
    return file1_list, conc1_list, hull_list

sys1_ready = int(input("data of system1 is ready: 1-ready, 0-not ready: "))
if sys1_ready:
    path_sys1  = 'data/sys01.csv'
    sys1_Li1 = float(input("system1 with concentration 1:  "))  #-58.9138
    sys1_Li0 = float(input("system1 with concentration 0:  "))  #-55.9725
sys2_ready = int(input("data of system2 is ready: 1-ready, 0-not ready: "))
if sys2_ready:
    path_sys2  = 'data/sys02.csv'
    sys2_Li1 = float(input("system2 with concentration 1:  "))  #-57.5269
    sys2_Li0 = float(input("system2 with concentration 0:  "))  #-56.0250

hull_out   = 0
hull1_name = "sys1_hull.csv"
hull2_name = "sys2_hull.csv"

fig_out    = 1
fig_name   = "data/hull.png"

if sys1_ready:
    sys1 = pd.read_csv(path_sys1,  index_col = [0])[["concention", "unit_dft"]]
    sys1_valid = sys1[sys1["unit_dft"]!="None"]
    
    name1 = sys1_valid.index
    conc1 = sys1_valid.values[:,0]
    form1 = sys1_valid.values[:,1]
    name1_new = ["Li0"] + name1.tolist() + ["Li"]
    conc1_new = ["0.0"] + conc1.tolist() + ["1.0"]
    form1_new = [sys1_Li0] + form1.tolist() + [sys1_Li1]
    conc1_new = [float(i) for i in conc1_new]
    form1_new = [float(i) for i in form1_new]
    x1_files, x1_hull, y1_hull = formula(name1_new, conc1_new, form1_new, 1, sys1_Li1, 1.0 , sys1_Li0, 0.0)

if sys2_ready:
    sys2 = pd.read_csv(path_sys2,  index_col = [0])[["concention", "unit_dft"]]
    sys2_valid = sys2[sys2["unit_dft"]!="None"]
    name2 = sys2_valid.index
    conc2 = sys2_valid.values[:,0]
    form2 = sys2_valid.values[:,1]
    name2_new = ["Li0"] + name2.tolist() + ["Li"]
    conc2_new = ["0"] + conc2.tolist() + ["1.0"]
    form2_new = [sys2_Li0] + form2.tolist() + [sys2_Li1]
    conc2_new = [float(i) for i in conc2_new]
    form2_new = [float(i) for i in form2_new]
    x2_files, x2_hull, y2_hull = formula(name2_new, conc2_new, form2_new,  1, sys1_Li1, 1.0 ,sys1_Li0, 0.0)
    
if hull_out:
    assert len(x1_files) == len(x1_hull) == len(y1_hull) 
    pd.DataFrame(list(zip(x1_hull, y1_hull)), index=x1_files, columns=["conc", "hull"]).to_csv(hull1_name)
    pd.DataFrame(list(zip(x2_hull, y2_hull)), index=x2_files, columns=["conc", "hull"]).to_csv(hull2_name)

plt.figure(figsize=(7.5,5))
if sys1_ready:
    plt.scatter(x1_hull, y1_hull, c = 'green', s=150,  marker='^', alpha = 0.8, label="AA stacking")
if sys2_ready:
    plt.scatter(x2_hull, y2_hull, c = 'blue',  s=200,  marker='*', label="ABBA stacking")

plt.rcParams['font.sans-serif']=['Times New Roman']   # 用黑体显示中文
plt.rcParams['axes.unicode_minus']=False     # 正常显示负号
plt.xticks((np.arange(0, 11, 2)/10)[:], fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel("Li${_x}$C${_6}$", fontsize=20)
plt.ylabel("Formation Energy (eV/f.u.)",fontsize=20)

plt.legend(fontsize=20)

if fig_out:
    plt.savefig(fig_name, dpi=1200)
plt.show()












