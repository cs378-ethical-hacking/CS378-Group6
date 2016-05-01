#!/user/bin/env/ python

import csv
import os
import sys
import re
import copy
from initial_scan import *
from csv_to_html import *
from snmpwalk import *

#### RUN NMAP SCAN ####
filename = sys.argv[1]
networkrange = sys.argv[2]
#word_list = "/usr/share/john/"+ john_list
def run_nmap():
    print "nmap scan..."
    command = 'nmap -O -oA ' + filename + ' ' + networkrange
    print command

    ## RUN NMAP COMMAND ##
    os.system(command)


def run_services(network_dict):
    print "run services..."
    word_list = run_john("./password.lst")

    for ip in network_dict:
        print "host: " + ip
        services = network_dict[ip][1]

        if "router" in network_dict[ip][3]:
            print "run snmpwalk..."
            run_snmpwalk(ip)

        for port in services:
            if port.split("/")[0] == '79':
                print "run finger..."
                finger_service = 'finger -l @' + ip
                print finger_service
                coutput = commands.getstatusoutput(finger_service)

                if("Timeout" not in coutput):
                    print "successful--write to file--"
                    write_to_file(ip+ "_output.txt", finger_service)
                    write_to_file(ip+ "_output.txt", coutput[1])

            if port.split("/")[0] == '22':
                print "run hydra..."
                hydra = "hydra -l root -P /usr/share/john/password.lst ssh://"+ip
                print hydra
                coutput = commands.getstatusoutput(hydra)

                if("[ERROR]" not in coutput[1]):
                    print "successful--write to file--"
                    write_to_file(ip+ "_output.txt", hydra)
                    write_to_file(ip+ "_output.txt", coutput[1])



def run_john(john_list):
    word_list = john_list
    words = []
    with open(word_list, "r") as f:
        for line in f:
            words.append(line)
    return words

def main():
    run_nmap()
    nmap_dict = set_dictionary(filename)

    run_services(nmap_dict)

    # Generate a CSV file corresponding to the NMAP scan output
    csv = create_csv()

    # Write the CSV to an output file
    write_to_csv(filename, csv)

    # Use the generated CSV output file to export to HTML boostrap file
    csv_to_html(filename)

if __name__ == "__main__":
    main()
