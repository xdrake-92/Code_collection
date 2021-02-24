import numpy as np
import glob
import os

file=os.path.join('/home', 's147g785', 'scratch', 'slab_runs', 'cool_100_surf_func', 'surf_*', 'relax.xyz')
filenames = glob.glob(file)  #selects all the files with the name in the given directories

cout=[]
oh_den=[]
total1 = 0
total2 = 0
slab_count = 100

for lines in filenames:
    outfile = open(lines,'r')
    data = outfile.readlines()
    outfile.close()
    count=0
    for f in data:
        if 'H' in f:
            count += 1
            A=int(count/4) #gives us the number of vicinal silanol pairs
    cout.append(A)
#print(cout)

print("***Slabs with the total number of ring counts***")

count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
for ele in cout:
    if ele==1:
        count1 += 1
    elif ele==2:
        count2 += 1
    elif ele==3:
        count3 += 1
    elif ele==4:
        count4 += 1
    elif ele==5:
        count5 += 1
    elif ele==6:
        count6 += 1
    else:
        count7+=1
print("number of slabs with 1 vicinal silanol pair: ", count1)
print("number of slabs with 2 vicinal silanol pairs: ", count2)
print("number of slabs with 3 vicinal silanol pairs: ", count3)
print("number of slabs with 4 vicinal silanol pairs: ", count4)
print("number of slabs with 5 vicinal silanol pairs: ", count5)
print("number of slabs with 6 vicinal silanol pairs: ", count6)
print("number of slabs with 7 vicinal silanol pairs: ", count7)
        

