from __future__ import print_function

import os

def get_filename_parts(fn):
    p = os.path.split(fn)

    if ( "" == p[0] ):
        p = (".", p[1])

    f = os.path.splitext(p[1])

    return [ p[0], f[0], f[1] ]

def test_directory(d):
    if ( not os.path.isdir(d) ):
        os.makedirs(d)
