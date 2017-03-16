# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class MutableTree:

    def __init__ (self):
        self.length = 0
        self.value = None

    @property
    def value (self):
        return self.__value

    @value.setter
    def value (self, x):
        self.__value = x

    def full_length (self):
        return len(self)

    def walk (self):
        return iter(())

    def __len__ (self):
        return self.length

    def __iter__ (self):
        return iter(())

    def __getitem__ (self, index):
        raise IndexError("tree index out of range")

    def __repr__ (self):
        return "<{}>".format(self.__class__.__name__)

    def insert (self, index, node):
        self.length = 1