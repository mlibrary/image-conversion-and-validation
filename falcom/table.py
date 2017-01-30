# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class Table:

    class InputStrContainsCarriageReturn (RuntimeError):
        pass

    def __init__ (self, tab_separated_text = None):
        if tab_separated_text:
            self.text = tab_separated_text
            self.__raise_error_if_carriage_returns()

        else:
            self.text = tab_separated_text

        self.__create_internal_structure()

    @property
    def rows (self):
        return len(self)

    @property
    def cols (self):
        return len(self.text.split("\n")[0].split("\t")) if self.text else 0

    def __len__ (self):
        return len(self.__rows)

    def __iter__ (self):
        return iter(self.__rows)

    def __getitem__ (self, key):
        return self.__rows[key]

    def __repr__ (self):
        return "<{} {}>".format(self.__class__.__name__,
                                repr(self.text))

    def __raise_error_if_carriage_returns (self):
        if "\r" in self.text:
            raise self.InputStrContainsCarriageReturn

    def __create_internal_structure (self):
        if self.text:
            self.__rows = [tuple(r.split("\t"))
                    for r in self.text.rstrip("\n").split("\n")]

        else:
            self.__rows = []
