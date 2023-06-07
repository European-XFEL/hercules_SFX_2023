#!/bin/bash

PROPOSAL=700000
RUNS=(30 299)

FINDXFEL_PATH=`which findxfel`
EXTRADATA_PATH=`which extra-data-make-virtual-cxi`

for RUN in ${RUNS[@]}; do
    DATA_PATH=`$FINDXFEL_PATH $PROPOSAL $RUN --proc`
    RUN_STR=`printf %04d ${RUN}`

    $EXTRADATA_PATH $DATA_PATH \
        -o p${PROPOSAL}_r${RUN_STR}_proc.cxi \
        --fill-value data 0.0 \
        --fill-value mask 0xffff
done

