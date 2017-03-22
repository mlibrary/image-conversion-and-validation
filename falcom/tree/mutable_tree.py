# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

from .read_only_tree import Tree

class MutableTree (Tree):

    def __init__ (self, *args, **kwargs):
        self.__assert_no_more_than_one_arg(args, kwargs)
        self.__parse_args(args, kwargs)

    @property
    def value (self):
        return self.__value

    @value.setter
    def value (self, x):
        self.__value = x

    def __len__ (self):
        return len(self.__children)

    def __iter__ (self):
        return iter(self.__children)

    def __getitem__ (self, index):
        return self.__children[index]

    def insert_value (self, index, value):
        self.insert_tree(index, self.new_tree_with_value(value))

    def append_value (self, value):
        self.append_tree(self.new_tree_with_value(value))

    def new_tree_with_value (self, value):
        return MutableTree(value=value)

    def insert_tree (self, index, node):
        self.__children.insert(index, node)

    def append_tree (self, node):
        self.__children.append(node)

    def __repr__ (self):
        debug = self.__class__.__name__

        if self.value is not None:
            debug += " " + repr(self.value)

        return "<{} {}>".format(debug, repr(self.__children))

    def __assert_no_more_than_one_arg (self, *arg_containers):
        total = sum(map(len, arg_containers))
        if total > 1:
            raise TypeError("Expected no more than 1 argument; " \
                            "got {:d}".format(total))

    def __parse_args (self, args, kwargs):
        if args:
            self.__deep_copy_from(args[0])

        else:
            self.__read_value_if_any(kwargs)

    def __deep_copy_from (self, input_tree):
        self.__become_new_tree(input_tree.value)
        for child in input_tree:
            self.insert_tree(len(self), MutableTree(child))

    def __read_value_if_any (self, kwargs):
        if kwargs:
            self.__extract_value_from_kwargs(kwargs)

        else:
            self.__become_new_tree()

    def __extract_value_from_kwargs (self, kwargs):
        if "value" in kwargs and len(kwargs) == 1:
            self.__become_new_tree(kwargs["value"])

        else:
            raise TypeError("Expected keywords in {} not {}".format(
                                    {"value"}, set(kwargs)))

    def __become_new_tree (self, value = None):
        self.__children = [ ]
        self.value = value
