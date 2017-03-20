# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class ReadOnlyDataStructure:

    auto_properties = ( )
    __subclasses = set()

    def __init__ (self, **kwargs):
        self.__set_read_only_data(kwargs)
        self.__create_auto_properties()

    def get (self, key, default = None):
        return self.__read_only_data.get(key, default)

    def __bool__ (self):
        return bool(self.__read_only_data)

    def __repr__ (self):
        dictstr = [self.__class__.__name__]
        for key, value in self.__read_only_data.items():
            dictstr.append("{}={}".format(key, repr(value)))

        return "<{}>".format(" ".join(dictstr))

    def __set_read_only_data (self, kwargs):
        self.__read_only_data = kwargs
        self.__remove_null_keys()

    def __remove_null_keys (self):
        null_keys = [k for k, v in self.__read_only_data.items() if v is None]

        for key in null_keys:
            del self.__read_only_data[key]

    def __create_auto_properties (self):
        if self.__class__ not in self.__subclasses:
            self.__subclasses.add(self.__class__)
            self.__add_each_auto_property()

    def __add_each_auto_property (self):
        for p in self.auto_properties:
            self.__examine_then_add_auto_property(p)


    def __examine_then_add_auto_property (self, prop):
        if isinstance(prop, tuple):
            self.__add_auto_property(*prop)

        else:
            self.__add_auto_property(prop)

    def __add_auto_property (self, prop_name, default = None):
        def getp (self):
            return self.get(prop_name, default)

        setattr(self.__class__, prop_name, property(getp))
