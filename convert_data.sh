#!/bin/bash

#==========input path==========
main_path='/Users/s147g785/Desktop/sp21/2mring_results/2m_ring_surf_func/cool_1_surf_func'

#==========output path=========
data_path='/Users/s147g785/Desktop/sp21/2mring_results/2m_ring_surf_func/cool_1_surf_func/sal_temp'  #where data will be stored

#==========because there are 100 different files==========
for num in {1..100}
do
    fold=$(printf '%03d' $num)
    mkdir $data_path/surf_$fold
    cd $data_path/surf_$fold
    #awk '{NR}END{for(i = NR/2; i > NR/2; ++i) print x[i]}' $main_path/surf_$fold/relax.xyz > $data_path/surf_$fold/relax.xyz
    awk -v h=$(echo $(wc -l <$main_path/surf_$fold/relax.xyz)) 'NR>h/2' $main_path/surf_$fold/relax.xyz > $data_path/surf_$fold/relax.xyz

    #====if you need the first half then put "{exit}1" after NR>h/2===
    #=================================================================
done



    
	    
