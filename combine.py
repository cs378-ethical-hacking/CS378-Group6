#!/user/bin/env/ python

import csv
import os
import sys
import re
import copy

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


def parse_nmap():
    info_dict = {}
    headers = list()

    for i in range(8):
        if (i == 1):
            headers.append([])
        else:
            headers.append(0)
    ip = ""

    nmap_file = open(filename + ".nmap", 'r')

    with open(filename + ".nmap", 'r') as my_file:
        nmap_file = my_file.read()

        nmap_file_split = nmap_file.split('\n')
        total_lines = len(nmap_file_split)-4                                # 


        for i in range(0, total_lines):
            line = nmap_file_split[i]
            print line
            if 'Nmap scan report for ' in line:
                line_split = line.split('Nmap scan report for ')
                ip = line_split[1]
                if("(" in ip):
                    ip_split = ip.split("(")
                    hostname = ip_split[0]
                    ip = ip_split[1][:-1]
                else:
                    ip = ip
                    hostname = ""
                #print hostname
                #print ip
                headers[0] = hostname
                #print "header: " , headers[0]
            
            elif 'PORT' in line:
                services = []
                while ':' not in nmap_file_split[i+1]:
                    service = nmap_file_split[i+1]
                    # print(nmap_file_split[i+1])
                    services.append(service)
                    i = i + 1
                headers[1] = services
                #print headers[1]

            elif "MAC Address: " in line:
                line_split = line.split("MAC Address: ")
                mac_address = line_split[1]
                # print("MAC Address: " + mac_address)
                if (headers != ""):
                    headers[2] = mac_address
                else:
                    headers[2] = ""
                # print(headers)

            elif "Device type: " in line:
                line_split = line.split("Device type: ")
                device_type = line_split[1]
                # print("Device type: " + device_type)
                headers[3] = device_type
                # print(headers)

            elif "Running: " in line:
                line_split = line.split("Running: ")
                running = line_split[1]
                # print("Running: " + running)
                headers[4] = running
                # print(headers)

            elif "OS CPE: " in line:
                line_split = line.split("OS CPE: ")
                os_cpe = line_split[1]
                # print("OS CPE: " + os_cpe)
                headers[5] = os_cpe
                # print(headers)

            elif "OS details: " in line:
                line_split = line.split("OS details: ")
                os_details = line_split[1]
                # print("OS details: " + os_details)
                headers[6] = os_details
                # print(headers)

            elif "Network Distance: " in line:
                line_split = line.split("Network Distance: ")
                network_distance = line_split[1]
                # print("Network Distance: " + network_distance)
                headers[7] = network_distance
                # print(headers)

            elif line == '':
                tempHead = copy.deepcopy(headers)
                # print (tempHead, headers)
                info_dict[ip] = tempHead

                for i in range(len(headers)):
                    headers[i] = 0
            info_dict[ip] = headers
    del info_dict['']
    #print info_dict
    return info_dict

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
    nmap_dict = parse_nmap()
    print nmap_dict
    run_services(nmap_dict)

main()
