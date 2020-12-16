#!/bin/bash
for i in {1..100}
do
echo "1 11" | ./krand
python3 try.py >> test/alg/DDT_x_11_1_krand
done
