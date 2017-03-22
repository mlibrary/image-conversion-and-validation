# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ...test.hamcrest import evaluates_to
from .matchers import has_full_length, \
                      iterates_into_list, \
                      walks_into_list, \
                      has_node_value
from ..mutable_tree import MutableTree

class TreeHelpers:

    def new_tree (self, value = None):
        return MutableTree(value=value)

    def tree_copy (self, tree):
        return MutableTree(tree)

    def set_value (self, value):
        self.tree.value = value

    def assert_tree (self, matcher):
        assert_that(self.tree, matcher)

    def assert_invalid_index (self, index):
        assert_that(calling(lambda x: x[index]).with_args(self.tree),
                    raises(IndexError))

class GivenEmptyTree (TreeHelpers):

    def setUp (self):
        self.tree = self.new_tree()

    def test_when_initing_new_tree_we_get_a_deep_copy (self):
        copy = self.tree_copy(self.tree)
        assert_that(copy, is_(equal_to(self.tree)))

    def test_cannot_init_new_tree_with_both_tree_and_value (self):
        assert_that(calling(MutableTree).with_args(self.tree, None),
                    raises(TypeError))
        assert_that(calling(MutableTree).with_args(self.tree, value=None),
                    raises(TypeError))

class GivenTreeWithOneEmptyChild (GivenEmptyTree):

    def setUp (self):
        super().setUp()

        self.first_child = self.new_tree(1)
        self.tree.insert_tree(0, self.first_child)

    def test_first_child_has_value_of_1 (self):
        assert_that(self.first_child, has_node_value(1))

class GivenTreeWithTwoEmptyChildren (GivenTreeWithOneEmptyChild):

    def setUp (self):
        super().setUp()

        self.second_child = self.new_tree(2)
        self.tree.insert_tree(1, self.second_child)

    def test_second_child_has_value_of_2 (self):
        assert_that(self.second_child, has_node_value(2))

class GivenTreeWithTwoChildrenAndOneGrandchild (
        GivenTreeWithTwoEmptyChildren):

    def setUp (self):
        super().setUp()

        self.grandchild = self.new_tree(3)
        self.first_child.insert_tree(0, self.grandchild)

    def test_grandchild_has_value_of_3 (self):
        assert_that(self.grandchild, has_node_value(3))

class GivenTreeWithTwoChildrenAndOneGreatGrandchild (
        GivenTreeWithTwoChildrenAndOneGrandchild):

    def setUp (self):
        super().setUp()

        self.great_grandchild = self.new_tree(4)
        self.grandchild.insert_tree(0, self.great_grandchild)

    def test_great_grandchild_has_value_of_3 (self):
        assert_that(self.great_grandchild, has_node_value(4))

class TestGivenNothing (unittest.TestCase):

    def test_can_init_tree_with_value (self):
        tree = MutableTree(value="hi")
        assert_that(tree, has_node_value("hi"))

    def test_cannot_init_new_tree_with_unexpected_kwarg (self):
        assert_that(calling(MutableTree).with_args(weird="bad"),
                    raises(TypeError))

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

    def test_values_iterate_into_empty_list (self):
        assert_that(list(self.tree.values()), is_(equal_to([])))

    def test_values_walk_into_empty_list (self):
        assert_that(list(self.tree.walk_values()), is_(equal_to([])))

    def test_has_no_first_item (self):
        self.assert_invalid_index(0)

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

    def test_can_insert_value (self):
        self.tree.insert_value(0, 7)
        self.assert_tree(has_length(1))
        assert_that(self.tree[0], has_node_value(7))

    def test_can_append_value (self):
        self.tree.append_value(12)
        self.assert_tree(has_length(1))
        assert_that(self.tree[0], has_node_value(12))

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
        assert_that(self.tree[0], is_(same_instance(self.first_child)))

    def test_there_is_no_second_item (self):
        self.assert_invalid_index(1)

    def test_iterates_into_list_with_child (self):
        self.assert_tree(iterates_into_list([self.first_child]))

    def test_walks_into_list_with_child (self):
        self.assert_tree(walks_into_list([self.first_child]))

    def test_child_has_length_of_0 (self):
        assert_that(self.first_child, has_length(0))

    def test_child_has_full_length_of_0 (self):
        assert_that(self.first_child, has_full_length(0))

class TestTreeWithTwoEmptyChildren (GivenTreeWithTwoEmptyChildren,
                                    unittest.TestCase):

    def test_evaluates_to_true (self):
        self.assert_tree(evaluates_to(True))

    def test_has_length_of_2 (self):
        self.assert_tree(has_length(2))

    def test_has_full_length_of_2 (self):
        self.assert_tree(has_full_length(2))

    def test_can_get_second_child_by_index (self):
        assert_that(self.tree[1], is_(same_instance(self.second_child)))

    def test_there_is_no_third_item (self):
        self.assert_invalid_index(2)

    def test_iterates_into_list_with_children (self):
        self.assert_tree(iterates_into_list([self.first_child,
                                             self.second_child]))

    def test_walks_into_list_with_children (self):
        self.assert_tree(walks_into_list([self.first_child,
                                          self.second_child]))

class TestTreeWithTwoChildrenAndOneGrandchild (
        GivenTreeWithTwoChildrenAndOneGrandchild,
        unittest.TestCase):

    def test_has_length_of_2 (self):
        self.assert_tree(has_length(2))

    def test_has_full_length_of_3 (self):
        self.assert_tree(has_full_length(3))

    def test_iterates_into_list_of_both_children (self):
        self.assert_tree(iterates_into_list([self.first_child,
                                             self.second_child]))

    def test_walks_into_list_with_all_descendants (self):
        self.assert_tree(walks_into_list([self.first_child,
                                          self.grandchild,
                                          self.second_child]))

class TestTreeWithTwoChildrenAndOneGreatGrandchild (
        GivenTreeWithTwoChildrenAndOneGreatGrandchild,
        unittest.TestCase):

    def test_has_length_of_2 (self):
        self.assert_tree(has_length(2))

    def test_has_full_length_of_4 (self):
        self.assert_tree(has_full_length(4))

    def test_iterates_into_list_of_both_children (self):
        self.assert_tree(iterates_into_list([self.first_child,
                                             self.second_child]))

    def test_walks_into_list_with_all_descendants (self):
        self.assert_tree(walks_into_list([self.first_child,
                                          self.grandchild,
                                          self.great_grandchild,
                                          self.second_child]))

    def test_values_iterate_through_immediate_children_only (self):
        assert_that(list(self.tree.values()), is_(equal_to([1, 2])))

    def test_values_walk_through_all_descendents (self):
        assert_that(list(self.tree.walk_values()),
                    is_(equal_to([1, 3, 4, 2])))

    def test_can_append_nodes (self):
        self.tree.append_tree(self.new_tree("append"))
        self.assert_tree(has_length(3))
