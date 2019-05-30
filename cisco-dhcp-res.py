from netmiko import ConnectHandler
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
pools=dhcp_srv_conn.send_command("show ip dhcp pool | inc Pool")
pool_names=[]
for line in pools.splitlines():
	line=line.lstrip("Pool ")
	line=line.rstrip(" :")
	pool_names.append(line)
print("\nCurrent DHCP pools: \n")
for pool in pool_names:
	print(pool)
target_pool=input("\nSelect the DHCP pool for the target lease to convert (this pool's options will be applied to reservation: ")
while target_pool not in pool_names:
	target_pool=input("Select the DHCP pool for the target lease to convert: ")
pool_config=dhcp_srv_conn.send_command("show run | sec "+target_pool)
pool_settings=[]
for line in pool_config.splitlines():
	if line.startswith("  "):
		pool_settings.append(line)
leases=dhcp_srv_conn.send_command("show ip dhcp bin")
print(leases+"\n")
lease_dict={}
for line in leases.splitlines():
	if re.match(ip_regex,line):
		ip=re.search(ip_regex,line)
		#ips.append(ip.group())
		client_id=re.search(clientid_regex,line)
		x={ip.group():client_id.group()}
		#client_ids.append(client_id)
		lease_dict.update(x)
reservation=input("Enter the IP of the lease to convert to reservation: ")
while reservation not in lease_dict.keys():
	reservation=input("Invalid selection. Enter the IP of the lease to convert to reservation: ")
dhcp_srv_conn.send_command("clear ip dhcp bin "+reservation)
dhcp_srv_conn.send_config_set("ip dhcp pool "+reservation+"\nhost "+reservation+"\nclient-id "+lease_dict[reservation])
for x in pool_settings:
	dhcp_srv_conn.send_config_set("ip dhcp pool "+reservation+"\n"+x)
print("\nYour DHCP reservation has been created:\n")
print(dhcp_srv_conn.send_command("show ip dhcp bind "+reservation+" | inc "+reservation+"_"))
