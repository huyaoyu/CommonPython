
def extract_int_from_string(s, expected, delimiter=","):
    expected = int(expected)
    assert expected > 0

    ss = s.split(delimiter)

    ii = [ int(i.strip()) for i in ss ]

    n = len(ii)

    if ( n != expected ):
        raise Exception("Extracted %d integers but expecting %d." % (n ,expected))

    return ii

def extract_float_from_string(s, expected, delimiter=","):
    expected = int(expected)
    assert expected > 0

    ss = s.split(delimiter)

    ff = [ float(f.strip()) for f in ss ]

    n = len(ff)

    if ( n != expected ):
        raise Exception("Extracted %d floating point numbers but expecting %d." % (n ,expected))

    return ff
