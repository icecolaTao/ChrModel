#!/bin/bash
#SBATCH 

loc='YOUR PATH'

let j=100
let k=$j+533

sed -i 's/nTF=0/'nTF=${j}'/g' ${loc}tfMtop7.py
sed -i 's/534-683/'534-${k}'/g' ${loc}tfAt13.dat

python ${loc}tfMtop7.py

for ((i=1;i<=60;i=i+1))
do
	{
	sed 's/y=1/'y=${i}'/g' ${loc}gro.py > ${loc}gro${i}.py
	sed -i 's/nTF=0/'nTF=${j}'/g' ${loc}gro${i}.py

	python ${loc}gro${i}.py
	
	grompp_mpi -f ${loc}minim.mdp -c ${loc}${i}.gro -p ${loc}7.top -o ${loc}em${i}.tpr -maxwarn 600
	mdrun_mpi -v -deffnm em${i} -table ${loc}ptable.xvg -tablep ${loc}btable.xvg

	grompp_mpi -f ${loc}tfMannealing.mdp -c ${loc}em${i}.gro -p ${loc}7.top -o ${loc}${i}.tpr -maxwarn 600
	mdrun_mpi -s ${loc}${i}.tpr -x ${loc}${i}.xtc -g ${loc}md${i}.log -table ${loc}ptable.xvg -tablep ${loc}btable.xvg -plumed ${loc}tfAt13.dat
	echo 0 | trjconv_mpi -s ${loc}${i}.tpr -f ${loc}${i}.xtc -o ${loc}${i}.pdb

	sed 's/fn=1/'fn=${i}'/g' ${loc}platforms.py > ${loc}p${i}.py
	sed -i 's/nTF=0/'nTF=${j}'/g' ${loc}p${i}.py
	python ${loc}p${i}.py
	
	sed 's/fn=1/'fn=${i}'/g' ${loc}distance.py > ${loc}dis${i}.py
	sed -i 's/'nTF=0'/'nTF=${j}'/g' ${loc}dis${i}.py
	python ${loc}dis${i}.py
	} &
done

wait

endTime=`date +%s`
echo "Total time:" $(($endTime-$beginTime)) "seconds"
