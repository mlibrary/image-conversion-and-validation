# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class Table:

    class InputStrContainsCarriageReturn (RuntimeError):
        pass

    def __init__ (self, tab_separated_text = None):
        if tab_separated_text and "\r" in tab_separated_text:
            raise self.InputStrContainsCarriageReturn

        self.text = tab_separated_text

    @property
    def rows (self):
        return len(self)

    @property
    def cols (self):
        return len(self.text.split("\t")) if self.text else 0

    def __len__ (self):
        return 1 if self.text else 0

    def __iter__ (self):
        if self.text:
            return iter((tuple(self.text.split("\t")),))

        else:
            return iter(())

    def __getitem__ (self, key):
        if self.text and key == 0:
            return tuple(self.text.split("\t"))

        else:
            raise IndexError

    def __repr__ (self):
        return "<{} {}>".format(self.__class__.__name__,
                                repr(self.text))
