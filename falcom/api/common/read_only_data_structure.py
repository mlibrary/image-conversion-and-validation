# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class ReadOnlyDataStructure:

    auto_properties = ( )
    __subclasses = set()

    def __init__ (self, **kwargs):
        self.__set_read_only_data(kwargs)
        self.__ensure_we_have_our_property_accession_methods()

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
        null_keys = self.__independent_list_of_keys_with_null_values()

        for key in null_keys:
            del self.__read_only_data[key]

    def __independent_list_of_keys_with_null_values (self):
        return [k for k, v in self.__read_only_data.items()
                   if v is None]

    def __ensure_we_have_our_property_accession_methods (self):
        if self.__this_is_the_first_instance_of_this_class():
            self.__generate_each_property_accession_method()
            self.__mark_this_class_as_a_complete_subclass()

    def __this_is_the_first_instance_of_this_class (self):
        return self.__class__ not in self.__subclasses

    def __mark_this_class_as_a_complete_subclass (self):
        self.__subclasses.add(self.__class__)

    def __generate_each_property_accession_method (self):
        for p in self.auto_properties:
            self.__read_auto_property_instruction(p)

    def __read_auto_property_instruction (self, prop):
        if self.__property_instruction_contains_multiple_args(prop):
            self.__generate_property_accession_method(*prop)

        else:
            self.__generate_property_accession_method(prop)

    def __property_instruction_contains_multiple_args (self, prop):
        return isinstance(prop, tuple)

    def __generate_property_accession_method (self,
                                              property_name,
                                              default_value = None):
        def get_this_property (self):
            return self.get(property_name, default_value)

        setattr(self.__class__,
                property_name,
                property(get_this_property))
