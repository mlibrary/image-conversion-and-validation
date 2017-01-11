# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from urllib.parse import urlencode

class URI:

    def __init__ (self, uri_base):
        if uri_base is None:
            self.__base = ""

        else:
            self.__base = uri_base

    def __call__ (self, **kwargs):
        if kwargs:
            return "?" + urlencode(kwargs)

        else:
            return self.__base

    def __bool__ (self):
        return False

    def __eq__ (self, rhs):
        return self.__base == rhs.__base

    def __repr__ (self):
        return "<{} {}>".format(self.__class__.__name__,
                                repr(self.__base))
