#!/bin/bash
#SBATCH

for ((i=61;i<=120;i=i+1))
do
	{ 
    sed 's/y=1/'y=${i}'/g' ${loc}gro.py > ${loc}gro${i}.py
    python ${loc}gro${i}.py

	grompp_mpi -f ${loc}mep.mdp -c ${loc}${i}.gro -p ${loc}1.top -o ${loc}${i}.tpr -maxwarn 600
	mdrun_mpi -s ${loc}${i}.tpr -x ${loc}${i}.xtc -g ${loc}md${i}.log -table ${loc}ptable.xvg -tablep ${loc}btable.xvg -plumed ${loc}at13.dat
	echo 0 | trjconv_mpi -s ${loc}${i}.tpr -f ${loc}${i}.xtc -o ${loc}${i}.pdb

	} &
done

wait

sleep 20m

python preplat.py

for ((i=1;i<=120;i=i+1))
do
 	{ 

     sed 's/y=1/'y=${i}'/g' ${loc}platforms.py > ${loc}platforms${i}.py
     python platforms${i}.py

 	} &
done

wait

python extract.py

matlab < computeb1.m
