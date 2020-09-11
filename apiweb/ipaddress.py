from __future__ import absolute_import, division, unicode_literals

import socket
import unittest

from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class IPAddress(object):
    def __init__(self, *args, **kwargs):
        if not args and "ip" in kwargs:
            ip = kwargs.pop("ip")
        else:
            ip = args[0]
            args = args[1:]
        try:
            ip = ip.split(",")[0]  # use only the first; hope that's enough
            self.name, dummy, numbers = socket.gethostbyaddr(ip)
        except socket.error:
            self.name, numbers = "example.com", ["-1.0.0.0"]
        self.number = numbers[0]
        self.length = dict(name=len(self.name), number=len(self.number))
        super(IPAddress, self).__init__(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.name, self.number)

    def matches(self, args):
        return self.name.endswith(tuple(args)) or self.number.startswith(tuple(args))


class TestIPAddress(unittest.TestCase):
    def setUp(self):
        self.ipaddress = IPAddress("www.astro.uva.nl")

    def test_basic(self):
        """Test name resolution"""
        self.assertEqual(str(self.ipaddress), "waterman.science.uva.nl (146.50.56.36)")

    def test_ip(self):
        """Match a single IP address"""

        # addresses same as in test_name()
        self.assertFalse(self.ipaddress.matches(["74.125.77.99"]))
        self.assertTrue(self.ipaddress.matches(["146.50.56.36"]))
        self.assertTrue(self.ipaddress.matches(["146.50.56"]))
        self.assertTrue(self.ipaddress.matches(["146.50"]))

    def test_ips(self):
        """Match a multiple IP addresses"""

        addresses = ["74.126.77.99", "64.4.31.252", "157.166.255.18"]
        self.assertFalse(self.ipaddress.matches(addresses))
        addresses.append("146.50.56")
        self.assertTrue(self.ipaddress.matches(addresses))

    def test_name(self):
        """Match a single name"""

        self.assertFalse(self.ipaddress.matches(["www.google.com"]))
        self.assertFalse(self.ipaddress.matches(["www.astro.uva.nl"]))
        self.assertTrue(self.ipaddress.matches(["waterman.science.uva.nl"]))
        self.assertTrue(self.ipaddress.matches(["science.uva.nl"]))
        self.assertFalse(self.ipaddress.matches(["winfo.science.uva.nl"]))

    def test_names(self):
        """Match a multiple IP names"""

        addresses = ["www.google.com", "www.microsoft.com", "cnn.com"]
        self.assertFalse(self.ipaddress.matches(addresses))
        addresses.append("science.uva.nl")
        self.assertTrue(self.ipaddress.matches(addresses))

    def test_errors(self):
        """Test for non-resolvable IP names"""

        address = IPAddress("83.149.71.231")
        self.assertEqual(address.name, "example.com")
        self.assertEqual(address.number, "-1.0.0.0")
        address = IPAddress("117.207.59.128")
        self.assertEqual(address.name, "example.com")
        self.assertEqual(address.number, "-1.0.0.0")
        address = IPAddress("62.61.71.197, 10.37.28.203")
        self.assertEqual(address.name, "example.com")
        self.assertEqual(address.number, "-1.0.0.0")


if __name__ == "__main__":
    unittest.main()
