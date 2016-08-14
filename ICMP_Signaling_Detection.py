import os
import sys
from isc_dhcp_leases.iscdhcpleases import Lease, IscDhcpLeases
import time
import contextlib
import watchdog.observers
from watchdog.observers import Observer
from watchdog.observers.api import EventEmitter
from watchdog.events import FileSystemEventHandler
import ping
from random import randint
import count_ICMP
import pickle


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
		observer.pause()
		print('ALERT DETECTED\nSignaling Clients\n')
		callback()
		observer.resume()


class PausingObserver(Observer):
    def dispatch_events(self, *args, **kwargs):
        if not getattr(self, '_is_paused', False):
            super(PausingObserver, self).dispatch_events(*args, **kwargs)

    def pause(self):
        self._is_paused = True

    def resume(self):
        time.sleep(self.timeout)  # allow interim events to be queued
        self.event_queue.queue.clear()
        self._is_paused = False

    @contextlib.contextmanager
    def ignore_events(self):
        self.pause()
        yield
        self.resume()

def callback():
	leases = IscDhcpLeases('/var/lib/dhcp/dhcpd.leases')
	result = leases.get()  # Returns the leases as a list of Lease objects
	i=0
	j=0
	attacker=False
	for ip in result:
		hostname = result[i].ip
		print('Pinging '+hostname)
		rnd_num = randint(1,5)
		print ('Sending %d requests' % rnd_num)
		while (j<rnd_num):
			response = ping.verbose_ping(hostname, 2, 1)
			print (response)
			j=j+1
		time.sleep(11)
		fp = open('ICMP_count.pkl', 'r')
		ICMP_count = pickle.load(fp)
		fp.close()
		tmp = ICMP_count/2
		print('Received %d replies' % tmp)	
		j=0
		f = open('User_Classifications.txt', 'a')
		#count number of replies
		# if requests = replies --> all legitimate
		if rnd_num == tmp:
			if attacker==True:
				f.write('Cleint ' + hostname + ' is malicious\n')
				print ('Cleint ' + hostname + ' is malicious\n')
			else:
				f.write('Cleint ' + hostname + ' is legitimate\n')
				print ('Cleint ' + hostname + ' is legitimate\n')
		elif tmp < rnd_num: # if replies < requests --> client is malicious
			f.write('Cleint ' + hostname + ' is malicious\n')	
			print ('Cleint ' + hostname + ' is malicious\n')
		else: # if replies > requests --> malicious clients exists
			attacker=True
			f.write('Cleint ' + hostname + ' legitimate but malicious cleints exist\n')	
			print ('Cleint ' + hostname + ' legitimate but malicious cleints exist\n')
		i=i+1

	
if __name__ == "__main__":
	fp = open('ICMP_count.pkl', 'r')
	ICMP_count = pickle.load(fp)
	event_handler = MyHandler()
	observer = PausingObserver()
	observer.schedule(event_handler, path='Alerts', recursive=False)
	observer.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()

