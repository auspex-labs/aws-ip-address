import json

from ipaddress import ip_network, ip_address


def read_address(file_name="aws_networks.json"):

    with open(file_name) as network_file:
        network = json.load(network_file)

        return network


def list_cidr(networks):

    result = []

    for mask in sorted(networks):
        for cidr in sorted(networks[mask]):
            result.append(ip_network(cidr))

    return result


def test_address(networks, ipaddress="54.240.236.94"):

    ip = ip_address(ipaddress)
    result = any(ip in network for network in networks)

    return result

networks = list_cidr(read_address())

if test_address(networks):
    print("Found")
else:
    print("Not Found")
