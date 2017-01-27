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
