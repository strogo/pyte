# -*- coding: utf-8 -*-
"""
    capture
    ~~~~~~~

    An example showing how to capure output from a running terminal app.

    :copyright: (c) 2015 by pyte authors and contributors,
                see AUTHORS for details.
    :license: LGPL, see LICENSE for more details.
"""

from __future__ import print_function, unicode_literals

import codecs
import os
import pty
import select
import subprocess
import sys

import pyte


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        sys.exit("usage: %prog% output command [args]")

    stream = pyte.Stream()

    decoder = codecs.getincrementaldecoder(sys.getdefaultencoding())("replace")
    master, slave = pty.openpty()
    with open(sys.argv[1], "wb") as handle:
        p = subprocess.Popen(sys.argv[2:], stdout=slave, stderr=slave)
        while True:
            try:
                [fd], _wlist, _xlist = select.select([master], [], [], 1)
            except (KeyboardInterrupt,  # Stop right now!
                    ValueError):        # Nothing to read.
                p.kill()
                break
            else:
                chunk = os.read(fd, 1024)
                handle.write(chunk)
