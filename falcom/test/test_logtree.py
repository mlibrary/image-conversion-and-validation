# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
import unittest

from .hamcrest import evaluates_to
from ..logtree import MutableTree

class TreeMatcher (BaseMatcher):

    def __init__ (self, expected_value):
        self.expected_value = expected_value

    def describe_to (self, description):
        description.append_text(
                self.expectation.format(repr(self.expected_value)))

class has_full_length (TreeMatcher):
    expectation = "a tree with a full length of {}"

    def _matches (self, item):
        return item.full_length() == self.expected_value

class iterates_into_list (TreeMatcher):
    expectation = "a tree that iterates into {}"

    def _matches (self, item):
        return list(item) == self.expected_value

class iterates_recursively_into_list (TreeMatcher):
    expectation = "a tree that iterates recursively into {}"

    def _matches (self, item):
        return list(item.walk()) == self.expected_value

class has_value (TreeMatcher):
    expectation = "a tree node with a value of {}"

    def _matches (self, item):
        return item.value == self.expected_value

class GivenEmptyTree (unittest.TestCase):

    def setUp (self):
        self.tree = MutableTree()

    def set_value (self, value):
        self.tree.value = value

    def test_evaluates_to_false (self):
        assert_that(self.tree, evaluates_to(False))

    def test_has_length_of_zero (self):
        assert_that(self.tree, has_length(0))

    def test_has_total_length_of_zero (self):
        assert_that(self.tree, has_full_length(0))

    def test_iterates_into_empty_list (self):
        assert_that(self.tree, iterates_into_list([]))

    def test_walk_iterates_into_empty_list (self):
        assert_that(self.tree, iterates_recursively_into_list([]))

    def test_has_no_first_item (self):
        assert_that(calling(lambda x: x[0]).with_args(self.tree),
                    raises(IndexError))

    def test_value_is_none (self):
        assert_that(self.tree, has_value(None))

    def test_can_modify_value (self):
        self.set_value("hello")
        assert_that(self.tree, has_value("hello"))

        self.set_value(235813)
        assert_that(self.tree, has_value(235813))

    def test_cannot_delete_value (self):
        assert_that(calling(delattr).with_args(self.tree, "value"),
                    raises(AttributeError))

    def test_when_value_changes_it_still_cannot_be_deleted (self):
        self.set_value("hello")
        assert_that(calling(delattr).with_args(self.tree, "value"),
                    raises(AttributeError))

    def test_when_inserted_child_node_length_is_1 (self):
        self.tree.insert(0, MutableTree())
        assert_that(self.tree, has_length(1))
