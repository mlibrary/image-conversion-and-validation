# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from urllib.parse import urlencode

from .args_from_format import get_expected_args_from_format_str

class URI:

    class MissingRequiredArg (RuntimeError):
        pass

    def __init__ (self, uri_base = None):
        self.__set_uri_base(uri_base)
        self.__extract_required_args()

    def __call__ (self, **kwargs):
        base, mapping = self.get_duple(kwargs)

        return self.join_uri_and_get_args(base, mapping)

    def get_duple (self, kwargs):
        if self.__required_args:
            return self.__get_formatted_base(kwargs), \
                    self.__get_mapping_without_required_args(kwargs)

        else:
            return self.__base, kwargs

    def __bool__ (self):
        return bool(self.__base)

    def __eq__ (self, rhs):
        try:
            return self.__base == rhs.__base

        except:
            return False

    @staticmethod
    def join_uri_and_get_args (base_uri, arg_dict):
        if arg_dict:
            return "?".join((base_uri, urlencode(arg_dict)))

        else:
            return base_uri

    def __repr__ (self):
        return "<{} {}>".format(self.__class__.__name__,
                                repr(self.__base))

    def __set_uri_base (self, uri_base):
        if uri_base is None:
            self.__base = ""

        else:
            self.__base = uri_base

    def __extract_required_args (self):
        self.__required_args = get_expected_args_from_format_str(
                                                        self.__base)

    def __get_formatted_base (self, kwargs):
        self.__assert_that_we_have_all_required_kwargs(kwargs)

        return self.__base.format_map(kwargs)

    def __get_mapping_without_required_args (self, kwargs):
        return dict((k, v) for k, v in kwargs.items()
                            if k not in self.__required_args)

    def __assert_that_we_have_all_required_kwargs (self, kwargs):
        for arg in self.__required_args:
            if arg not in kwargs:
                raise self.MissingRequiredArg(arg)
