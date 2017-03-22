# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class Tree:

    def __init__ (self, tree = None):
        if tree is None:
            self.__value = None
            self.children = ()

        else:
            self.__value = tree.value
            self.children = tuple(Tree(c) for c in tree)

    @property
    def value (self):
        return self.__value

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

    def values (self):
        return (c.value for c in self)

    def walk_values (self):
        return (c.value for c in self.walk())

    def __getitem__ (self, index):
        return self.children[index]

    def __eq__ (self, rhs):
        return True

    def __repr__ (self):
        debug = self.__class__.__name__

        if self.value is not None:
            debug += " " + repr(self.value)

        return "<{}>".format(debug)
