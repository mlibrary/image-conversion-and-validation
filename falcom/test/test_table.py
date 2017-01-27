# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedAssertion, \
        evaluates_to_false, evaluates_to_true
from ..table import Table

class TableTest (unittest.TestCase):

    def test_degenerate (self):
        table = Table()
        assert_that(table, evaluates_to_false())
        assert_that(table, has_length(0))
        assert_that(table.rows, is_(equal_to(0)))
        assert_that(table.cols, is_(equal_to(0)))
        assert_that(list(table), is_(equal_to([])))
        assert_that(calling(lambda t: t[0]).with_args(table),
                    raises(IndexError))
