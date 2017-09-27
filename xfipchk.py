#!/usr/bin/env python

"""
@author Casey Boettcher
@date 2017-09-26

This script accepts an ip address or addresses, on the command line or via newline-delimited file, and calls the ipr
method of IBM's X-Force API to retrieve data describing the address's reputation.

"""

import sys
import re
import pprint
import argparse
import requests
import IPy

XFORCE_API_BASE = 'https://api.xforce.ibmcloud.com'
XFORCE_API_IP_REP = 'ipr'
XFORCE_CRED_PATTERN = '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


def parse_args():
    """
    Parse the command line.

    :return: a Namespace object of parsed arguments
    """
    parser = argparse.ArgumentParser(description="Use the X-Force API to check IP address reputation.")
    parser.add_argument('-o', '--out', metavar='output_file',
                        type=argparse.FileType('w'), help="Write result of X-Force call to file.")
    parser.add_argument('authN', type=argparse.FileType('r'),
                        help='Path to a file containing your X-Force credentials, key and password on first and second '
                             'lines, respectively.')

    # user should not be able to specify both IP on cmdline and in a file
    ip_group = parser.add_mutually_exclusive_group()
    # TODO: nargs='N' and loop through list
    ip_group.add_argument('-i', '--ip', nargs='?', metavar='ip_address', help='An IP address to be checked via '
                                                                              'X-Force. If the IP address is omitted or invalid, the user will be prompted for one.')
    ip_group.add_argument('-I', '--Ips', type=argparse.FileType('r'), metavar='file_of_ip_addresses',
                          help='A file containing IP addresses, one per line.')
    return parser.parse_args()


def request_valid_ip():
    """
    Prompts the user for a valid IP, then validates it, returning None if invalid

    :return:
        a valid IP or None if the user supplied an invalid or private address
    """
    ip = input("Enter a valid IP address you would like to check: ")
    return validate_ip(ip)


def validate_ip(ip):
    """
    Validate an address using IPy

    :param ip: a string representation of an IP address
    :return: return None if IP is invalid or within a private network range
    """
    try:
        ipobj = IPy.IP(ip)
        if ipobj.iptype() == 'PRIVATE':
            print("IP addresses {} will be ignored as it is in a private network range.".format(ip))
            ip = None
    except ValueError as ve:
        print("Invalid IP: {}".format(ve.args))
        ip = None
    finally:
        return ip


def read_in_address_file(file):
    """
    Reads a file of IP addresses and returns only those that are valid in a list

    :param file: a plaintext file of IP addresses, one per line
    :return address_list: a list of valid IP addresses
    """
    address_list = list()
    lines = 0
    valid_ips = 0
    with file as f:
        for n in file:
            lines += 1
            if validate_ip(n.strip()):
                address_list.append(n.strip())
                valid_ips += 1
    if valid_ips < lines:
        print("Of the {} lines in the file you supplied, only {} were valid. The latter will be used to call the "
              "API.".format(lines, valid_ips))
    if valid_ips == 0:
        print("Please supply a valid IP address.")
        address_list = None
    return address_list


def read_in_xforce_keys(file):
    """
    Read a plaintext file of two lines and return X-Force credentials in the form of a tuple, validating general form
    of the key and password in the process

    :param file:  a two-line plaintext files; the first line contains the X-Force API key and the second the password
    :return:    a tuple of (key, password)
    """
    matcher = re.compile(XFORCE_CRED_PATTERN)
    for x in range(0, 2):
        if x == 0:
            key = file.readline().strip()
            if not matcher.match(key):
                print("API key invalid. Exiting...")
                sys.exit(1)
        if x == 1:
            password = file.readline().strip()
            if not matcher.match(password):
                print("API password invalid. Exiting...")
                sys.exit(1)
    return key, password


def call_xforce_api(address_list, key, password):
    """
    Call the ipr method of the X-Force API using the IP address(es) contained in the parameter. Results are written
    to a file or stdout (default).

    :param address_list:  a list of IP addresses
    :return:    a list of json objects
    """
    results = []
    for a in address_list:
        url = "{}/{}/{}".format(XFORCE_API_BASE, XFORCE_API_IP_REP, a)
        results.append(requests.get(url, auth=(key, password)).json())
    return results


def print_json_stdout(results):
    """
    Print a list of json objects to the console

    :param results: a list of json objects
    """
    for json in results:
        print("\n########## Result for IP {} ##########".format(json['ip']))
        pprint.pprint(json)
        print('######################################')
        print()


def print_json_file(results, file):
    """
    Print a list of json objects to the console

    :param results:     a list of json objects
    :param file:        the destination file for the printed list of json objects passed in
    """
    print("Writing results to file...")
    for json in results:
        file.write("\n########## Result for IP {} ##########\n".format(json['ip']))
        pprint.pprint(json, stream=file)
        file.write('######################################\n')


def main():

    ip = None
    addresses = list()
    args = parse_args()
    if args.Ips:
        addresses = read_in_address_file(args.Ips)
    else:
        # get user-supplied IP address from the cmd line
        if args.ip:
            ip = validate_ip(args.ip)
        # prompt user for valid IP in case of typo on cmdline
        while not ip:
            ip = request_valid_ip()
        addresses.append(ip)
    creds = read_in_xforce_keys(args.authN)
    results = call_xforce_api(addresses, creds[0], creds[1])
    if args.out:
        print_json_file(results, args.out)
    else:
        print_json_stdout(results)

    return 0


if __name__ == '__main__':
    main()
