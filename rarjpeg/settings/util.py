import ctypes
import mmh3

def username(email):
    return (email[:email.rindex('@')] +
            format(ctypes.c_uint32(mmh3.hash(email)).value, '+09x'))