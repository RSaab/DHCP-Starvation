import subprocess
from isc_dhcp_leases.iscdhcpleases import Lease, IscDhcpLeases
# snort -dev -l Desktop/Snort -i wlan0 -c Desktop/snort_dhcp.conf
_cmd_lst = ['snort', '-dev', '-l', 'Snort', '-i', 'wlan0', '-c', 'snort_dhcp.conf']  # sudo snort -q -A console -i eth0 -c /etc/snort/snort.conf
hostname = '192.168.1.70'
leases = None
result = None
_rpi_lst = ['python', 'attack_detection.py', hostname]            # python script that toggles RPi
_alert = 'DHCP DISCOVER'                                  # The keyword you're looking for
                                                 #  in snort output

#===============================================================================
def getHostNames():
	leases = IscDhcpLeases('/var/lib/dhcp/dhcpd.leases')
	result = leases.get()  # Returns the leases as a list of Lease objects


# Simple helper function that calls the RPi toggle script
def toggle_rpi():
	getHostNames()
	i=0
	for ip in result:
		hostname=result[i]
		subprocess.call(_rpi_lst)
		i=i+1

def try_subprocess(cmd_lst, alert, rpi_lst):
    p = subprocess.Popen(' '.join(cmd_lst), shell=True, stdout=subprocess.PIPE, bufsize=1)

    try:
		alert_file = open('/root/Desktop/Snort/alert','r')
		while True:
			alert_text = alert_file.read()
			print('hi')
			if alert in alert_text:
				print("try_subprocess() found alert: %s" % alert)
				toggle_rpi()
		alert_file.close

    except KeyboardInterrupt:   print(" Caught Ctrl+C -- killing subprocess...")
    except Exception as ex:     print ex
    finally:
        print("Cleaning up...")
        p.kill()
        print("Goodbye.")


def try_pexpect(cmd_lst, alert, rpi_lst):
    import pexpect # http://pexpect.sourceforge.net/pexpect.html

    p = pexpect.spawn(' '.join(cmd_lst))

    try:
        while True:
            p.expect(alert)     # This blocks until <alert> is found in the output of cmd_str
            print("try_pexpect() found alert: %s" % alert)
            toggle_rpi()

    except KeyboardInterrupt:   print(" Caught Ctrl+C -- killing subprocess...")
    except Exception as ex:     print ex
    finally:
        print("Cleaning up...")
        p.close(force=True)
        print("Goodbye.")



def try_pty(cmd_lst, alert, rpi_lst, MAX_READ=2048):
    import pty, os, select

    mfd, sfd = pty.openpty()

    p = subprocess.Popen(' '.join(cmd_lst), shell=True, stdout=sfd, bufsize=1)

    try:
        while True:
            rlist, _, _, = select.select([mfd], [], [])

            if rlist:
                data = os.read(mfd, MAX_READ)
                print("try_pty() read: %s" % data.strip())
                if not data:
                    print("try_pty() got EOF -- exiting")
                    break
                if alert in data:
                    print("try_pty() found alert: %s" % alert)
                    toggle_rpi()
            elif p.poll() is not None:
                print("try_pty() had subprocess end -- exiting")
                break

    except KeyboardInterrupt:   print(" Caught Ctrl+C -- killing subprocess...")
    except Exception as ex:     print ex
    finally:
        print("Cleaning up...")
        os.close(sfd)
        os.close(mfd)
        p.kill()
        print("Goodbye.")

#===============================================================================

try_subprocess(_cmd_lst, _alert, _rpi_lst)
#try_pexpect(_cmd_lst, _alert, _rpi_lst)
#try_pty(_cmd_lst, _alert, _rpi_lst)
