# --------------------------------------------------------------
# Demonstrates correlation b/w hydrolysis_en vs params of unfunc
#
# (C) 2022 Sahan Godahewa (Thompson Lab)
# email (sahangodahewa@ku.edu)
# --------------------------------------------------------------

# --------------------------------------------------------------
# The most important to know about this code is that this code 
# takes the ring from ringfile and takes in the corresponding 
# atoms from the siofile(sio.xyz). So make sure to change the
# line that reads the ringfile line in ringfile file.
# --------------------------------------------------------------

import numpy as np
import os
import time
import matplotlib.pyplot as plt
import shutil

start_time = time.time()

# -------- variable definition
dirs = ['sio_dir', 'ring_dir', 'func_dir', 'func_xyz_dir', 'sisi_distances', 'oo_distances', 'siOsi_angles1', 'siOsi_angles2', 'si1_ch', 'si2_ch', 'o1_ch', 'o2_ch', 'si1_o2','si2_o2']
data = {}
for var in dirs:
    data[var] = []

natoms = 576
file_name = 'min_energy_'
dir_name = 'surf_'
fthree= 'three'
file_type = '.dat'
left_silanols = []
right_silanols = []
nsi = 192
no = 384

# ---Hydrolysis Energies -----------
Energies = "/home/s147g785/work/fa21/reaxff_joyce/2M_minimizations/funced_sil/data_with_reaxff_equi/results_cg/bks/method7/2015_rff/1st_ring/2M_kulkarni_1st_ring_HE.dat"
Energy_path = '/home/s147g785/work/fa21/reaxff_joyce/2M_minimizations/funced_sil/data_with_reaxff_equi/results_cg/bks/method7/2015_rff/1st_ring'

hydrolysis_energies = np.genfromtxt(Energies, usecols=(4)).tolist()
print(hydrolysis_energies)

# Open the file and read its content into a list of lines 
with open(Energies) as file:
    lines = file.readlines()

result = []
# ----- Loop through the lines, split each line into columns, and extract the second and third columns
# ----- and append them to a list called result
for line in lines:
    columns = line.strip().split()
    result.append([columns[2], columns[3]])

#------ Loop through each pair and save the orientation of the minimum as left or right so we know which directory to look
left_or_right = []
for pair in result:
    if float(pair[0]) < float(pair[1]):
        left_or_right.append('left')
    else:
        left_or_right.append('right')

print(left_or_right)
# ------ Get the extension at the end of the directory, E.g. _001, _002, _003, etc. and save it to an array called ext
ext = []
for i in range (1,101):
        if i<10:
                ext.append("00"+str(i))
        elif i<100:
                ext.append("0"+str(i))
        else:
                ext.append(str(i))
#print(ext)                                                                                                                                         

nfiles = len(ext)

# ------- Regardless of whether the minimum value is in the left or right, here we save the extensions based on the left and right orientation to two arrays/
# ------- called extensions_left and extensions_right and they will be of the same LENGTH                                                                                 

func_path_left = '/home/s147g785/work/fa21/reaxff_joyce/2M_minimizations/funced_sil/data_with_reaxff_equi/results_cg/bks/method7/2015_rff/1st_ring/oh_left'
func_path_right = '/home/s147g785/work/fa21/reaxff_joyce/2M_minimizations/funced_sil/data_with_reaxff_equi/results_cg/bks/method7/2015_rff/1st_ring/oh_right'
path_name = '/home/s147g785/work/fa21/reaxff_joyce/2M_minimizations/funced_sil/data_with_reaxff_equi/results_cg/bks/method7/2015_rff/1st_ring/oh_' 
extensions_left = []
extensions_right = []
for i in range(0, nfiles):
    file_path_check1 = os.path.join(func_path_left,dir_name+ext[i],file_name+ext[i]+file_type)
    if os.path.exists(file_path_check1):
        extensions_left.append(ext[i])
    file_path_check2 = os.path.join(func_path_right,dir_name+ext[i],file_name+ext[i]+file_type)
    if os.path.exists(file_path_check2):
        extensions_right.append(ext[i])

print(extensions_left)
print(extensions_right)

sio_name = 'sio.xyz'
two_ring_name = 'two.dat'
charges = 'charges.xyz'


direct_sort2,direct_sort3 = [], []
if (len(extensions_left) != len(extensions_right)):
    raise ValueError('The number of files in the left and right directories are not the same')
else:
    #We need only one array out of the two arrays because their lengths are the same
    for index,orient in zip(extensions_left,left_or_right):
        path_to_get1 = os.path.join(path_name+orient,dir_name+index,sio_name)
        path_to_get2 = os.path.join(path_name+orient,dir_name+index,two_ring_name)
        direct_sort2.append(path_to_get1)
        direct_sort3.append(path_to_get2)
    
# ------ here we consider only one of the arrays out of extensions_left and _right because the charge values are from the unfunctionalized site
charge_path='/home/s147g785/work/fa21/reaxff_joyce/unfunc_sil/data_with_reaxff_equil/cool_1kps/results_cg/dmax_0.001/2015_rff/'

direct_sort2_ch = []
for index in extensions_left:
    path_to_get3 = os.path.join(charge_path,dir_name+index,charges)
    direct_sort2_ch.append(path_to_get3)

#print(direct_sort2_ch)

# --------Define paths so to write the new files to -------------------

unfunc_path_ring = '/home/s147g785/work/fa21/reaxff_joyce/2M_minimizations/funced_sil/data_with_reaxff_equi/results_cg/bks/grp_grp/unfunc/2M/1st_ring/ring'
unfunc_path_rest = '/home/s147g785/work/fa21/reaxff_joyce/2M_minimizations/funced_sil/data_with_reaxff_equi/results_cg/bks/grp_grp/unfunc/2M/1st_ring/rest'

# ------We select the vectors and calculate the parameters ------------
#count = 0
for ring_path, sio_path in zip(direct_sort3, direct_sort2):
    print(sio_path)
    sio_file = np.genfromtxt(sio_path,skip_header=2,dtype=None,encoding='ascii').tolist()
    count = sio_path.split('/')[-2].split('_')[-1] #because the first split outputted 'surf_001'
    print(count)
    #formatted_count = str(count).zfill(3)
    #print(sio_path)
    
    
    # ----- Ring File ---------
    # -----this picks out the indices of the ring indices and put them in 
    #
    #with open(ring_path, 'r') as fp:
    ringfile = np.genfromtxt(ring_path,max_rows=1,usecols=(0,1,2,3),dtype=None).tolist()
    #print(ringfile)

    just_ring = [] #saves the ring atom coordinates
    for i in ringfile:
        just_ring.append(sio_file[i-1])
    
    os.makedirs("{}/surf_{}".format(unfunc_path_ring,count))

    with open("{}/surf_{}/ring_cords_{}.xyz".format(unfunc_path_ring,count,count), "w+") as file1:
        file1.write(str(4)+"\n\n")
        for line in just_ring:
            atom, x, y, z = line
            if atom == 'Si':
                atom_value = 1
            elif atom == 'O':
                atom_value = 2
            file1.write("{} {} {} {}\n".format(atom_value, x, y, z))


    os.makedirs("{}/surf_{}".format(unfunc_path_rest, count))
    
    with open("{}/surf_{}/frame_cords_{}.xyz".format(unfunc_path_rest,count,count), "w+") as file2:
        file2.write(str(572)+"\n\n")
        for i,ele in enumerate(sio_file):
            if i+1 not in ringfile:
                atom,x,y,z = ele
                if atom == 'Si':
                    atom_val = 1
                elif atom == 'O':
                    atom_val = 2
                file2.write("{} {} {} {}\n".format(atom_val, x, y, z))
        


