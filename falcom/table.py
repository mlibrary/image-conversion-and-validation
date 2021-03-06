# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class Table:

    class InputStrContainsCarriageReturn (RuntimeError):
        pass

    class InconsistentColumnCounts (RuntimeError):
        def __init__ (self, expected_len, row):
            self.expected_len = expected_len
            self.row = row

        def __str__ (self):
            return "Expected every row to have len={:d}: {}".format(
                    self.expected_len, repr(self.row))

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

    def body (self):
        body = iter(self)
        next(body, None)
        return body

    def add_header (self, *args):
        self.__assert_valid_length(args)
        self.__header = args

    def __len__ (self):
        return len(self.__rows) + self.__get_header_rowcount()

    def __iter__ (self):
        if self.__we_have_a_header():
            yield self.__header

        yield from self.__rows

    def __getitem__ (self, key):
        if self.__we_have_a_header():
            return self.__get_item_with_header(key)

        else:
            return self.__rows[key]

    def __repr__ (self):
        items = [self.__class__.__name__, repr(self.text)]

        if self.__we_have_a_header():
            items.insert(1, repr(self.__header))

        return "<{}>".format(" ".join(items))

    def __raise_error_if_carriage_returns (self):
        if self.text and "\r" in self.text:
            raise self.InputStrContainsCarriageReturn

    def __create_internal_structure (self):
        self.__header = None
        self.__rows = self.__get_rows() if self.text else []
        self.__raise_error_unless_col_counts_are_consistent()

    def __get_rows (self):
        return [self.__split_row(r) for r in self.__rows_from_text()]

    def __split_row (self, row_text):
        return tuple(row_text.split("\t"))

    def __rows_from_text (self):
        return self.text.rstrip("\n").split("\n")

    def __raise_error_unless_col_counts_are_consistent (self):
        for row in self.__rows:
            self.__assert_valid_length(row)

    def __assert_valid_length (self, row):
        if len(row) != self.cols:
            raise Table.InconsistentColumnCounts(self.cols, row)

    def __get_header_rowcount (self):
        return 1 if self.__we_have_a_header() else 0

    def __we_have_a_header (self):
        return self.__header is not None

    def __get_item_with_header (self, key):
        if key == 0:
            return self.__header

        else:
            return self.__rows[key - 1]
