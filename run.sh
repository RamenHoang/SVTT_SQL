#!/bin/bash
if [ "$UID" -eq 0 -o "$EUID" -eq 0 ]; then
    cd SVTT_SQL
    nohup python3 run.py &
else
    echo "Please run with sudo"
fi