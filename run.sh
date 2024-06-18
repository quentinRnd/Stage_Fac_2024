#!/bin/bash

# Go to the script folder
cd "$(dirname "$0")"

# Get the app environment variables
source .env

./clean.sh

if [ ! -d $LOG_DIR ]; then
    mkdir -p   $LOG_DIR
fi
echo "launching process"
for (( i=0 ; i<$NUM_PROCESSEUR_SOLVE ; ++i ))
do
    
    python3 ./Modele4.py --t $NUM_PROCESSEUR_SOLVE --i $i -output="solve$i" 1>"$LOG_DIR/log_numthread_$i.log" 2>"$LOG_DIR/log_error_numthread_$i.log" &
    if (($i < $(( $NUM_PROCESSEUR_SOLVE -1 )) )); then 
        sleep 10
    fi
done
echo "all process launch waiting for them to complete"
wait
echo "all process have completed their task"
