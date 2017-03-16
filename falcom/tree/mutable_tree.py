# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class MutableTree:

    def __init__ (self, value = None):
        self.child = None
        self.children = [ ]
        self.value = value

    @property
    def value (self):
        return self.__value

    @value.setter
    def value (self, x):
        self.__value = x

    def __len__ (self):
        return 0 if self.child is None else 1

    def full_length (self):
        return len(self)

    def __iter__ (self):
        if self:
            return iter((self.child,))

        else:
            return iter(())

    def walk (self):
        return iter(self)

    def __getitem__ (self, index):
        return self.children[index]

    def insert (self, index, node):
        self.child = node
        self.children.insert(index, node)

    def __repr__ (self):
        debug = self.__class__.__name__

        if self.value is not None:
            debug += " " + repr(self.value)

        return "<{} {}>".format(debug, repr(self.children))
