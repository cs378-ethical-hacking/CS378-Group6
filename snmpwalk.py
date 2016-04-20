import os
import commands
network_dict = {'10.202.208.2': ['router.asus.com ', ['53/tcp open  domain', '80/tcp open  http', '161/tcp open snmp'], 'asdfsadfsaf', 'asdf asdfasdf', 'sdf 2.6.X', 'cpe:asdfsafsdf', 'asdfsadf', 'asdfas'], '10.202.208.1': ['router.asus.com ', ['53/tcp open  domain', '80/tcp open  http'], '10:BF:48:D3:93:B8 (Asustek Computer)', 'general purpose', 'Linux 2.6.X', 'cpe:/o:linux:linux_kernel:2.6', 'Linux 2.6.8 - 2.6.30', '1 hop']}

#network_dict.contains(service)

def main():
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

main()