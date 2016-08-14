import os
import sys

hostname = sys.argv[1] #example
response = os.system("ping -c 1 " + hostname)
f=open('User_Classifications.txt', 'w')

def callback():
	#and then check the response...
	if response == 0:
		f.write('Host ' + hostname + ' is malicious')	
		print ('Host ' + hostname + ' is malicious')	
	else:
		f.write('Host ' + hostname + ' is legitimate')
		print ('Host ' + hostname + ' is legitimate')

