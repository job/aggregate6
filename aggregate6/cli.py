#!/usr/bin/env python2.7
# Copyright (C) 2014 Job Snijders <job@ntt.net>
#
# This file is part of aggregate6
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import fileinput
import sys

try:
    import argparse
except ImportError:
    print "ERROR: install argparse manually"
    print "HINT: sudo pip install argparse"
    sys.exit(2)

try:
    from ipaddr import IPNetwork
except ImportError:
    print "ERROR: ipaddr missing"
    print "HINT: pip install ipaddr"
    sys.exit(2)

try:
    import radix
except ImportError:
    print "ERROR: radix missing"
    print "HINT: pip install \
https://github.com/mjschultz/py-radix/archive/v0.7.0.zip"
    sys.exit(2)


def aggregate(tree):
    prefixes = list(tree.prefixes())
    if len(prefixes) == 1:
        return tree
    r_tree = radix.Radix()
    # test 1: can we join adjacent prefixes into larger prefixes?
    for prefix in prefixes[:-1]:
        # current prefix
        cp = IPNetwork(prefix)
        # fetch next prefix
        if int(cp.broadcast) == 2 ** 128 - 1:
            r_tree.add(str(cp))
            continue
        np = IPNetwork(prefixes[prefixes.index(prefix) + 1])
        if cp.broadcast + 1 == np.network and cp.prefixlen == np.prefixlen:
                larger = IPNetwork('%s/%s' % (cp.network, cp.prefixlen - 1))
                r_tree.add(str(larger))
        # test 2: is the prefix already covered?
        elif tree.search_worst(prefix).prefix in [prefix, None]:
            r_tree.add(prefix)
    # test 2: is the prefix already covered? (for last item)
    if len(prefixes) > 1:
        last = r_tree.search_worst(prefixes[-1])
        if last:
            if last.prefix == prefixes[-1]:
                r_tree.add(prefixes[-1])
        else:
            r_tree.add(prefixes[-1])
    return r_tree


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('args', nargs=argparse.REMAINDER,
                        help='<file> [ ... <file> ] or STDIN')
    args = parser.parse_args()

    p_tree = radix.Radix()

    for elem in fileinput.input(args.args):
        if not elem.strip():
            continue
        try:
            prefix = str(IPNetwork(elem.strip()))
        except ValueError:
            sys.stderr.write("ERROR: '%s' is not a valid IPv6 network, \
    ignoring.\n" % elem.strip())
            continue
        if IPNetwork(prefix).version == 6:
            p_tree.add(prefix)

    # keep optimising until the list cannot be smaller
    while True:
        agg = aggregate(p_tree)
        if p_tree.prefixes() == agg.prefixes():
            break
        else:
            p_tree = agg

    # print results
    for prefix in p_tree.prefixes():
        print prefix


if __name__ == '__main__':
    main()
