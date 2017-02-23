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

    def test_has_length_of_zero (self):
        assert_that(self.tree, has_length(0))

    def test_has_total_length_of_zero (self):
        assert_that(self.tree.full_length(), is_(equal_to(0)))

    def test_iterates_into_empty_list (self):
        assert_that(list(self.tree), is_(equal_to([])))

    def test_walk_iterates_into_empty_list (self):
        assert_that(list(self.tree.walk()), is_(equal_to([])))

    def test_has_no_first_item (self):
        assert_that(calling(lambda x: x[0]).with_args(self.tree),
                    raises(IndexError))
