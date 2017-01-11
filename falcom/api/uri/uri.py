# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from urllib.parse import urlencode

from .fake_mapping import FakeMappingThatRecordsAccessions

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
        recorder = FakeMappingThatRecordsAccessions()
        recorder.check_on_format_str(self.__base)

        self.__required_args = recorder.get_set()

    def __get_url_pieces (self, kwargs):
        self.__assert_that_we_have_all_required_kwargs(kwargs)

        result = [self.__base]

        if kwargs:
            result.append(urlencode(kwargs))

        return result

    def __assert_that_we_have_all_required_kwargs (self, kwargs):
        for arg in self.__required_args:
            if arg not in kwargs:
                raise self.MissingRequiredArg
