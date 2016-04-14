import re
import sys
import copy

info_dict = {}
headers = list()

for i in range(8):
	headers.append(0)
ip = ""

nmap_file = open('initial_scan_test.txt', 'r')

with open('initial_scan_test.txt', 'r') as my_file:
	nmap_file = my_file.read()

	nmap_file_split = nmap_file.split('\n')
	total_lines = len(nmap_file_split)

	for i in range(0, total_lines):
		line = nmap_file_split[i]
		if 'Nmap scan report for ' in line:
			line_split = line.split('Nmap scan report for ')
			ip = line_split[1]
			ip_split = ip.split("(")
			hostname = ip_split[0]
			ip = ip_split[1][:-1]
			# print(hostname)
			# print(ip)
			headers[0] = hostname
		
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
	print(info_dict)


