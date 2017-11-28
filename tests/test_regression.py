#!/usr/bin/env python3

from aggregate6 import aggregate
import unittest

class TestAggregate(unittest.TestCase):

    def test_00__default_wins(self):
        self.assertEqual(aggregate(["0.0.0.0/0", "10.0.0.0/16"]),
                         ["0.0.0.0/0"])

    def test_01__join_two(self):
        self.assertEqual(aggregate(["10.0.0.0/8", "11.0.0.0/8"]),
                         ["10.0.0.0/7"])

    def test_03__mix_v4_v6_default(self):
        self.assertEqual(aggregate(["0.0.0.0/0", "::/0"]),
                         ["0.0.0.0/0", "::/0"])

    def test_04__lot_of_ipv4(self):
        pfxs = []
        for i in range(0, 256):
            pfxs.append("{}.0.0.0/8".format(i))
        self.assertEqual(aggregate(pfxs), ["0.0.0.0/0"])

    def test_05__lot_of_ipv4_holes(self):
        pfxs = []
        for i in range(5, 200):
            pfxs.append("{}.0.0.0/8".format(i))
        outcome = ["5.0.0.0/8", "6.0.0.0/7", "8.0.0.0/5", "16.0.0.0/4",
                   "32.0.0.0/3", "64.0.0.0/2", "128.0.0.0/2", "192.0.0.0/5"]
        self.assertEqual(aggregate(pfxs), outcome)

    def test_06__reduce_dups(self):
        self.assertEqual(aggregate(["2001:db8::/32", "2001:db8::/32"]),
                         ["2001:db8::/32"])


def main():
    unittest.main()

if __name__ == '__main__':
    main()
