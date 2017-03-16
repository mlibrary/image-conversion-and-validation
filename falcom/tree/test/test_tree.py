# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ...test.hamcrest import evaluates_to
from .matchers import *
from ..mutable_tree import MutableTree

class GivenEmptyTree:

    def setUp (self):
        self.tree = MutableTree()

    def set_value (self, value):
        self.tree.value = value

class GivenTreeWithOneEmptyChild (GivenEmptyTree):

    def setUp (self):
        super().setUp()
        self.tree.insert(0, MutableTree())

class TestEmptyTree (GivenEmptyTree, unittest.TestCase):

    def test_evaluates_to_false (self):
        assert_that(self.tree, evaluates_to(False))

    def test_has_length_of_0 (self):
        assert_that(self.tree, has_length(0))

    def test_has_total_length_of_0 (self):
        assert_that(self.tree, has_full_length(0))

    def test_iterates_into_empty_list (self):
        assert_that(self.tree, iterates_into_list([]))

    def test_walk_iterates_into_empty_list (self):
        assert_that(self.tree, iterates_recursively_into_list([]))

    def test_has_no_first_item (self):
        assert_that(calling(lambda x: x[0]).with_args(self.tree),
                    raises(IndexError))

    def test_value_is_none (self):
        assert_that(self.tree, has_node_value(None))

    def test_can_modify_value (self):
        self.set_value("hello")
        assert_that(self.tree, has_node_value("hello"))

        self.set_value(235813)
        assert_that(self.tree, has_node_value(235813))

    def test_cannot_delete_value (self):
        assert_that(calling(delattr).with_args(self.tree, "value"),
                    raises(AttributeError))

    def test_when_value_changes_it_still_cannot_be_deleted (self):
        self.set_value("hello")
        assert_that(calling(delattr).with_args(self.tree, "value"),
                    raises(AttributeError))

class TestTreeWithOneEmptyChild (GivenTreeWithOneEmptyChild,
                                 unittest.TestCase):

    def test_has_length_of_1 (self):
        assert_that(self.tree, has_length(1))
