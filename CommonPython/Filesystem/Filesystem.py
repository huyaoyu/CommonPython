from __future__ import print_function

import glob
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

def test_directory_by_filename(fn):
    parts = get_filename_parts(fn)

    return test_directory(parts[0])

def find_files(d, pattern):
    files = sorted( glob.glob( '%s/**/%s' % (d, pattern), recursive=True ) )

    return files