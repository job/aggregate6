aggregate6
==========

aggregate6 will compress an unsorted list of IP (both IPv4 and IPv6) prefixes.

DESCRIPTION
-----------

Takes a list of IPv6 prefixes in conventional format on stdin, and performs two
optimisations to attempt to reduce the length of the prefix list. The first
optimisation is to remove any supplied prefixes which are superfluous because
they are already included in another supplied prefix. For example,
```2001:67c:208c:10::/64``` would be removed if ```2001:67c:208c::/48``` was
also supplied.

The second optimisation identifies adjacent prefixes that can be combined under
a single, shorter-length prefix. For example, ```2001:67c:208c::/48``` and
```2001:67c:208d::/48``` can be combined into the single prefix
2001:67c:208c::/47.

INSTALLATION
------------

```
    $ pip install aggregate6
```

USAGE
-----

Either provide the list of IPv4 and IPv prefixes on STDIN, or give filenames
containing lists of IPv6 prefixes as arguments.

```
    $ cat prefix_list | aggregate6
       ... output ...

    $ aggregate6 file_with_list_of_prefixes [ ... optional_other_prefix_lists ]
       ... output ...

    $ echo -e "2001:67c:208c::/48\n2000::/3" | aggregate6
    2000::/3
```

See ```aggregate6 -h``` for a full list of options.

BUGS
----

Please report bugs at: https://github.com/job/aggregate6/issues
