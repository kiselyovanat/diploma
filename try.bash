#!/bin/bash
for i in {1..10}
do
echo "1 3" | ./krand
python3 try.py >> test/alg/DDT_x_3_krand
done
