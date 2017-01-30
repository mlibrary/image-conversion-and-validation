# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class Table:

    class InputStrContainsCarriageReturn (RuntimeError):
        pass

    def __init__ (self, tab_separated_text = None):
        self.text = tab_separated_text

        self.__raise_error_if_carriage_returns()
        self.__create_internal_structure()

    @property
    def rows (self):
        return len(self)

    @property
    def cols (self):
        return len(self.__rows[0]) if self else 0

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
        if self.text and "\r" in self.text:
            raise self.InputStrContainsCarriageReturn

    def __create_internal_structure (self):
        if self.text:
            self.__rows = self.__list_of_rows_from_text()

        else:
            self.__rows = []

    def __list_of_rows_from_text (self):
        result = []
        cols = None

        for row_text in self.__rows_from_text():
            row = self.__split_row(row_text)

            if cols is None:
                cols = len(row)

            elif len(row) != cols:
                raise RuntimeError

            result.append(row)

        return result

    def __split_row (self, row_text):
        return tuple(row_text.split("\t"))

    def __rows_from_text (self):
        return self.text.rstrip("\n").split("\n")
