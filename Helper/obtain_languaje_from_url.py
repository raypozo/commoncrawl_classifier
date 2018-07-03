import sys,re

line = sys.argv[1]
option = int(sys.argv[2])

if option == 1:
    m = re.search('/(\\w+)wiki/',line.strip())
    if m:
        print m.group(1)
if option == 2:
    m = re.search('https://dumps.wikimedia.org/(.*)$',line.strip())
    if m:
        print m.group(1)