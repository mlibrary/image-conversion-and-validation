# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class Table:

    rows = 0
    cols = 0

    def __init__ (self, tab_separated_text = None):
        self.text = tab_separated_text

    def __len__ (self):
        return 1 if self.text else 0

    def __iter__ (self):
        return iter(())

    def __getitem__ (self, key):
        raise IndexError

    def __repr__ (self):
        return "<{} {}>".format(self.__class__.__name__,
                                repr(self.text))
