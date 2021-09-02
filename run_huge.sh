#!/bin/bash
IFS_copy="$IFS"

WRK=${1} # full path to work directory
SCRATCH=${2} # full path to scratch diredtory
RESULT_DIR=${3} # full path to result directory
PROG=${4} # full path to executable

# Define basis sets and methods 
basis="aug-cc-pVDZ"
method="ccs lowmem-cc2"

for f in geometries/huge/*.xyz
do
   molecule=$(basename $f .xyz)
   
   # extract geometry
   IFS=
   geometry=$(tail -n +3 $f | cut -f 1-4 )

   # general input for given geometry   
   cp eT_es.inp "${molecule}.inp"
   echo $geometry >> "${molecule}.inp"
   echo "end geometry" >> "${molecule}.inp" 
  
   IFS="$IFS_copy"
   for b in $basis
   do
     # insert basis set
     sed -e "s/basis-x/$b/" "${molecule}.inp" > "${molecule}_${b}.inp"
     for m in $method
     do
        # insert method 
        sed -e "s/method-x/$m/" "${molecule}_${b}.inp" > "${molecule}_${b}_${m}.inp"

        # run calculation
        echo "Running $m calculation on $molecule/$b"
        
        cp $PROG/eT $SCRATCH/eT
        mv ${molecule}_${b}_${m}.inp $SCRATCH/eT.inp

	cd $SCRATCH
        time ./eT -omp $THREADS
        for r in eT.*
        do
           cp $r $RESULT_DIR/${molecule}_${b}_${m}.$r
        done
        cd $WORK

     done
     rm ${molecule}_${b}.inp
   done
   rm ${molecule}.inp
done
