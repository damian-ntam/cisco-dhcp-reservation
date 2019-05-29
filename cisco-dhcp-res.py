from netmiko import ConnectHandler
import time
import re
import getpass

ip_regex=re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
clientid_regex=re.compile(r'[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{2}')

dhcp_srv=input("Enter IP of device hosting DHCP: ")
while not re.match(ip_regex,dhcp_srv):
	dhcp_srv=input("You must enter an IP address: ")
	
username=input("Username: ")
while not username:
	username=input("Username: ")
password=getpass.getpass()
while not password:
	password=getpass.getpass()

dhcp_srv_conn=ConnectHandler(device_type='cisco_ios',host=dhcp_srv,username=username,password=password,fast_cli=False)
leases=dhcp_srv_conn.send_command("show ip dhcp bin")
print(leases+"\n")
dict={}
for line in leases.splitlines():
	if re.match(ip_regex,line):
		ip=re.search(ip_regex,line)
		#ips.append(ip.group())
		client_id=re.search(clientid_regex,line)
		x={ip.group():client_id.group()}
		#client_ids.append(client_id)
		dict.update(x)
reservation=input("Enter the IP of the lease to convert to reservation: ")
while reservation not in dict.keys():
	reservation=input("Invalid selection. Enter the IP of the lease to convert to reservation: ")
dhcp_srv_conn.send_command("clear ip dhcp bin "+reservation)
dhcp_srv_conn.send_config_set("ip dhcp pool "+reservation+"\nhost "+reservation+"\nclient-id "+dict[reservation])
print("\nYour DHCP reservation has been created:\n")
print(dhcp_srv_conn.send_command("show ip dhcp bind "+reservation+" | inc "+reservation+"_"))
