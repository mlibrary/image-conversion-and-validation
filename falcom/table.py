# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class Table:

    def __init__ (self, tab_separated_text = None):
        self.text = tab_separated_text

    @property
    def rows (self):
        return len(self)

    @property
    def cols (self):
        return len(self)

    def __len__ (self):
        return 1 if self.text else 0

    def __iter__ (self):
        return iter(((self.text,),)) if self.text else iter(())

    def __getitem__ (self, key):
        raise IndexError

    def __repr__ (self):
        return "<{} {}>".format(self.__class__.__name__,
                                repr(self.text))
