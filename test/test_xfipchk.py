import os
import requests
import unittest
import xfipchk


class TestXfipchk(unittest.TestCase):
    API_CREDS = '../keys.txt'
    CREDS_TEST_FILE = './data/creds.txt'
    ADDRESS_TEST_FILE = './data/ips.txt'

    def test_validate_ip(self):
        BAD_IPS = 4
        GOOD_IPS = 16
        good = bad = 0
        with open(self.ADDRESS_TEST_FILE, 'r') as ipfile:
            for ip in ipfile:
                if xfipchk.validate_ip(ip):
                    good += 1
                else:
                    bad += 1

        assert (good == GOOD_IPS and bad == BAD_IPS)

    def test_validate_api_creds(self):
        good = bad = 0
        GOOD_TOKENS = 5
        BAD_TOKENS = 6
        with open(self.CREDS_TEST_FILE, 'r') as file:
            for line in file:
                if xfipchk.validate_api_creds(line.strip()):
                    good += 1
                else:
                    bad += 1

    def test_start_server(self):
        os.chdir('..')
        xfipchk.start_server()
        try:
            r = requests.get('http://127.0.0.1:8080')
        except:
            assert False


if __name__ == '__main__':
    unittest.main()
