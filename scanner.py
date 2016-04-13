#!/user/bin/env/ python

import csv
import os
import sys 

#### RUN NMAP SCAN ####

filename = sys.argv[1]
networkrange = sys.argv[2]

command = 'nmap -O -oA ' + filename + ' ' + networkrange 
print command


## RUN NMAP COMMAND ##
os.system(command)

## PARSE THROUGH OUTPUT FILE ##


