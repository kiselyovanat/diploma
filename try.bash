#!/bin/bash
for i in {1..50}
do
echo "1 12" | ./krand
python3 try.py >> test/alg/DDT_x_12_4_krand
done
