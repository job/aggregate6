aggregate6
==========

aggregate6 will compress an unsorted list of IPv6 prefixes.

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
    $ sudo apt install python-dev python-pip3 python-setuptools
    $ git clone https://github.com/job/aggregate6
    $ cd aggregate6
    $ sudo pip3 install .

or

    $ sudo pip3 install aggregate6

```

USAGE
-----

Either provide the list of IPv6 prefixes on STDIN, or give filenames containing
lists of IPv6 prefixes as arguments.

```
    $ cat prefix_list | aggregate6
       ... output ...

    $ aggregate6 prefix_list [ ... optional_other_prefix_lists ]
       ... output ...

    $ echo -e "2001:67c:208c::/48\n2000::/3" | aggregate6
    2000::/3
```

See ```aggregate6 -h``` for a full list of options.

BUGS
----

Please report bugs at: https://github.com/job/aggregate6

Copyright and License
---------------------

Copyright (c) 2014, Job Snijders <job@instituut.net>. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
