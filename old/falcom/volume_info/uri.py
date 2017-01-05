# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from urllib.parse import urlencode
from urllib.request import urlopen

from ..general.exceptions.type_errors import MissingPositionalArgsError
from .str_format import get_keys_required_by_format_str

class URI:
    """URI object that handles GET and/or POST data."""

    def __init__ (self, ArgumentCollector, *args, **kwargs):
        """Init URI with base, expected args, and default data."""
        self.__extract_uri(args)
        self.__set_argument_collector(ArgumentCollector, args, kwargs)
        self.__tell_collector_to_skip_format_keys()

    def get (self, *args, **kwargs):
        """Return an HTTPResponse for the given GET request."""
        return urlopen(self.get_uri(*args, **kwargs).decode("ascii"))

    def post (self, *args, **kwargs):
        """Return an HTTPResponse for the given POST request."""
        uri, data = self.post_uri(*args, **kwargs)

        return urlopen(uri.decode("ascii"), data)

    def get_uri (self, *args, **kwargs):
        """Return a URI bytes object with appropriate GET data."""
        uri, data = self.post_uri(*args, **kwargs)

        if data:
            uri += b"?" + data

        return uri

    def post_uri (self, *args, **kwargs):
        """Return a duple of bytes objects: base URI and POST data."""
        data = self.__get_encoded_data(args, kwargs)
        uri_str = self.__get_uri_str()

        uri = self.__uri.decode("ascii").format_map(
                self.__argument_collector).encode("ascii")

        return uri, data

    ################################################################
    ################ Private Properties and Methods ################
    ################################################################

    def __extract_uri (self, positional_args):
        if positional_args:
            # If we have any arguments, then we're looking at the first
            # one. It needs to be ASCII bytes.
            self.__uri = self.__assert_bytes(positional_args[0])

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
            raise MissingPositionalArgsError("__init__", 1, "uri_base")

    def __assert_bytes (self, ascii_str):
        if isinstance(ascii_str, bytes):
            # If it's already bytes, we'll just assume it's all ASCII.
            return ascii_str

        else:
            # If it's a str, we'll need to encode it into bytes.
            return ascii_str.encode("ascii")

    def __set_argument_collector (self,
            ArgumentCollector, args, kwargs):
        self.__argument_collector = ArgumentCollector(args[1:], kwargs)

    def __tell_collector_to_skip_format_keys (self):
        uri_str = self.__get_uri_str()
        key_set = get_keys_required_by_format_str(uri_str)

        self.__argument_collector.skip_iter(*tuple(key_set))

    def __get_uri_str (self):
        return self.__uri.decode("ascii")

    def __get_encoded_data (self, args, kwargs):
        # Update our internal argument collector.
        self.__argument_collector.update(args, kwargs)

        # Run urllib.parse.urlencode on the mapping.
        encoded = urlencode(self.__argument_collector)

        # We might get a str, and we want bytes.
        return self.__assert_bytes(encoded)
