import os
import commands

def run_snmpwalk(ip):
    word_list = run_john("password.lst")
    snmpwalk_public = "snmpwalk -v1 -c public " + ip
    print snmpwalk_public
    result_public = commands.getstatusoutput(snmpwalk_public)

    if('SNMP' in result_public[1]):
        print "successful--write to file--"
        write_to_file(ip+"_output.txt", snmpwalk_public)
        write_to_file(ip+"_output.txt",result_public[1])
    else:
        for word in word_list:
            if "#" not in word:
                snmpwalk_john = "snmpwalk -v1 -c " + word.rstrip() +" " + ip
                print snmpwalk_john
                coutput = commands.getstatusoutput(snmpwalk_john)

                if('SNMP' in coutput[1]):
                    print "successful--write to file--"
                    write_to_file(ip+"_output.txt", snmpwalk_john)
                    write_to_file(ip+"_output.txt", coutput[1])
                    break;

def run_john(john_list):
    words = []
    with open(john_list, "r") as f:
        for line in f:
            words.append(line)
    return words

def write_to_file(filename, output):
    f = open(filename, 'w')
    f.write(output)

def get_router_confg(host, router_name):
    cmd = "tftp " + host + " get " + router_name + "-confg"
    confg = commands.getstatusoutput(cmd)
    print confg[1]
