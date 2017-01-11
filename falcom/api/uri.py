# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from urllib.parse import urlencode

class FakeMapping:

    def __init__ (self):
        self.__set = set()

    def __getitem__ (self, key):
        self.__set.add(key)
        return 0

    def get_set (self):
        return self.__set

class URI:

    class MissingRequiredArg (RuntimeError):
        pass

    def __init__ (self, uri_base = None):
        self.__set_uri_base(uri_base)
        self.__extract_required_args()

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

    def __extract_required_args (self):
        fake_mapping = FakeMapping()
        junk = self.__base.format_map(fake_mapping)
        self.__required_args = fake_mapping.get_set()

    def __get_url_pieces (self, kwargs):
        result = [self.__base]

        for arg in self.__required_args:
            if arg not in kwargs:
                raise self.MissingRequiredArg

        if kwargs:
            result.append(urlencode(kwargs))

        return result
