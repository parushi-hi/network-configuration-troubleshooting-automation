Fault:
VLAN 30 was missing from the allowed VLAN list on the trunk interface
GigabitEthernet0/2 of SW1.

Symptom:
GUEST (VLAN 20) PC cannot reach other networks and its default gateway

Investigation:
'show interface trunk' revealed allowed vlans on interface Gig0/2

Fix:
Allowed vlan 20 on trunk interface Gig0/2

Verification:
Ping succeeded with 0% packet loss.

Automated validation:
Python checker detected the missing VLAN and returned [FAIL].
After correction, it returned [PASS].