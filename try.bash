#!/bin/bash
for i in {1..100}
do
echo "1 7" | ./krand
python3 newAttack.py >> test/newAttack/7_4_krand
done
