# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class MutableTree:

    def __init__ (self, input_tree = None, value = None):
        self.children = [ ]
        self.value = value

        if input_tree is not None:
            self.deep_copy_from(input_tree)

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

    def insert (self, index, node):
        self.children.insert(index, node)

    def append (self, node):
        pass

    def deep_copy_from (self, input_tree):
        self.value = input_tree.value
        for child in input_tree:
            self.insert(len(self), MutableTree(child))

    def __eq__ (self, rhs):
        return self.value == rhs.value \
                and len(self) == len(rhs) \
                and all(self[i] == rhs[i] for i in range(len(self)))

    def __repr__ (self):
        debug = self.__class__.__name__

        if self.value is not None:
            debug += " " + repr(self.value)

        return "<{} {}>".format(debug, repr(self.children))
