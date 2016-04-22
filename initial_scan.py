import re
import sys
import copy
import csv

info_dict = {}

def set_dictionary(filename):
	headers = list()

	for i in range(8):
		headers.append(0)
	ip = ""

	nmap_file = open(filename + ".nmap", 'r')

	with open(filename + ".nmap", 'r') as my_file:
		nmap_file = my_file.read()

		nmap_file_split = nmap_file.split('\n')
		total_lines = len(nmap_file_split)-4
  
		for i in range(0, total_lines):
			line = nmap_file_split[i]
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
		#print(info_dict)

	#del info_dict['']
	return info_dict

# Convert dictionary to CSV file
def create_csv():
	output_csv = 'IP,Hostname,Port Number,Port Transport,Port Status,Port Service,Mac Address,Device Type,Running,OS CPE,OS Details,Network Distance\n'

	for ip in info_dict:

		headers = info_dict[ip]

		hostname, services, mac_address, device_type, running, os_cpe, os_details, network_distance =\
		(headers[0], set_service_info(headers[1]), headers[2], headers[3], 
			headers[4], headers[5], headers[6], headers[7])


		services_split = services.split(' ')
		for service in services_split:
			if service != '':
				service_info = service.split(',')

				port_num, port_transport, port_status, port_service =\
				(service_info[0], service_info[1], service_info[2], service_info[3])

				output_csv += ip + ',' + hostname + ',' + port_num + ','
				output_csv += port_transport + ',' + port_status + ',' + port_service + ','
				output_csv += mac_address + ',' + device_type + ',' + running + ','
				output_csv += os_cpe + ',' + os_details + ',' + network_distance + '\n'

	return output_csv

def write_to_csv(csv_output):
	line_split = csv_output.split('\n')

	csv_file = open('something.csv','w')

	for line in line_split:
		csv_file.write(line + '\n')

	csv_file.close()
			

def set_service_info(services):
	# print 'service info'

	all_services, port_num, port_transport, port_status, port_service = '', '', '', '', ''

	for service in services:
		port_num_split = service.split('/')
		port_num = port_num_split[0]

		port_info_split = port_num_split[1].split(' ')

		port_info = []
		for info in port_info_split:
			if (info != ''):
				port_info.append(info)

		port_transport, port_status, port_service = port_info[0], port_info[1], port_info[2]

		all_services += port_num + ',' + port_transport + ',' + port_status + ',' + port_service + ' '

		port_info = []

	return all_services

if __name__ == "__main__":
	set_dictionary("initial_scan_test.txt")
	csv_output = create_csv()
	write_to_csv(csv_output)

