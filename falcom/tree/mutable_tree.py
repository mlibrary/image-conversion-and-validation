# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class MutableTree:

    def __init__ (self, value = None):
        self.children = [ ]
        self.value = value

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
            yield from child

    def __getitem__ (self, index):
        return self.children[index]

    def insert (self, index, node):
        self.children.insert(index, node)

    def __repr__ (self):
        debug = self.__class__.__name__

        if self.value is not None:
            debug += " " + repr(self.value)

        return "<{} {}>".format(debug, repr(self.children))
