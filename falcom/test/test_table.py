# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedMatcher, \
        evaluates_to_false, evaluates_to_true
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
            yield item, evaluates_to_true()

        else:
            yield item, evaluates_to_false()

        yield item, has_length(i), "length matches iteration"
        yield item.rows, is_(equal_to(i)), "row count"
        yield item.cols, is_(equal_to(expected_cols)), "column count"

        yield calling(lambda t: t[i]).with_args(item), \
              raises(IndexError), "no row with index {}".format(i)

class an_empty_table (ComposedMatcher):

    def assertion (self, item):
        yield item, is_(an_internally_consistent_table())
        yield item, evaluates_to_false()

class yields_an_empty_table (ComposedMatcher):

    def assertion (self, item):
        table = Table(item)
        yield table, is_(an_empty_table())

class TableTest (unittest.TestCase):

    def test_degenerate (self):
        assert_that(Table(), is_(an_empty_table()))

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
        table = Table("a")
        assert_that(table, is_(an_internally_consistent_table()))
        assert_that(table, has_length(1))
        assert_that(table[0][0], is_(equal_to("a")))

    def test_HT_divides_2_columns (self):
        table = Table("a\tb")
        assert_that(table, is_(an_internally_consistent_table()))
        assert_that(table, has_length(1))
        assert_that(table.cols, is_(equal_to(2)))
        assert_that(table[0], contains("a", "b"))

    def test_HT_divides_3_columns (self):
        table = Table("a\tb\tc")
        assert_that(table, is_(an_internally_consistent_table()))
        assert_that(table, has_length(1))
        assert_that(table.cols, is_(equal_to(3)))
        assert_that(table[0], contains("a", "b", "c"))

    def test_2_rows_2_cols (self):
        table = Table("a\tb\nc\td")
        assert_that(table, is_(an_internally_consistent_table()))
        assert_that(table, has_length(2))
        assert_that(table, contains(("a", "b"), ("c", "d")))
