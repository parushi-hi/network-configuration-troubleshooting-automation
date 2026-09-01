# Network Configuration & Troubleshooting Automation

I designed and configured a small network in Cisco Packet Tracer. I set up
VLANs, DHCP, trunking, NAT, ACLs, and SSH-based management, then
intentionally broke parts of the configuration, troubleshot the faults, and
wrote a Python script to check the configuration automatically.

## What's in the network

| VLAN | Name       | Subnet          |
|------|------------|-----------------|
| 10   | Employee   | 192.168.10.0/24 |
| 20   | Guest      | 192.168.20.0/24 |
| 30   | Server     | 192.168.30.0/24 |
| 99   | Management | 192.168.99.0/24 |

- R1 (edge router), an ISP router, 2 switches (SW1, SW2), a few PCs, and an external test server
- Inter-VLAN routing on R1 (router-on-a-stick)
- DHCP for the Employee and Guest VLANs
- NAT overload (PAT) on R1 so internal devices can share one public IP to reach the internet
- Trunk and access ports configured across SW1/SW2
- ACL configured to block the Guest VLAN from reaching the Server VLAN
- SSH-only management access, allowed only from the Management VLAN

## Troubleshooting

I broke 5 things on purpose, then found and fixed each one using Cisco IOS
commands. Details and screenshots are in the `scenarios/` folder.

1. **Wrong access port VLAN** — fixed by reassigning the port to the right VLAN
2. **Missing VLAN on trunk** — fixed by adding the VLAN to the trunk's allowed list
3. **Wrong DHCP default gateway** — fixed by correcting the DHCP pool
4. **Missing NAT inside on a subinterface** — fixed by adding `ip nat inside`
5. **ACL blocking DNS** — fixed by removing the bad ACL (done manually, not part of the checker)

## Python checker

`checker.py` reads the expected setup from `requirements.yaml` (using
PyYAML) and compares it against the real Cisco config files in `configs/`.
It prints `[PASS]` or `[FAIL]` for each thing it checks (VLANs, DHCP, trunk
VLANs, NAT, etc.).

### Run it

```
pip install pyyaml
python checker.py
```

Example output:

```
[PASS] Vlan 10
[PASS] VLAN 10 gateway
[FAIL] VLAN 10 EMPLOYEE dhcp default gateway
[PASS] NAT overload
```

## What I learned

This was my first hands-on project combining Cisco networking with Python.
It helped me get comfortable with VLANs, DHCP, NAT, and ACLs, and with
troubleshooting a network step by step instead of guessing. Writing the
checker also gave me practice reading config files and comparing them
against expected values in code.

**Note:** Scenario 5 (the DNS/ACL one) was troubleshot manually and isn't
part of the automated checker.