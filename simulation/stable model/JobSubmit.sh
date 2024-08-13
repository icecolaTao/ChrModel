#!/bin/bash
#SBATCH 

loc='YOUR PATH'

for ((i=1;i<=20;i=i+1))
do
	{
	let j=100
	let k=$j+533
	sed 's/y=1/'y=${i}'/g' ${loc}gro.py > ${loc}grotemp${i}.py
	sed 's/nTF=0/'nTF=${j}'/g' ${loc}grotemp${i}.py > ${loc}gro${i}.py

	sed 's/x=1/'x=${i}'/g' ${loc}top.py > ${loc}toptemp${i}.py
	sed 's/nTF=0/'nTF=${j}'/g' ${loc}toptemp${i}.py > ${loc}top${i}.py

	sed -i 's/534-683/'534-${k}'/g' ${loc}at13.dat

	python ${loc}gro${i}.py
	python ${loc}top${i}.py

	grompp_mpi -f ${loc}minim.mdp -c ${loc}${i}.gro -p ${loc}${i}.top -o ${loc}em${i}.tpr -maxwarn 600
	mdrun_mpi -v -deffnm em${i}

	grompp_mpi -f ${loc}annealing.mdp -c ${loc}em${i}.gro -p ${loc}${i}.top -o ${loc}${i}.tpr -maxwarn 600
	mdrun_mpi -s ${loc}${i}.tpr -x ${loc}${i}.xtc -g ${loc}md${i}.log -plumed ${loc}at13.dat
	echo 0 | trjconv_mpi -s ${loc}${i}.tpr -f ${loc}${i}.xtc -o ${loc}${i}.pdb

	sed 's/fn=1/'fn=${i}'/g' ${loc}platforms.py > ${loc}temp${i}.py
	sed 's/nTF=0/'nTF=${j}'/g' ${loc}temp${i}.py > ${loc}${i}.py
	python ${loc}${i}.py
	
	sed 's/fn=1/'fn=${i}'/g' ${loc}distance.py > ${loc}dis${i}.py
	sed -i 's/'nTF=0'/'nTF=${j}'/g' ${loc}dis${i}.py
	python ${loc}dis${i}.py
	} &
done
