#!/bin/bash


main_path='/Users/s147g785/Desktop/vmd/slab_runs/cool_1000_surf_fun'
data_path='/Users/s147g785/Desktop/vmd/relax_1000'

for num in {1..100}
do
    fold=$(printf '%03d' $num)

    mkdir $data_path/surf_$fold
    cd $data_path/surf_$fold
    
    cp $main_path/surf_$fold/relax.xyz .
done
