#!/bin/bash
host=$1
for port in {1..65535}; do
    (bash -c "echo > /dev/tcp/$host/$port") && echo "$port port is open" & sleep 1 ; kill -9 $! > /dev/null 2>&1
done
echo "Done"

