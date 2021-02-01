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

def extract_strings(line, expected, delimiter):
    ss = line.split(delimiter)
    n = len(ss)

    assert (n == expected ), \
        "{} strings extracted from {} with delimiter {}. \
Expected to be {}. ".format(n, line, delimiter, expected)

    return [ s.strip() for s in ss ]

def read_string_list_2D(fn, expCols, delimiter=",", prefix="", flagSeparateCols=False):
    """
    fn is the filename.
    expCols is the expected columns of each line. 
    delimiter is the separator between strings.
    If prefix is not empty, then the prefix string will be added to the front of each string.
    If flagSeparateCols is True, then the strings will be orgnized as separate columns.
    """
    
    assert (int(expCols) > 0), "expCols = {}. ".format(expCols)
    expCols = int(expCols)

    if ( False == os.path.isfile( fn ) ):
        raise Exception("%s does not exist." % (fn))
    
    strings2D = []
    n = 0

    with open(fn, "r") as fp:
        lines = fp.read().splitlines()

        n = len(lines)

        if ( "" == prefix ):
            for i in range(n):
                line = extract_strings(lines[i].strip(), expCols, delimiter)
                strings2D.append( line )
        else:
            for i in range(n):
                line = extract_strings(lines[i].strip(), expCols, delimiter)

                for j in range(expCols):
                    line[j] = "%s/%s" % ( prefix, line[j] )

                strings2D.append( line )

    if ( n == 0 ):
        raise Exception("Read {} failed. ".format(fn))

    if ( flagSeparateCols ):
        return [ [*entry] for entry in zip(*strings2D) ]
    else:
        return strings2D

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
