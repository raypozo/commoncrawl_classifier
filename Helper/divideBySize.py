import re

with open("size.txt") as file:
	for line in file: 
		res = line.split()
		print (res[-1].split(".")[1], res[4])