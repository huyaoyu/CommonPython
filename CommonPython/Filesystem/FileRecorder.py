from __future__ import print_function

import os

def read_string_list(fn):
    """
    Read a file contains lines of strings. A list will be returned.
    Each element of the list contains a single entry of the input file.
    Leading and tailing white spaces, tailing carriage return will be stripped.
    """

    if ( False == os.path.isfile( fn ) ):
        raise Exception("%s does not exist." % (fn))
    
    with open(fn, "r") as fp:
        lines = fp.read().splitlines()

        n = len(lines)

        for i in range(n):
            lines[i] = lines[i].strip()

    return lines

def write_string_list_2_file(fn, s):
    """
    Write a string list s into a file fn.
    Every element of s will be written as a separate line.
    """

    with open(fn, "w") as fp:
        n = len(s)

        for i in range(n):
            temp = "%s\n" % (s[i].strip())
            fp.write(temp)
