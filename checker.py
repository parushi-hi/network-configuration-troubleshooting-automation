import yaml
import ipaddress


# Open the requirements.yaml file in read mode and convert its data in python
with open("requirements.yaml","r") as file:
    requirements=yaml.safe_load(file)


# Open the R1 configuration file and read its content
with open("configs/R1.txt", "r") as file:
    config_R1 = file.read()


# Check required VLANs
for vlan in requirements["vlans"]:
   value=f"encapsulation dot1Q {vlan['id']}" in config_R1
   if value:
       print(f"[PASS] Vlan {vlan['id']}")
   else:
       print(f"[FAIL] Vlan {vlan['id']}")
print()


#check for required subinterfaces
for vlan in requirements["vlans"]:
    interface = f"interface GigabitEthernet0/1.{vlan['id']}"
    if interface in config_R1:
        print(f"[PASS] Interface for VLAN {vlan['id']}")
    else:
        print(f"[FAIL] Interface for VLAN {vlan['id']}")
print()


# Check VLAN gateways
lines = config_R1.splitlines()

for vlan in requirements["vlans"]:
    expected_interface = f"interface GigabitEthernet0/1.{vlan['id']}"
    expected_gateway = vlan["gateway"]
    network = ipaddress.ip_network(vlan["subnet"])
    expected_subnet = str(network.netmask)

    current_interface = False
    interface_found = False

    for line in lines:
        if line.startswith("interface "):
            current_interface = line == expected_interface
            if current_interface:
                interface_found = True
        elif current_interface and line.strip().startswith("ip address"):
            actual_gateway = line.strip().split()[2]
            actual_subnet = line.strip().split()[3]
            if actual_gateway == expected_gateway:
                print(f"[PASS] VLAN {vlan['id']} gateway")
            else:
                print(f"[FAIL] VLAN {vlan['id']} gateway")

            if actual_subnet == expected_subnet:
                print(f"[PASS] VLAN {vlan['id']} subnet")
            else:
                print(f"[FAIL] VLAN {vlan['id']} subnet")
            break
    if not interface_found:
        print(f"[FAIL] Interface for VLAN {vlan['id']} not found")
print()


#check dhcp for EMPLOYEE and GUEST
lines=config_R1.splitlines()
for vlan in requirements["dhcp"]:
       expected_vlan=vlan["vlan"]
       network=ipaddress.ip_network(vlan["network"])
       expected_network=str(network.network_address)
       expected_subnet=str(network.netmask)
       expected_gateway=vlan["gateway"]
       expected_dns=vlan["dns"]

       current_vlan=False

       for line in lines:
              if line.strip().startswith("ip dhcp pool"):
                     if line.strip().split()[3]=="EMPLOYEE":
                            name="EMPLOYEE"
                            current_vlan=10==expected_vlan
                     elif line.strip().split()[3]=="GUEST":
                            name="GUEST"
                            current_vlan=20==expected_vlan
              elif current_vlan and line.strip().startswith("network"):
                     actual_network=line.strip().split()[1]
                     actual_subnet=line.strip().split()[2]
                     if(actual_network==expected_network and actual_subnet==expected_subnet):
                            print(f"[PASS] VLAN {vlan['vlan']} {name} dhcp network")
                     else:
                            print(f"[FAIL] VLAN {vlan['vlan']} {name} network") 
              elif current_vlan and line.strip().startswith("default-router"):
                     actual_gateway=line.strip().split()[1]
                     if(actual_gateway==expected_gateway):
                             print(f"[PASS] VLAN {vlan['vlan']} {name} dhcp default gateway")
                     else:
                              print(f"[FAIL] VLAN {vlan['vlan']} {name} dhcp default gateway")
              elif current_vlan and line.strip().startswith("dns-server"):
                     actual_dns=line.strip().split()[1]
                     if(actual_dns==expected_dns):
                             print(f"[PASS] VLAN {vlan['vlan']} {name} dhcp dns-server")
                     else:
                              print(f"[FAIL] VLAN {vlan['vlan']} {name} dhcp dns-server")
                     break
print()


#check allowed vlan on trunk ports
configs = {
    "SW1": "configs/SW1.txt",
    "SW2": "configs/SW2.txt"
}

for switch, filename in configs.items():
    with open(filename, "r") as file:
        config = file.read()

    lines = config.splitlines()

    for vlan in requirements["trunks"]:
        if vlan["switch"] != switch:
            continue

        expected_interface = vlan["interface"]
        expected_vlan = vlan["allowed_vlans"]
        current_interface = False

        for line in lines:
            line = line.strip()

            if line.startswith("interface Gigabit"):
                current_interface = line.split()[1] == expected_interface
            elif current_interface and line.startswith("switchport trunk allowed"):
                actual_vlans = list(map(int, line.split()[4].split(",")))
                if expected_vlan == actual_vlans:
                    print(f"[PASS] {switch} {expected_interface} allowed vlan")
                else:
                    print(f"[FAIL] {switch} {expected_interface} allowed vlan")

                break
print()


#check access ports on SW1 and SW2
configs = {
    "SW1": "configs/SW1.txt",
    "SW2": "configs/SW2.txt"
}

for switch, filename in configs.items():
    with open(filename, "r") as file:
        config = file.read()

    lines = config.splitlines()

    for port in requirements["access_ports"]:
        if port["switch"] != switch:
            continue

        expected_interface = port["interface"]
        expected_vlan = port["vlan"]
        current_interface = False

        for line in lines:
            line = line.strip()

            if line.startswith("interface "):
                current_interface = line.split()[1] == expected_interface
            elif current_interface and line.startswith("switchport mode"):
                actual_mode = line.split()[2]
                if actual_mode == "access":
                    print(f"[PASS] {switch} {expected_interface} access mode")
                else:
                    print(f"[FAIL] {switch} {expected_interface} access mode")
            elif current_interface and line.startswith("switchport access vlan"):
                actual_vlan = int(line.split()[3])
                if actual_vlan == expected_vlan:
                    print(f"[PASS] {switch} {expected_interface} VLAN")
                else:
                    print(f"[FAIL] {switch} {expected_interface} VLAN")
                break
print()


#check NAT
lines=config_R1.splitlines()
nat_requirement = requirements["nat"]
expected_interface = nat_requirement["outside_interface"]
expected_overload = nat_requirement["overload"]

nat_found = False

for line in lines:
    line = line.strip()
    if line.startswith("ip nat inside source list"):
        parts = line.split()
        actual_interface = parts[7]
        actual_overload = "overload" in parts
        if actual_interface == expected_interface and actual_overload == expected_overload:
            print("[PASS] NAT overload")
        else:
            print("[FAIL] NAT overload")
        nat_found = True
        break
if not nat_found:
    print("[FAIL] NAT overload")

nat_requirement = requirements["nat"]
for expected_interface in nat_requirement["inside_interfaces"]:

    current_interface = False

    for line in lines:
        line = line.strip()
        if line.startswith("interface "):
            current_interface = line.split()[1] == expected_interface
        elif current_interface and line == "ip nat inside":
            print(f"[PASS] R1 {expected_interface} NAT inside")
            break
    else:
        print(f"[FAIL] R1 {expected_interface} NAT inside")

expected_interface = requirements["nat"]["outside_interface"]
current_interface = False
nat_outside_found = False

for line in lines:
    line = line.strip()
    if line.startswith("interface "):
        current_interface = line.split()[1] == expected_interface
    elif current_interface and line == "ip nat outside":
        print(f"[PASS] R1 {expected_interface} NAT outside")
        nat_outside_found = True
        break
if not nat_outside_found:
    print(f"[FAIL] R1 {expected_interface} NAT outside")
print()
                  