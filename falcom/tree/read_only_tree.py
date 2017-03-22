# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class Tree:

    def __init__ (self, tree = None):
        pass

    @property
    def value (self):
        pass

    def __bool__ (self):
        return False

    def __repr__ (self):
        debug = self.__class__.__name__

        if self.value is not None:
            debug += " " + repr(self.value)

        return "<{}>".format(debug)
