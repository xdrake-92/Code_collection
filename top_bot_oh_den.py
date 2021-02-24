#------------------------------------------------------------------------------------
#------------Finding the average silanol densities of top and bottom surfaces--------
#------------------------------------------------------------------------------------      
import numpy as np
import glob
import os

file=os.path.join('/home', 's147g785', 'scratch', 'slab_runs', 'cool_100_surf_func', 'surf_*', 'relax.xyz')
filenames = glob.glob(file)  #selects all the files with the name in the given directories

cout=[]
top_oh_den=[]
bot_oh_den=[]
slab_count = 100
z_total=[]
total1 = 0
total2 = 0

for lines in filenames:
    outfile = open(lines,'r')
    data = outfile.readlines()
    outfile.close()
    z_list=[]
    for f in data:
        if 'H' in f:
#            print(f)
            silanols = f
            coord = silanols.split()
            z_dir = float(coord[3])
            z_list.append(z_dir)
#            print(z_list)
            count_top=0
            count_bottom=0
            for num in z_list:
                if num>=0:
                    count_top += 1
                else:
                    count_bottom += 1
#    print(int(count_top/2))
#    print(int(count_bottom/2))
    top_oh_den.append(float(count_top/(2*(2.101554**2))))
    bot_oh_den.append(float(count_bottom/(2*(2.101554**2))))
print("density of the top: ",top_oh_den)
print("density of the bottom: ",bot_oh_den)

##----------------------------------------------------------------------                                                 ##-----average OH density and average vicinal_silanol_pair calculation--                                                 ##-------------------------------------------------------------------------  

for ele in range(0,len(top_oh_den)):                                                                                     
    total1 =  total1 + top_oh_den[ele]
    av_top_oh_den = total1/float(slab_count)
print("average top surface OH density : ",av_top_oh_den)

for ele in range(0,len(bot_oh_den)):
    total2 = total2 + bot_oh_den[ele]
    av_bot_oh_den = total2/float(slab_count)
print("average bottom surface OH density : ", av_bot_oh_den)
    
















