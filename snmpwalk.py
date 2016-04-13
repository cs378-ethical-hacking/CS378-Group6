network_dict = {ip: { [0, services[53, 80], 2, 3, 4, 5 ]}}

#network_dict.contains(service)

word_list = run_john("password.lst")
for ip in network_dict:
    services = network_dict[ip][1]
    for port in services:
        if port == '161':
            snmpwalk_public = "snmpwalk -v1 -c public " + ip + " > tmp/snmpwalk.tmp"
            os.system(snmpwalk_public)

            for word in word_list:
                snmpwalk_john = "snmpwalk -v1 -c " + word +" " + ip
                os.system(snmpwalk_john)



def run_john(john_list):
    word_list = "/usr/share/john/"+ john_list
    words = []
    with open(word_list, "r") as f:
        for line in f:
            array.append(line)
    return words
