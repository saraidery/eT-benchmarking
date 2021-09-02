#!/bin/bash

WRK=
SCRATCH=
RESULT_DIR=
PROG=

sh run_small.sh $WRK $SCRATCH $RESULT_DIR $PROG
sh run_medium.sh $WRK $SCRATCH $RESULT_DIR $PROG
sh run_large.sh $WRK $SCRATCH $RESULT_DIR $PROG
sh run_huge.sh $WRK $SCRATCH $RESULT_DIR $PROG
