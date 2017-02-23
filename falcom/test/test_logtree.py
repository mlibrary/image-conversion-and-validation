# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import evaluates_to_false
from ..logtree import MutableTree

class GivenEmptyTree (unittest.TestCase):

    def setUp (self):
        self.tree = MutableTree()

    def test_tree_has_repr (self):
        assert_that(repr(self.tree), starts_with("<MutableTree"))

    def test_evaluates_to_false (self):
        assert_that(self.tree, evaluates_to_false())
