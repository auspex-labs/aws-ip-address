import requests
import json

from ipaddress import ip_network

# TODO Utilize Pandas

# Obtain the AWS IP address range from https://ip-ranges.amazonaws.com/ip-ranges.json


def download_addresses(url="https://ip-ranges.amazonaws.com/ip-ranges.json"):

    ip_ranges_json = json.loads(requests.get(url).content)

    return ip_ranges_json


# Extract the CIDRs from the JSON file.


def extract_ipv4(ip_ranges_json):

    ipv4prefixes = list()
    for prefix in ip_ranges_json["prefixes"]:
        ipv4prefixes.append(prefix["ip_prefix"])

    return ipv4prefixes


def extract_ipv6(ip_ranges_json):

    ipv6prefixes = list()
    for prefix in ip_ranges_json["ipv6_prefixes"]:
        ipv6prefixes.append((ip_network(prefix["ipv6_prefix"]).exploded))

    return ipv6prefixes


def reduce_cidr(prefixes):

    # Remove any duplicate CIDRs

    cidr = list()
    [cidr.append(x) for x in prefixes if x not in cidr]
    cidr.sort()

    # Remove CIDRs that are subnets of other CIDRs.

    for net in cidr.copy():
        for sub in cidr.copy():
            if net != sub:
                if ip_network(net).subnet_of(ip_network(sub)):
                    cidr.remove(net)

    # Find and merge adjacent CIDRs.

    networks = dict()
    [networks.update({(int(x.split("/")[1])): []}) for x in cidr if int(x.split("/")[1]) not in networks.keys()]

    for net in cidr:
        networks[int(net.split("/")[1])].append(net)

    updates = True
    while updates:
        updates = False
        for mask in sorted(networks.copy()):
            for network in networks[mask].copy():
                complete = True
                for sub in ip_network(network).supernet().subnets():
                    if str(sub) not in networks[mask]:
                        complete = False
                if complete:
                    updates = True
                    supernet = str(ip_network(network).supernet())
                    if int(supernet.split("/")[1]) in networks:
                        networks[int(supernet.split("/")[1])].append(supernet)
                    else:
                        networks.update({(int(supernet.split("/")[1])): [supernet]})
                    for sub in ip_network(network).supernet().subnets():
                        networks[mask].remove(str(sub))

    return networks


#  Return a list of CIDRs


def print_cidr(networks):

    for mask in sorted(networks):
        for cidr in sorted(networks[mask]):
            print(cidr)

    return


def list_cidr(networks):

    result = []

    for mask in sorted(networks):
        for cidr in sorted(networks[mask]):
            result.append(ip_network(cidr))

    return result


def write_cidr(networks):

    with open("aws_networks.json", "w") as open_file:
        json.dump(networks, open_file, indent=4, sort_keys=True)

    return


print(".", end="")

ip_ranges_json = download_addresses()

print(".", end="")

ipv4 = extract_ipv4(ip_ranges_json)

# ipv6 = extract_ipv6(ip_ranges_json)

print(".", end="")

ipv4 = reduce_cidr(ipv4)

# ipv6 = reduce_cidr(ipv6)

# print_cidr(ipv4)

# print_cidr(ipv6)

print(list_cidr(ipv4))

print(".", end="")

# write_cidr(ipv4)
