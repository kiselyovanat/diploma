#!/bin/bash
for i in {1..100}
do
echo "1 5" | ./krand
python3 try.py >> test/alg/DDT_x_5_3_krand
done
