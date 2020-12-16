#!/bin/bash
for i in {1..100}
do
echo "1 8" | ./krand
python3 try.py >> test/alg/DDT_x_8_3_krand
done
