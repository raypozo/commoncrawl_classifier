import re

res = []

with open("compressed_name.txt") as file:
	for line in file: 
		res = res + line.split()

res_len = len(res)
for i in range(4):
	print res[i*res_len/4: (i+1)*res_len/4] 

		# print (res[-1].split(".")[1], res[4])