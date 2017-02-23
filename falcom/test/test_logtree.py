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

    def test_value_is_none (self):
        assert_that(self.tree.value, is_(none()))

    def test_can_modify_value (self):
        self.tree.value = "hello"
        assert_that(self.tree.value, is_(equal_to("hello")))

        self.tree.value = 235813
        assert_that(self.tree.value, is_(equal_to(235813)))

    def test_cannot_delete_value (self):
        assert_that(calling(delattr).with_args(self.tree, "value"),
                    raises(AttributeError))

    def test_when_value_changes_it_still_cannot_be_deleted (self):
        self.tree.value = "hello"
        assert_that(calling(delattr).with_args(self.tree, "value"),
                    raises(AttributeError))
