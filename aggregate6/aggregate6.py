#!/usr/bin/env python
# Copyright (C) 2014-2017 Job Snijders <job@instituut.net>
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

from __future__ import print_function
from __future__ import unicode_literals

from builtins import str as text
from ipaddress import ip_network

import aggregate6
import radix
import sys


def aggregate(l):
    """Aggregate a `list` of prefixes.

    Keyword arguments:
    l -- a python list of prefixes

    Example use:
    >>> aggregate(["10.0.0.0/8", "10.0.0.0/24"])
    ['10.0.0.0/8']
    """
    tree = radix.Radix()
    for item in l:
        try:
            tree.add(item)
        except (ValueError) as err:
            print("ERROR, invalid IP prefix: {}".format(item))
            raise

    return aggregate_tree(tree).prefixes()


def aggregate_tree(l_tree):
    """Walk a py-radix tree and aggregate it.

    Arguments
    l_tree -- radix.Radix() object
    """

    def _aggregate_phase1(tree):
        # check if prefix is already covered
        n_tree = radix.Radix()
        for prefix in tree.prefixes():
            if tree.search_worst(prefix).prefix == prefix:
                n_tree.add(prefix)
        return n_tree

    def _aggregate_phase2(tree):
        n_tree = radix.Radix()
        for rnode in tree:
            p = text(ip_network(text(rnode.prefix)).supernet())
            r = tree.search_covered(p)
            if len(r) == 2:
                if r[0].prefixlen == r[1].prefixlen == rnode.prefixlen:
                    n_tree.add(p)
                else:
                    n_tree.add(rnode.prefix)
            else:
                n_tree.add(rnode.prefix)
        return n_tree

    l_tree = _aggregate_phase1(l_tree)

    if len(l_tree.prefixes()) == 1:
        return l_tree

    while True:
        r_tree = _aggregate_phase2(l_tree)
        if l_tree.prefixes() == r_tree.prefixes():
            break
        else:
            l_tree = r_tree
            del r_tree

    return l_tree


def parse_args(args):
    import argparse
    p = argparse.ArgumentParser(description="Aggregate lists of IP prefixes",
                                epilog="""
Copyright 2014-2017 Job Snijders <job@instituut.net>
Project website: https://github.com/job/aggregate6
""", formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('-v', dest='version', action='store_true',
                   help="Display aggregate6 version")
    afi_group = p.add_mutually_exclusive_group()
    afi_group.add_argument('-4', dest='ipv4_only', action='store_true',
                           default=False,
                           help="Only output IPv4 prefixes")
    afi_group.add_argument('-6', dest='ipv6_only', action='store_true',
                           default=False,
                           help="Only output IPv6 prefixes")
    p.add_argument('args', nargs=argparse.REMAINDER,
                   help='[file ...] or STDIN')
    return p.parse_args(args)


def main():
    import fileinput

    args = parse_args(sys.argv[1:])

    if args.version: # pragma: no cover
        print("aggregate6 %s" % aggregate6.__version__)
        sys.exit()

    p_tree = radix.Radix()

    for line in fileinput.input(args.args):
        if not line.strip(): # pragma: no cover
            continue
        for elem in line.strip().split():
            try:
                prefix_obj = ip_network(text(elem.strip()))
                prefix = text(prefix_obj)
            except ValueError:
                sys.stderr.write("ERROR: '%s' is not a valid IP network, \
ignoring.\n" % elem.strip())
                continue

            if args.ipv4_only and prefix_obj.version == 4:
                p_tree.add(prefix)
            elif args.ipv6_only and prefix_obj.version == 6:
                p_tree.add(prefix)
            elif not args.ipv4_only and not args.ipv6_only:
                p_tree.add(prefix)

    for prefix in aggregate_tree(p_tree).prefixes():
        print(prefix)
