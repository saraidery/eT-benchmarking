#!/bin/bash

WRK=
SCRATCH=
RESULT_DIR=
PROG=
THREADS=

sh run_small.sh $WRK $SCRATCH $RESULT_DIR $PROG $THREADS
sh run_medium.sh $WRK $SCRATCH $RESULT_DIR $PROG $THREADS
sh run_large.sh $WRK $SCRATCH $RESULT_DIR $PROG $THREADS
sh run_huge.sh $WRK $SCRATCH $RESULT_DIR $PROG $THREADS
