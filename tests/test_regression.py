#!/usr/bin/env python

from aggregate6 import aggregate
from aggregate6.aggregate6 import parse_args
from aggregate6.aggregate6 import main as agg_main

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

import io
import sys
import unittest


def stub_stdin(testcase_inst, inputs):
    stdin = sys.stdin

    def cleanup():
        sys.stdin = stdin

    testcase_inst.addCleanup(cleanup)
    sys.stdin = StringIO(inputs)


def stub_stdouts(testcase_inst):
    stderr = sys.stderr
    stdout = sys.stdout

    def cleanup():
        sys.stderr = stderr
        sys.stdout = stdout

    testcase_inst.addCleanup(cleanup)
    sys.stderr = StringIO()
    sys.stdout = StringIO()


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

    def test_07__non_ip_input(self):
        stub_stdouts(self)
        with self.assertRaises(Exception) as context:
            aggregate(["this_is_no_prefix", "10.0.0.0/24"])
        self.assertTrue('ERROR: invalid IP prefix: this_is_no_prefix' in
                        str(context.exception))

    def test_08__test_args_v4(self):
        self.assertEqual(parse_args(["-4"]).ipv4_only, True)

    def test_09__main(self):
        stub_stdin(self, '1.1.1.24/29\n1.1.1.0/24\n1.1.1.1/32\n1.1.0.0/24\n\n')
        stub_stdouts(self)
        with patch.object(sys, 'argv', [""]):
            agg_main()
        self.assertEqual(sys.stdout.getvalue(), '1.1.0.0/23\n')

    def test_10__main(self):
        stub_stdin(self, '2001:db8::/32\n2001:db8::/128\n10.0.0.0/8\n')
        stub_stdouts(self)
        with patch.object(sys, 'argv', ["prog.py", "-6"]):
            agg_main()
        self.assertEqual(sys.stdout.getvalue(), '2001:db8::/32\n')

    def test_11_main(self):
        stub_stdin(self, 'not_a_prefix\n2001:db8::/32\n2001:db8::/128\n'
                   '10.0.0.0/8\n10.1.2.3/32')
        stub_stdouts(self)
        with patch.object(sys, 'argv', ["prog.py", "-4"]):
            agg_main()
        self.assertEqual(sys.stdout.getvalue(), '10.0.0.0/8\n')
        self.assertEqual(sys.stderr.getvalue(),
                         "ERROR: 'not_a_prefix' is not a valid IP network, "
                         "ignoring.\n")

    def test_12__use_space_in_stdin(self):
        stub_stdin(self, '2001:db8::/32 2001:db8::/128\n10.0.0.0/8\n')
        stub_stdouts(self)
        with patch.object(sys, 'argv', ["prog.py", "-6"]):
            agg_main()
        self.assertEqual(sys.stdout.getvalue(), '2001:db8::/32\n')

    def test_13_truncate(self):
        stub_stdin(self, '2001:db8::1/32 2001:db9::1/32\n10.5.5.5/8\n')
        stub_stdouts(self)
        with patch.object(sys, 'argv', ["prog.py", "-t"]):
            agg_main()
        self.assertEqual(sys.stdout.getvalue(), '10.0.0.0/8\n2001:db8::/31\n')

    def test_14_maxlength(self):
        stub_stdin(self, '10.0.0.0/24 10.0.1.0/25 10.0.1.128/25\n')
        stub_stdouts(self)
        with patch.object(sys, 'argv', ["prog.py", "-m", "24"]):
            agg_main()
        self.assertEqual(sys.stdout.getvalue(), '10.0.0.0/24\n')

    def test_15_verbose(self):
        stub_stdin(self, '10.0.0.0/24 10.0.1.0/24 172.16.0.0/24 10.0.0.0/32\n')
        stub_stdouts(self)
        with patch.object(sys, 'argv', ["prog.py", "-v"]):
            agg_main()
        self.assertEqual(sys.stdout.getvalue(), "+ 10.0.0.0/23\n- "
                         "10.0.0.0/24\n- 10.0.0.0/32\n- 10.0.1.0/24\n  "
                         "172.16.0.0/24\n")


class StringIO(io.StringIO):
    """
    A "safely" wrapped version
    """

    def __init__(self, value=''):
        value = value.encode('utf8', 'backslashreplace').decode('utf8')
        io.StringIO.__init__(self, value)

    def write(self, msg):
        io.StringIO.write(self, msg.encode(
            'utf8', 'backslashreplace').decode('utf8'))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
