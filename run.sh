#!/bin/bash

# Go to the script folder
cd "$(dirname "$0")"

# Get the app environment variables
source .env



if [ ! -d $LOG_DIR ]; then
    mkdir -p   $LOG_DIR
fi
for (( i=0 ; i<$NUM_PROCESSEUR_SOLVE ; ++i ))
do
    python3 ./Modele1.py -t $NUM_PROCESSEUR_SOLVE -i $i 1>"$LOG_DIR/log_numthread_$i.txt" 2>"$LOG_DIR/log_error_numthread_$i.txt" &
done
