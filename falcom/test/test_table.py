# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedMatcher, \
        evaluates_to_false, evaluates_to_true
from ..table import Table

class an_empty_table (ComposedMatcher):

    def assertion (self, item):
        yield item, evaluates_to_false()
        yield item, has_length(0)
        yield item.rows, is_(equal_to(0))
        yield item.cols, is_(equal_to(0))
        yield list(item), is_(equal_to([]))
        yield calling(lambda t: t[0]).with_args(item), \
              raises(IndexError)

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

    def test_single_char_yields_1_row_1_col (self):
        table = Table("a")
        assert_that(table, evaluates_to_true())
        assert_that(table, has_length(1))
        assert_that(table.rows, is_(equal_to(1)))
        assert_that(table.cols, is_(equal_to(1)))
        assert_that(list(table), is_(equal_to([("a",)])))
