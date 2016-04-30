#!/bin/bash

source ../env.sh || exit 1

make || { echo "Failed to build"; exit 1; }

DDIR="dump"

rm -f nohup.out
rm -rf ${DDIR}

mkdir ${DDIR}

setsid nohup ./pstree &
root_pid=$!

${CRIU} dump -D ${DDIR} -t ${root_pid} || { echo "Failed to dump"; kill -9 -${root_pid}; exit 1; }
${CRIU} restore -D ${DDIR} --leave-stopped -d || { echo "Failed to restore"; exit 1; }

./tree_checker.py ${root_pid}

if [ $? -eq 0 ]; then
    echo "PASS"
    kill -9 -${root_pid}
else
    echo "FAIL"
    kill -9 -${root_pid}
    exit 1
fi
