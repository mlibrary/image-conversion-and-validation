# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from urllib.parse import urlencode

class URI:

    def __init__ (self, uri_base = None):

        self.__set_uri_base(uri_base)

    def __call__ (self, **kwargs):
        return "?".join(self.__get_url_pieces(kwargs))

    def __bool__ (self):
        return bool(self.__base)

    def __eq__ (self, rhs):
        try:
            return self.__base == rhs.__base

        except:
            return False

    def __repr__ (self):
        return "<{} {}>".format(self.__class__.__name__,
                                repr(self.__base))

    def __set_uri_base (self, uri_base):
        if uri_base is None:
            self.__base = ""

        else:
            self.__base = uri_base

    def __get_url_pieces (self, kwargs):
        result = [self.__base]

        if kwargs:
            result.append(urlencode(kwargs))

        return result
