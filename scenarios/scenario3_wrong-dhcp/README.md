Fault:
IP address of default gateway configured for EMPLOYEE dhcp pool was incorrect

Symptom:
EMPLOYEE PC cannot reach other networks

Investigation:
The command 'show running-config | section dhcp' was used to check
the DHCP configuration and identify the incorrect default gateway
for the EMPLOYEE VLAN.

Fix:
Configured the correct IP address of default gateway for EMPLOYEE dhcp

Verification:
Connectivity was tested again using ping, and the ping succeeded with
0% packet loss.

Automated validation:
Python checker detected the wrong default-router configured for for dhcp pool
and returned [FAIL].
After correction, it returned [PASS].