## Cisco DHCP Reservation Creation

This Python script allows you to easily convert current DHCP leases on Cisco IOS devices to reservations.

Please note that this script is only designed to run on Cisco IOS devices.

### Usage

1. Open a command prompt/terminal and run cisco-dhcp-res.py 

2. Enter the IP of the device hosting the DHCP pool and credentials to SSH to it.

```
Enter IP of device hosting DHCP: 10.6.1.1
Username: admin
Password: ******
```

3. Select the existing DHCP pool of the target lease to be converted:

```
Current DHCP pools:

Workstations
Servers
Access_Points

Select the DHCP pool for the target lease to convert (case-sensitive): Servers
```

Note: This step of selecting the existing DHCP pool is to obtain settings (default-router, domain-name, DHCP options) that will be applied to the reservation pool.

4. Select a lease to convert from a list of current leases.

```
IP address       Client-ID/              Lease expiration        Type
                 Hardware address
10.1.1.16        0100.1234.ed33.c4       May 29 2019 05:32 PM    Automatic
10.1.1.17        0100.1234.d620.de       May 28 2019 09:16 PM    Automatic
10.1.1.18        0100.1234.a67f.80       May 29 2019 04:38 PM    Automatic

Enter the IP of the lease to convert to reservation: 10.1.1.18
```

The script will then confirm the creation of your DHCP reservation.

```
Your DHCP reservation has been created:

10.1.1.68        0140.017a.7072.e4       Infinite                Manual
```

### Requirements

-Python version 3.x

-Python module 'netmiko'

-SSH access to the Cisco device hosting the DHCP pool

