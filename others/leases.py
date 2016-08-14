from isc_dhcp_leases.iscdhcpleases import Lease, IscDhcpLeases

leases = IscDhcpLeases('/var/lib/dhcp/dhcpd.leases')
result = leases.get()  # Returns the leases as a list of Lease objects

i=0
for ip in result:
	print result[i].ip
	i=i+1
#leases.get_current()  # Returns only the currently valid dhcp leases as dict
                      # The key of the dict is the device mac address and the
                      # Value is a Lease object
