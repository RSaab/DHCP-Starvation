from scapy.all import *
import pickle
ICMP_count = 0

def count():
	
	while (True):
		ICMP_count = 0
		pkts = sniff(filter="icmp", timeout =10,count=100)
		for packet in pkts:
			if packet.getlayer(ICMP) is not None:
				if  str(packet.getlayer(ICMP).type) == "0": #type 0 = reply | type 8 = request
					print('src: ' + packet[IP].src +' || dst: '+ packet[IP].dst)
					ICMP_count =ICMP_count + 1
					print(ICMP_count)
			fp = open("ICMP_count.pkl","wb")
			pickle.dump(ICMP_count, fp)
			fp.close()

if __name__ == "__main__":
	ICMP_count=0
	fp = open("ICMP_count.pkl","wb")
	pickle.dump(ICMP_count, fp)
	fp.close()
	count()
