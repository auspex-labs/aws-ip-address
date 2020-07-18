import requests
import json

# Obtain the AWS IP address range from https://ip-ranges.amazonaws.com/ip-ranges.json

url = "https://ip-ranges.amazonaws.com/ip-ranges.json"

ip_ranges_json = requests.get(url).content

# Extract the CIDRs from the JSON file.

# Remove any duplicate CIDRs

# Find adjacent CIDRs and merge them if possible.

#  Return a list of CIDRs

