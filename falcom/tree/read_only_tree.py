# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class Tree:

    def __init__ (self, tree = None):
        if tree is None:
            self.__init_empty_tree()

        else:
            self.__init_with_base(tree)

    @property
    def value (self):
        return self.__value

    def __len__ (self):
        return len(self.__children)

    def full_length (self):
        return len(self) + sum(c.full_length() for c in self)

    def __iter__ (self):
        return iter(self.__children)

    def walk (self):
        for child in self:
            yield child
            yield from child.walk()

    def values (self):
        return (c.value for c in self)

    def walk_values (self):
        return (c.value for c in self.walk())

    def __getitem__ (self, index):
        return self.__children[index]

    def __eq__ (self, rhs):
        return self.value == rhs.value \
                and len(self) == len(rhs) \
                and all(self[i] == rhs[i] for i in range(len(self)))

    def __repr__ (self):
        debug = self.__class__.__name__

        if self.value is not None:
            debug += " " + repr(self.value)

        debug += " " + repr(list(self.__children))

        return "<{}>".format(debug)

    def __init_empty_tree (self):
        self.__value = None
        self.__children = ()

    def __init_with_base (self, base):
        self.__value = base.value
        self.__children = tuple(Tree(c) for c in base)
