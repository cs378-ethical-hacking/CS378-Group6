#!/user/bin/env/ python

import csv
import os
import sys
import re
import copy
from initial_scan import *
from csv_to_html import *
from snmpwalk import *
from toPDF  import *

import argparse

#word_list = "/usr/share/john/"+ john_list
filename = ""
networkrange = ""
pw_file = ""

def run_nmap():
    print "nmap scan..."
    command = 'nmap -O -oA ' + filename + ' ' + networkrange
    print command

    ## RUN NMAP COMMAND ##
    os.system(command)


def run_services(network_dict):
    print "run services..."
    word_list = run_john(pw_file)
    print network_dict

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
                hydra = "hydra -l root -P "+ pw_file +" ssh://"+ip
                print hydra
                coutput = commands.getstatusoutput(hydra)

                if("[ERROR]" not in coutput[1]):
                    print "successful--write to file--"
                    write_to_file(ip+ "_output.txt", hydra)
                    write_to_file(ip+ "_output.txt", coutput[1])

def arg_parse():
    parser = argparse.ArgumentParser(description="Disclaimer: This is an educational project for CS378: Ethical Hacking at the University of Texas at Austin with Chris Prosise in Spring 2016. Our goal was to create a simple tool that automates some portion of the (network) assessment methodology. Tools Used: nmap, snmpwalk, finger and hydra.")

    parser.add_argument('ip', help='ip addresses required for network scanning')
    parser.add_argument('-o', action='store', dest='output_file', default="nmap_output", help='network scan output file path; by default=nmap_output')
    parser.add_argument('--password=', action='store', dest='password_file', default="./password.lst",help='password file path for bruce force')
    parser.add_argument('--pdf', action='store_true', default=False, dest='is_pdf',help='Output to PDF')
    parser.add_argument('--csv', action='store_true', default=False, dest='is_csv',help='Output to CSV')
    parser.add_argument('--html', action='store_true', default=False, dest='is_html',help='Output to HTML')
    parser.add_argument('-a', '--all', action='store_true', default=False, dest='is_all',help='Output to PDF, CSV, HTML')
    result = parser.parse_args()

    return result

def main():
    global filename
    global networkrange
    global pw_file

    # Argument parsing by default
    arg_result = arg_parse()
    filename = arg_result.output_file
    networkrange = arg_result.ip
    pw_file = arg_result.password_file

    # Run nmap, create a dictionary, and run services by default
    run_nmap()
    nmap_dict = set_dictionary(filename)
    run_services(nmap_dict)

    # Output to csv, html, pdf is optional
    if (arg_result.is_all):
        csv = create_csv()
        write_to_csv(filename, csv)
        csv_to_html(filename)

    elif (arg_result.is_csv):
        # Generate a CSV file corresponding to the NMAP scan output
        # Write the CSV to an output file
        csv = create_csv()
        write_to_csv(filename, csv)

    elif (arg_result.is_html):
        csv = create_csv()
        write_to_csv(filename, csv)

        # Use the generated CSV output file to export to HTML boostrap file
        csv_to_html(filename)

    elif (arg_result.is_pdf):
        # Output to pdf
        to_pdf(filename)
        print "pdf"



if __name__ == "__main__":
    main()
