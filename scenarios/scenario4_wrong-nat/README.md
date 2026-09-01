Fault:
The NAT configuration on R1 was incorrect, preventing traffic from the
internal network from being translated correctly for communication with
the external network.

Symptom:
The internal PC was unable to communicate correctly with the Internet
test server.

Investigation:
The NAT configuration was checked using:
show ip nat translations
show ip nat statistics

Fix:
The EMPLOYEE VLAN subinterface Gig0/1.10 was configured as a NAT inside interface

Verification:
NAT translations were checked again using show ip nat translations and the IP was perfectly translated.

Automated validation:
Python checker detected the missing inside interface for nat and returned [FAIL].
After correction, it returned [PASS].