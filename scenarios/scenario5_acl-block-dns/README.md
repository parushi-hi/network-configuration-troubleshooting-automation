Fault:
The 'BLOCK_DNS' extended ACL was configured to block DNS traffic from the internal network.

Symptom:
The PC could reach the Internet test server using its IP address, but it could not resolve the domain name 'smartbranch.com'.

Investigation:
The command 'show ip access-list' revealed that the 'BLOCK_DNS' ACL was denying DNS traffic to the DNS server.

Fix:
Removed the 'BLOCK_DNS' ACL from R1 using
'no ip access-list extended BLOCK_DNS'