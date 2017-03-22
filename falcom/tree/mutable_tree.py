# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class MutableTree:

    def __init__ (self, *args, **kwargs):
        self.__assert_no_more_than_one_arg(args, kwargs)

        self.__clear_tree()

        self.__parse_args(args, kwargs)

    def __assert_no_more_than_one_arg (self, args, kwargs):
        if len(args) + len(kwargs) > 1:
            raise TypeError

    def __clear_tree (self):
        self.children = [ ]

    def __parse_args (self, args, kwargs):
        if args:
            self.deep_copy_from(args[0])

        else:
            self.__read_value_if_any(kwargs)

    def __read_value_if_any (self, kwargs):
        if kwargs:
            if "value" in kwargs and len(kwargs) == 1:
                self.value = kwargs["value"]

            else:
                raise TypeError

        else:
            self.value = None

    @property
    def value (self):
        return self.__value

    @value.setter
    def value (self, x):
        self.__value = x

    def __len__ (self):
        return len(self.children)

    def full_length (self):
        return len(self) + sum(c.full_length() for c in self)

    def __iter__ (self):
        return iter(self.children)

    def walk (self):
        for child in self:
            yield child
            yield from child.walk()

    def __getitem__ (self, index):
        return self.children[index]

    def insert_tree (self, index, node):
        self.children.insert(index, node)

    def append_tree (self, node):
        self.children.append(node)

    def deep_copy_from (self, input_tree):
        self.value = input_tree.value
        for child in input_tree:
            self.insert_tree(len(self), MutableTree(child))

    def __eq__ (self, rhs):
        return self.value == rhs.value \
                and len(self) == len(rhs) \
                and all(self[i] == rhs[i] for i in range(len(self)))

    def __repr__ (self):
        debug = self.__class__.__name__

        if self.value is not None:
            debug += " " + repr(self.value)

        return "<{} {}>".format(debug, repr(self.children))
