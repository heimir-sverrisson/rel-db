#!/bin/bash
#
./gen-users.py users.csv 1000
for i in 0 1 2 3
do
  ./gen-table.py users.csv ${i} | dot -Tpng -o d${i}.png
#  sips -r 90 d${i}.png
done
