#!/bin/bash
for i in {1..10}
do
echo "1 4" | ./krand
python3 latsage.py >> test/newlat/lat42
done
