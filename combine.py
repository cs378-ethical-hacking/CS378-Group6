#!/user/bin/env/ python

import csv
import os
import sys
import re
import copy
from initial_scan import set_dictionary 

#### RUN NMAP SCAN ####
filename = sys.argv[1]
networkrange = sys.argv[2]

def run_nmap():

    command = 'nmap -O -oA ' + filename + ' ' + networkrange 
    print command
    #coutput = commands.getstatusoutput(command)

    ## RUN NMAP COMMAND ##
    os.system(command)

    ## PARSE THROUGH OUTPUT FILE ##

def run_services(network_dict):
    word_list = run_john("password.lst")
    for ip in network_dict:
        services = network_dict[ip][1]
        
        for port in services:
            if port.split("/")[0] == '161':
                snmpwalk_public = "snmpwalk -v1 -c public " + ip
                print snmpwalk_public
                coutput = commands.getstatusoutput(snmpwalk_public)
                
                if("Timeout" not in coutput[1]):
                    print "successful--do something--"
                else:
                    for word in word_list:
                        if "#" not in word:
                            snmpwalk_john = "snmpwalk -v1 -c " + word.rstrip() +" " + ip
                            coutput = commands.getstatusoutput(snmpwalk_john)
                            if("Timeout" not in coutput[1]):
                                print "successful--do something--"
                                break;
        
            

def run_john(john_list):
    #word_list = "/usr/share/john/"+ john_list
    word_list = "./"+ john_list
    words = []
    with open(word_list, "r") as f:
        for line in f:
            words.append(line)
    return words

def main():
    run_nmap()
    nmap_dict = set_dictionary(filename)
    print nmap_dict
    run_services(nmap_dict)

main()
