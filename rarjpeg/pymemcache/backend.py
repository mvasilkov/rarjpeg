from enum import IntEnum
import pickle

from django.core.cache.backends.memcached import BaseMemcachedCache
from django.utils.functional import cached_property

from . import client

_kwargs = {
    'library': client,
    'value_not_found_exception': ValueError,
}

Flags = IntEnum('Flags', 'str pickle')


def pickle_serializer(key, value):
    if isinstance(value, str):
        return value, Flags.str
    return pickle.dumps(value), Flags.pickle


def pickle_deserializer(key, value, flags):
    if flags == Flags.str:
        return value
    if flags == Flags.pickle:
        return pickle.loads(value)
    raise ValueError('Bad flags (%d)' % flags)

_options = {
    'serializer': pickle_serializer,
    'deserializer': pickle_deserializer,
}


class PyMemcacheCache(BaseMemcachedCache):
    'An implementation of a cache binding using pymemcache.'

    def __init__(self, *args):
        super().__init__(*args, **_kwargs)

    def _get_server(self):
        return ('127.0.0.1', 11211)  # TODO

    @cached_property
    def _cache(self):
        return self._lib.Client(self._get_server(), **_options)
