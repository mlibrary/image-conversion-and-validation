# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedAssertion, \
        evaluates_to_false, evaluates_to_true
from ..table import Table

class an_empty_table (ComposedAssertion):

    def assertion (self, item):
        yield item, evaluates_to_false()
        yield item, has_length(0)
        yield item.rows, is_(equal_to(0))
        yield item.cols, is_(equal_to(0))
        yield list(item), is_(equal_to([]))
        yield calling(lambda t: t[0]).with_args(item), \
              raises(IndexError)

class TableTest (unittest.TestCase):

    def test_degenerate (self):
        table = Table()
        assert_that(table, is_(an_empty_table()))
