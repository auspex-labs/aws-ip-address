import requests
import json

# Obtain the AWS IP address range from https://ip-ranges.amazonaws.com/ip-ranges.json

url = "https://ip-ranges.amazonaws.com/ip-ranges.json"

ip_ranges_json = json.loads(requests.get(url).content)

# Extract the CIDRs from the JSON file.

ipv4prefixes = list()
for prefix in ip_ranges_json["prefixes"]:
    ipv4prefixes.append(prefix["ip_prefix"])

ipv6prefixes = list()
for prefix in ip_ranges_json["ipv6_prefixes"]:
    ipv6prefixes.append(prefix["ipv6_prefix"])

# Remove any duplicate CIDRs

ipv4cidr = list()
[ipv4cidr.append(x) for x in ipv4prefixes if x not in ipv4cidr]

ipv6cidr = list()
[ipv6cidr.append(x) for x in ipv6prefixes if x not in ipv6cidr]


# Find adjacent CIDRs and merge them if possible.

ipv4networks = dict()
[ipv4networks.update({(int(x.split("/")[1])): []}) for x in ipv4cidr if int(x.split("/")[1]) not in ipv4networks.keys()]

ipv6networks = dict()
[ipv6networks.update({(int(x.split("/")[1])): []}) for x in ipv6cidr if int(x.split("/")[1]) not in ipv6networks.keys()]


#  Return a list of CIDRs
