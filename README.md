[![Build Status](https://travis-ci.org/job/aggregate6.svg?branch=master)](https://travis-ci.org/job/aggregate6)
[![Requirements Status](https://requires.io/github/job/aggregate6/requirements.svg?branch=master)](https://requires.io/github/job/aggregate6/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/job/aggregate6/badge.svg?branch=master)](https://coveralls.io/github/job/aggregate6?branch=master)

aggregate6
==========

aggregate6 will compress an unsorted list of IP prefixes (both IPv4 and IPv6).

DESCRIPTION
-----------

Takes a list of IPv6 prefixes in conventional format on stdin, and performs two
optimisations to attempt to reduce the length of the prefix list. The first
optimisation is to remove any supplied prefixes which are superfluous because
they are already included in another supplied prefix. For example,
`2001:67c:208c:10::/64` would be removed if `2001:67c:208c::/48` was
also supplied.

The second optimisation identifies adjacent prefixes that can be combined under
a single, shorter-length prefix. For example, `2001:67c:208c::/48` and
`2001:67c:208d::/48` can be combined into the single prefix
`2001:67c:208c::/47`.

INSTALLATION
------------

```
$ pip install aggregate6
```

CLI USAGE
---------

Either provide the list of IPv4 and IPv prefixes on STDIN, or give filenames
containing lists of IPv6 prefixes as arguments.

```
$ # via STDIN
$ cat file_with_list_of_prefixes | aggregate6
   ... output ...

$ # with a filename as argument
$ aggregate6 file_with_list_of_prefixes [ ... optional_other_prefix_lists ]
   ... output ...

$ # Whitespace separated works too
$ echo 2001:67c:208c::/48 2000::/3 | aggregate6
2000::/3

$ # You can combine IPv4 and IPv6
$ echo 10.0.0.0/16 10.0.0.0/24 2000::/3 | aggregate6
10.0.0.0/16
2000::/3

$ # Or display only a specific AFI
$ echo 10.0.0.0/16 10.0.0.0/24 2000::/3 | aggregate6 -4
10.0.0.0/16
```

LIBRARY USAGE
-------------

```
>>> import from aggregate6 import aggregate
>>> aggregate(["10.0.0.0/8", "10.0.0.0/24"])
['10.0.0.0/8']
>>>
```

See `aggregate6 -h` for a full list of options.

BUGS
----

Please report bugs at: https://github.com/job/aggregate6/issues
