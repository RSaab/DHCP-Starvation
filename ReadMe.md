##Setup:

Computer 1: wlan0 --> Fake AP with DHCP Server
	    	wlan1 --> Snort for detecting DHCP Starvation and ICMP Signalling
	   		wlan1 --> launch DHCP Starvation attack
___________________________________
Detection and signaling Details:

Snort: 
	Snort is used to detect large number of DHCP DISCOVER and DHCP REQUEST messages
	alerts are reported to an alert text file to be monitored by final.py

final.py:
	watches the alert file of snort for changes
	once it is modified, it reads all leased IPs from the DHCP server, and then
	it calls a function from ping.py
	based on the result it identifies the user as legitimate or malicious

ping.py:
	an implimentation of ping in python used to ping users

---------------------------------------------------------------------------------------

## Run Snort
snort -dev -l alerts -i wlan1 -c ./snort_dhcp.conf

## run ICMP counter
 python count_ICMP.py

## Run detection an signaling
python ICMP_Signaling_Detection.py


#use scapy to reply to icmp requests
   # scapy

    Welcome to Scapy (2.1.0)

    >>> ip=IP()

    >>> ip.src='192.168.0.255'

    >>> ip.dst='192.168.0.1'

    >>> ip.display

    <bound method IP.display of <IP src=192.168.0.255 dst=192.168.0.1 |>>

    >>> icmp=ICMP()

    >>> icmp.type=8

    >>> icmp.code=0

    >>> icmp.display

    <bound method ICMP.display of <ICMP  type=echo-request code=0 |>>

    >>> send(ip/icmp)
