#!/bin/bash
for i in {1..10}
do
echo "1 3 3" | ./ogrf
python3 try.py >> test/alg/DDT_x_3_ogrf
done
