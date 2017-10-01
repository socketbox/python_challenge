import unittest
import xfipchk


class TestXfipchk(unittest.TestCase):
    API_CREDS = './xforce.cfg'

    def test_validate_ip(self):
        ADDRESS_FILE = './ips.txt'
        BAD_IPS = 4
        GOOD_IPS = 16

        good, bad = 0
        with open(ADDRESS_FILE, 'r') as ipfile:
            for ip in ipfile:
                if xfipchk(ip):
                    good += 1
                else:
                    bad += 1

        assert (good == GOOD_IPS and bad == BAD_IPS)


if __name__ == '__main__':
    unittest.main()
