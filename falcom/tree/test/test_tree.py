# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ...test.hamcrest import evaluates_to
from .matchers import *
from ..mutable_tree import MutableTree

class TreeHelpers:

    def new_tree (self):
        return MutableTree()

    def set_value (self, value):
        self.tree.value = value

    def assert_tree (self, matcher):
        assert_that(self.tree, matcher)

class GivenEmptyTree (TreeHelpers):

    def setUp (self):
        self.tree = self.new_tree()

class GivenTreeWithOneEmptyChild (GivenEmptyTree):

    def setUp (self):
        super().setUp()

        self.child = self.new_tree()
        self.tree.insert(0, self.child)

class TestEmptyTree (GivenEmptyTree, unittest.TestCase):

    def test_evaluates_to_false (self):
        self.assert_tree(evaluates_to(False))

    def test_has_length_of_0 (self):
        self.assert_tree(has_length(0))

    def test_has_full_length_of_0 (self):
        self.assert_tree(has_full_length(0))

    def test_iterates_into_empty_list (self):
        self.assert_tree(iterates_into_list([]))

    def test_walk_iterates_into_empty_list (self):
        self.assert_tree(walks_into_list([]))

    def test_has_no_first_item (self):
        assert_that(calling(lambda x: x[0]).with_args(self.tree),
                    raises(IndexError))

    def test_value_is_none (self):
        self.assert_tree(has_node_value(None))

    def test_can_modify_value (self):
        self.set_value("hello")
        self.assert_tree(has_node_value("hello"))

        self.set_value(235813)
        self.assert_tree(has_node_value(235813))

    def test_cannot_delete_value (self):
        assert_that(calling(delattr).with_args(self.tree, "value"),
                    raises(AttributeError))

    def test_when_value_changes_it_still_cannot_be_deleted (self):
        self.set_value("hello")
        assert_that(calling(delattr).with_args(self.tree, "value"),
                    raises(AttributeError))

class TestTreeWithOneEmptyChild (GivenTreeWithOneEmptyChild,
                                 unittest.TestCase):

    def test_evaluates_to_true (self):
        self.assert_tree(evaluates_to(True))

    def test_value_is_none (self):
        self.assert_tree(has_node_value(None))

    def test_has_length_of_1 (self):
        self.assert_tree(has_length(1))

    def test_has_full_length_of_1 (self):
        self.assert_tree(has_full_length(1))

    def test_first_item_is_child (self):
        assert_that(self.tree[0], is_(same_instance(self.child)))

    def test_there_is_no_second_item (self):
        assert_that(calling(lambda x: x[1]).with_args(self.tree),
                    raises(IndexError))

    def test_iterates_into_list_with_child (self):
        self.assert_tree(iterates_into_list([self.child]))

    def test_walks_into_list_with_child (self):
        self.assert_tree(walks_into_list([self.child]))

    def test_child_has_length_of_0 (self):
        assert_that(self.child, has_length(0))

    def test_child_has_full_length_of_0 (self):
        assert_that(self.child, has_full_length(0))
