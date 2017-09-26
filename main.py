import pprint
import argparse
import requests
import IPy

XFORCE_API_BASE = 'https://api.xforce.ibmcloud.com'
XFORCE_API_IP_REP = 'ipr'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--xforce', required=True, type=argparse.FileType('r'), help='Path to a file containing '
                                                                                           'your X-Force credentials.')
    parser.add_argument('address', nargs='?', help='An IP address to be checked via X-Force')
    return parser.parse_args()


def request_valid_ip():
    ip = input("Enter a valid IP address you would like to check: ")
    return validate_ip(ip)


def validate_ip(ip):
    try:
        ipobj = IPy.IP(ip)
        if ipobj.iptype() == 'PRIVATE':
            print("IP addresses should not be in private network ranges")
            ip = None
    except ValueError as ve:
        print("Invalid IP: {}".format(ve.args))
        ip = None
    finally:
        return ip


def read_in_xforce_keys(file):
    for x in range(0, 2):
        if x == 0:
            key = file.readline().strip()
        if x == 1:
            password = file.readline().strip()
    return key, password


def main():
    ip = None
    args = parse_args()

    # get user-supplied IP address
    if args.address:
        ip = validate_ip(args.address)
    while not ip:
        ip = request_valid_ip()

    url = "{}/{}/{}".format(XFORCE_API_BASE, XFORCE_API_IP_REP, ip)

    # get X-Force API keys
    creds = read_in_xforce_keys(args.xforce)
    result = requests.get(url, auth=(creds[0], creds[1]))
    pprint.pprint(result.json())
    return 0


if __name__ == '__main__':
    main()
