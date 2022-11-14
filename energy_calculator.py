# -----------------------------------------------------------                                                                                         
# calculates the hydrolysis energies for a given set of slabs
#                                                                                                                                                    
# (C) 2022 Sahan Godahewa (Thompson Lab)                                                                                                              
# email (sahangodahewa@ku.edu)                                                                                                                       
# -----------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.spatial import distance
import fnmatch,os
from os import path

func_path_left="/home/s147g785/work/fa21/reaxff_joyce/minimizations/funced_sil/data_with_reaxff_equi/results_cg/bks/method7/2015_rff/4th_ring/oh_left"
func_path_right="/home/s147g785/work/fa21/reaxff_joyce/minimizations/funced_sil/data_with_reaxff_equi/results_cg/bks/method7/2015_rff/4th_ring/oh_right"
unfunc_path="/home/s147g785/work/fa21/reaxff_joyce/minimizations/unfunc_sil/data_with_reaxff_equil/results_cg/dmax_0.001/2015_rff"
water_path="/home/s147g785/work/fa21/reaxff_joyce/minimizations/water/water_cg/2015_rff/energy_final.dat"

func_dir=[]
file_missing_in = []
left_func_energies = []
right_func_energies = []
unfunc_energies = []
pattern = 'min_energy_*.dat'
match_unfunc_set = set()
non_match_unfunc_set = set()
match_set_left = set()
non_match_set_left = set()
match_set_right = set()
non_match_set_right = set()
match_unfunc=[]


#1. === Read through the "FUNCTIONALIZED" energy files ===
for root, dirs, files in os.walk(func_path_left):
    if fnmatch.filter(files, pattern):
        match_set_left.add(root)
    else: 
        non_match_set_left.add(root)    

non_match_sort_left=sorted(non_match_set_left, key=lambda x: x[1:])
match_sort_left=sorted(match_set_left, key=lambda x: x[1:])

print("first element of funced list",match_sort_left[1])

#print("match sort", match_sort)

#2. === Save the "FUNCTIONALIZED" slab energies to another list
for i_path in match_sort_left:
    for root, dirs, files in os.walk(i_path):
        for fil in files:
            if fil.startswith('min_energy_'):
                #print(fil)
                f = open(os.path.join(i_path,fil), "r")
                left_func_energies.append(float(f.readline()))
                
print("left oriented enegies",left_func_energies)

#print(len(unfunc_energies))
#print(len(left_func_energies))

#1.1 === Read through the "FUNCTIONALIZED" energy files ===                                                                                           
for root, dirs, files in os.walk(func_path_right):
    if fnmatch.filter(files, pattern):
        match_set_right.add(root)
    else:
        non_match_set_right.add(root)

non_match_sort_right=sorted(non_match_set_right, key=lambda x: x[1:])
match_sort_right=sorted(match_set_right, key=lambda x: x[1:])

print("first element of funced list",match_sort_right[1])

#print("match sort", match_sort)                                                                                                                      

#2.1 === Save the "FUNCTIONALIZED" slab energies to another list                                                                                      
for i_path in match_sort_right:
    for root, dirs, files in os.walk(i_path):
        for fil in files:
            if fil.startswith('min_energy_'):
                #print(fil)                                                                                                                           
                f = open(os.path.join(i_path,fil), "r")
                right_func_energies.append(float(f.readline()))

print("right oriented enegies",right_func_energies)                                                                                                   


#print(len(unfunc_energies))                                                                                                                          
#print(len(right_func_energies))                                                                                                                       
length=len(left_func_energies)
length_right=len(right_func_energies)

if length != length_right:
    print("lengths are different")


#3. === Read through the "UNFUNCTIONALIZED" energy files and match with step 2 results
for i_path in match_sort_left:
    x = str(i_path)[-3:]
    #print('x is',x)
    for root, dirs, files in os.walk(unfunc_path):
        for subd in dirs:
            if x in subd:
                print('dirs are',subd)
                match_unfunc_set.add(os.path.join(root,subd))#.append(dirs)

match_unfunc_sort=sorted(match_unfunc_set, key=lambda x: x[1:])
#print(match_unfunc_sort)

#4. === save the "UNFUNCTIONALIZED" slab energies to a list                                                                                           
for i_path in match_unfunc_sort:   #somehow the actual numbering starts from the index = 1                                                        
    #print(i_path)                                                                                                                                    
    for root, dirs, files in os.walk(i_path):                                                                                                         
        for fil in files:
            if fil.startswith('min_energy_'): 
                f1 = open(os.path.join(i_path,fil), "r")
                unfunc_energies.append(float(f1.readline()))
                
#print(unfunc_energies)

#5. === Save the water energies to another list
water_energies=np.genfromtxt(water_path, usecols=(0)).tolist()
water_final=water_energies[0:length]
#print(water_final)
#print(len(water_final))


#6. === calculate the HYDROLYSIS ENEGY
hydrolysis_energy_left=[]
for i,j,k in zip(left_func_energies,unfunc_energies,water_final):
    hy_en_left = round((i-(j+k)),5)
    hydrolysis_energy_left.append(hy_en_left)
    
#print(hydrolysis_energy_left)


hydrolysis_energy_right=[]
for i,j,k in zip(right_func_energies,unfunc_energies,water_final):
    hy_en_right = round((i-(j+k)),5)
    hydrolysis_energy_right.append(hy_en_right)

#print(hydrolysis_energy)


#7. === Find the minimum from the two lists
min_en=[]
for ele in zip(hydrolysis_energy_left,hydrolysis_energy_right):
    min_en.append(min(ele))


#8. print the four values to an external file
data_left=np.column_stack((water_final,unfunc_energies,left_func_energies,hydrolysis_energy_left,hydrolysis_energy_right,min_en))
np.savetxt('./2M_kul_4th_ring_HE.dat',data_left,fmt='%16.5e')
