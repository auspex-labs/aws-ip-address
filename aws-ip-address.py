import requests
import json
import ipaddress

# Obtain the AWS IP address range from https://ip-ranges.amazonaws.com/ip-ranges.json

url = "https://ip-ranges.amazonaws.com/ip-ranges.json"

ip_ranges_json = json.loads(requests.get(url).content)

# Extract the CIDRs from the JSON file.

ipv4prefixes = list()
for prefix in ip_ranges_json["prefixes"]:
    ipv4prefixes.append(prefix["ip_prefix"])


ipv6prefixes = list()
for prefix in ip_ranges_json["ipv6_prefixes"]:
    ipv6prefixes.append((ipaddress.ip_network(prefix["ipv6_prefix"]).exploded))

# Remove any duplicate CIDRs

ipv4cidr = list()
[ipv4cidr.append(x) for x in ipv4prefixes if x not in ipv4cidr]
ipv4cidr.sort()


ipv6cidr = list()
[ipv6cidr.append(x) for x in ipv6prefixes if x not in ipv6cidr]
ipv6cidr.sort()

# Remove CIDRs that are subnets of other CIDRs.

for cidr in ipv4cidr.copy():
    for net in ipv4cidr.copy():
        if cidr != net:
            if ipaddress.ip_network(cidr).subnet_of(ipaddress.ip_network(net)):
                ipv4cidr.remove(cidr)

for cidr in ipv6cidr.copy():
    for net in ipv6cidr.copy():
        if cidr != net:
            if ipaddress.ip_network(cidr).subnet_of(ipaddress.ip_network(net)):
                ipv6cidr.remove(cidr)

# Find and merge adjacent CIDRs.

ipv4networks = dict()
[ipv4networks.update({(int(x.split("/")[1])): []}) for x in ipv4cidr if int(x.split("/")[1]) not in ipv4networks.keys()]

for cidr in ipv4cidr:
    ipv4networks[int(cidr.split("/")[1])].append(str(cidr.split("/")[0]))


ipv6networks = dict()
[ipv6networks.update({(int(x.split("/")[1])): []}) for x in ipv6cidr if int(x.split("/")[1]) not in ipv6networks.keys()]

for cidr in ipv6cidr:
    ipv6networks[int(cidr.split("/")[1])].append(str(cidr.split("/")[0]))


#  Return a list of CIDRs
