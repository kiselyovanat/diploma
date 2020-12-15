#!/bin/bash
for i in {1..10}
do
echo "1 3 1" | ./ogrf
python3 try.py >> test/alg/DDT_xi_3_2_ogrf
done
