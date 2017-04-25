# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedMatcher, evaluates_to
from ..table import Table

class an_internally_consistent_table (ComposedMatcher):

    def assertion (self, item):
        expected_cols = 0

        i = 0
        for row in item:
            yield row, is_(instance_of(tuple))
            yield item[i], is_(equal_to(row)), "row {:d}".format(i)

            if expected_cols:
                yield row, has_length(expected_cols), \
                        "same column counts in each row"

            else:
                yield row, has_length(greater_than(0)), \
                        "rows must have at least one column"

                expected_cols = len(row)

            i += 1

        if i:
            yield item, evaluates_to(True)

        else:
            yield item, evaluates_to(False)

        yield item, has_length(i), "length matches iteration"
        yield item.rows, is_(equal_to(i)), "row count"
        yield item.cols, is_(equal_to(expected_cols)), "column count"

        yield calling(lambda t: t[i]).with_args(item), \
              raises(IndexError), "no row with index {}".format(i)

class an_empty_table (ComposedMatcher):

    def assertion (self, item):
        yield item, is_(an_internally_consistent_table())
        yield item, evaluates_to(False)

class yields_an_empty_table (ComposedMatcher):

    def assertion (self, item):
        table = Table(item)
        yield table, is_(an_empty_table())

class TableTest (unittest.TestCase):

    def init_table (self, *args):
        self.table = Table(*args)
        assert_that(self.table, is_(an_internally_consistent_table()))

    def test_degenerate (self):
        self.init_table()
        assert_that(self.table, is_(an_empty_table()))

    def test_None_yields_empty_table (self):
        assert_that(None, yields_an_empty_table())

    def test_empty_str_yields_empty_table (self):
        assert_that("", yields_an_empty_table())

    def test_carriage_returns_are_not_allowed (self):
        assert_that(calling(Table).with_args("\r"),
                    raises(RuntimeError))
        assert_that(calling(Table).with_args("buried\rin here"),
                    raises(RuntimeError))

    def test_single_char_yields_1_row_1_col (self):
        self.init_table("a")
        assert_that(self.table, has_length(1))
        assert_that(self.table[0][0], is_(equal_to("a")))

    def test_HT_divides_2_columns (self):
        self.init_table("a\tb")
        assert_that(self.table, has_length(1))
        assert_that(self.table.cols, is_(equal_to(2)))
        assert_that(self.table[0], contains("a", "b"))

    def test_HT_divides_3_columns (self):
        self.init_table("a\tb\tc")
        assert_that(self.table, has_length(1))
        assert_that(self.table.cols, is_(equal_to(3)))
        assert_that(self.table[0], contains("a", "b", "c"))

    def test_2_rows_2_cols (self):
        self.init_table("a\tb\nc\td")
        assert_that(self.table, has_length(2))
        assert_that(self.table, contains(("a", "b"), ("c", "d")))

    def test_ignore_trailing_blank_lines (self):
        self.init_table("a\tb\nc\td\n")
        assert_that(self.table, has_length(2))
        assert_that(self.table, contains(("a", "b"), ("c", "d")))

    def test_mismatched_column_counts_are_not_allowed (self):
        assert_that(calling(self.init_table).with_args("\t\n\t\t"),
                    raises(RuntimeError))

    def test_empty_table_can_iterate_over_body (self):
        self.init_table()
        assert_that(list(self.table.body()), is_(equal_to([])))

class Given3x3Table (unittest.TestCase):

    def setUp (self):
        self.table = Table("a\tb\tc\nd\te\tf\ng\th\ti\n")

class Given3x3TableWithHeader (Given3x3Table):

    def setUp (self):
        super().setUp()
        self.table.add_header("1", "2", "3")

class Given3x3TableWithOverriddenHeader (Given3x3TableWithHeader):

    def setUp (self):
        super().setUp()
        self.table.add_header("2", "4", "8")

class Test3x3Table (Given3x3Table):

    def test_table_is_internally_consistent (self):
        assert_that(self.table, is_(an_internally_consistent_table()))

    def test_skipping_header_yields_last_two_rows (self):
        assert_that(list(self.table.body()),
                    is_(equal_to([("d", "e", "f"),
                                  ("g", "h", "i")])))

    def test_cannot_add_a_two_column_header (self):
        assert_that(calling(self.table.add_header).with_args("1", "2"),
                    raises(Table.InconsistentColumnCounts))

class Test3x3TableWithHeader (Given3x3TableWithHeader):

    def test_length_is_four (self):
        assert_that(self.table, has_length(4))

    def test_table_is_internally_consistent (self):
        assert_that(self.table, is_(an_internally_consistent_table()))

    def test_skipping_header_yields_original_three_rows (self):
        assert_that(list(self.table.body()),
                    is_(equal_to([("a", "b", "c"),
                                  ("d", "e", "f"),
                                  ("g", "h", "i")])))

    def test_first_row_is_the_header (self):
        assert_that(self.table[0], is_(equal_to(("1", "2", "3"))))

class Test3x3TableWithOverriddenHeader (
        Given3x3TableWithOverriddenHeader):

    def test_adding_a_second_header_does_not_effect_length (self):
        assert_that(self.table, has_length(4))

    def test_first_row_is_the_new_header (self):
        assert_that(self.table[0], is_(equal_to(("2", "4", "8"))))
