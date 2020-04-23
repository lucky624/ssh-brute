#!/bin/bash


for (( team=1; team <= 20; team++ ))
do
	part_ip='10.70.'
	ip="$part_ip"$team".2"
	echo "$ip"
	./brute.py -i $ip -u root
	echo -e "\n\n"
done
