# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class ReadOnlyDataStructure:

    auto_properties = ( )

    def __init__ (self, **kwargs):
        self.__internal = kwargs
        self.__remove_null_keys()
        self.__create_auto_properties()

    def get (self, key, default = None):
        return self.__internal.get(key, default)

    def __bool__ (self):
        return bool(self.__internal)

    def __repr__ (self):
        dictstr = [self.__class__.__name__]
        for key, value in self.__internal.items():
            dictstr.append("{}={}".format(key, repr(value)))

        return "<{}>".format(" ".join(dictstr))

    def __remove_null_keys (self):
        null_keys = [k for k, v in self.__internal.items() if v is None]

        for key in null_keys:
            del self.__internal[key]

    def __create_auto_properties (self):
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
