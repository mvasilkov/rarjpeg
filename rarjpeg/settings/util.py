import ctypes
import mmh3

def username(email):
    return (email[:email.rindex('@')] +
            format(ctypes.c_uint32(mmh3.hash(email)).value, '+09x'))

import os
from django.core.exceptions import ImproperlyConfigured

class _Env:
    err = 'The environment variable {} is not set'

    def __getattr__(self, attr):
        try:
            return os.environ[attr]
        except KeyError:
            raise ImproperlyConfigured(self.err.format(attr))

env = _Env()
