import requests
import json

# Obtain the AWS IP address range from https://ip-ranges.amazonaws.com/ip-ranges.json

url = "https://ip-ranges.amazonaws.com/ip-ranges.json"

ip_ranges_json = json.loads(requests.get(url).content)

# Extract the CIDRs from the JSON file.

ipv4prefixes = []
ipv6prefixes = []


for prefix in ip_ranges_json['prefixes']:
    ipv4prefixes.append(prefix['ip_prefix'])

for prefix in ip_ranges_json['ipv6_prefixes']:
    ipv6prefixes.append(prefix['ipv6_prefix'])

# Remove any duplicate CIDRs

ipv4cidr = []
ipv6cidr = []

[ipv4cidr.append(x) for x in ipv4prefixes if x not in ipv4cidr]

[ipv6cidr.append(x) for x in ipv6prefixes if x not in ipv6cidr]








# Find adjacent CIDRs and merge them if possible.

#  Return a list of CIDRs

