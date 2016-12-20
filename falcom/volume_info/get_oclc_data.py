# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from collections.abc import Mapping
from urllib.parse import urlencode
from urllib.request import urlopen

from ..exceptions import *
from .tabular_data import TabularData
from .argument_collector import ArgumentCollector

########################################################################
############################### Classes ################################
########################################################################

class DecoyMapping (Mapping):
    """Pretends to be a mapping but tracks queries and returns 0.

    This is nice if you need to know exactly which keys are queried.
    """

    def __init__ (self, value = 0):
        """Init an empty decoy mapping."""

        # Start with an empty set.
        self.__keys = set()
        self.__value = value

    def get_keys (self):
        """Return the set of keys."""
        return self.__keys

    def __getitem__ (self, key):
        """Add key and return 0."""

        # A query! Add this to our set.
        self.__keys.add(key)

        # Return 0. Probably safe.
        return self.__value

    def __len__ (self):
        """Return 0."""
        return 0

    def __iter__ (self):
        """Return an empty iterator."""
        return iter(())

def extract_format_keys (s):
    """Return the set of named keywords in the format string."""

    # Use a decoy mapping to track whatever we're asking for.
    mapping = DecoyMapping()

    # We use format map to stop the thing from trying to convert to a
    # dict or anything weird.
    junk = s.format_map(mapping)

    # Return the resulting set of keys.
    return mapping.get_keys()

class URI:
    """URI object that handles GET and/or POST data."""

    def __init__ (self, *args, **kwargs):
        """Init URI with base, expected args, and default data."""

        # The base URI should be the first positional argument.
        self.__uri = self.__extract_uri(args)

        # For everything else, we use an ArgumentCollector.
        self.__args = ArgumentCollector(args[1:], kwargs)

        # I don't want the arguments to iterate through any format names
        # that happen to be in the URI.
        self.__args.skip_iter(*tuple(
                extract_format_keys(self.__uri.decode("ascii"))))

    def get (self, *args, **kwargs):
        """Return an HTTPResponse for the given GET request."""

        # We store URIs as bytes objects, so we need to decode it to an
        # ASCII str.
        return urlopen(self.get_uri(*args, **kwargs).decode("ascii"))

    def post (self, *args, **kwargs):
        """Return an HTTPResponse for the given POST request."""

        uri, data = self.post_uri(*args, **kwargs)

        # We store URIs as bytes objects, so we need to decode it to an
        # ASCII str.
        return urlopen(uri.decode("ascii"), data)

    def get_uri (self, *args, **kwargs):
        """Return a URI bytes object with appropriate GET data."""

        # Get the data.
        uri, data = self.post_uri(*args, **kwargs)

        if data:
            # If we have any data, it's appended to the URI with a
            # question mark.
            return uri + b"?" + data

        else:
            # If we have no data, we can just use the URI as-is.
            return uri

    def post_uri (self, *args, **kwargs):
        """Return a duple of bytes objects: base URI and POST data."""
        # Get the data.
        data = self.__get_encoded_data(args, kwargs)

        # Get the specific URI.
        uri = self.__uri.decode("ascii").format_map(
                self.__args).encode("ascii")

        return uri, data

    ################################################################
    ################ Private Properties and Methods ################
    ################################################################

    def __extract_uri (self, positional_args):
        if positional_args:
            # If we have any arguments, then we're looking at the first
            # one. It needs to be ASCII bytes.
            return self.__assert_bytes(positional_args[0])

        else:
            # If we don't have any positional arguments, it's time to
            # raise a TypeError telling the user about it.
            #
            # Normally, it'd be better to explicitly include a named
            # argument "uri_base" in the function, but I don't want to
            # limit the names of keyword arguments. If I put that there,
            # and one of the keyword arguments was keyed on uri_base,
            # then it'd override that instead of being passed on to the
            # argument collector.
            raise TypeError("__init__() missing 1 required " \
                    "positional argument: 'uri_base'")

    def __get_encoded_data (self, args, kwargs):
        # Update our internal argument collector.
        self.__args.update(args, kwargs)

        # Run urllib.parse.urlencode on the mapping.
        encoded = urlencode(self.__args)

        # We might get a str, and we want bytes.
        return self.__assert_bytes(encoded)

    def __assert_bytes (self, ascii_str):
        if isinstance(ascii_str, bytes):
            # If it's already bytes, we'll just assume it's all ASCII.
            return ascii_str

        else:
            # If it's a str, we'll need to encode it into bytes.
            return ascii_str.encode("ascii")
