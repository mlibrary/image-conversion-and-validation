# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import evaluates_to_false
from ..logtree import Tree

class GivenEmptyTree (unittest.TestCase):

    def setUp (self):
        self.tree = Tree()

    def test_tree_has_repr (self):
        assert_that(repr(self.tree), starts_with("<Tree"))

    def test_evaluates_to_false (self):
        assert_that(self.tree, evaluates_to_false())
