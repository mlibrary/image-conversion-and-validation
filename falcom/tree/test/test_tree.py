# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ...test.hamcrest import evaluates_to
from ..read_only_tree import Tree
from ..mutable_tree import MutableTree

class GivenNothing (unittest.TestCase):

    def test_cannot_init_tree_with_value (self):
        assert_that(calling(Tree).with_args(value="hi"),
                    raises(TypeError))

    def test_stores_value_when_inited_with_valued_tree (self):
        mutable = MutableTree(value="hello")
        tree = Tree(mutable)
        assert_that(tree.value, is_(equal_to("hello")))

class GivenEmptyTree (unittest.TestCase):

    def setUp (self):
        self.tree = Tree()

    def test_evaluates_to_false (self):
        assert_that(self.tree, evaluates_to(False))

    def test_has_length_0 (self):
        assert_that(self.tree, has_length(0))

    def test_has_full_length_0 (self):
        assert_that(self.tree.full_length(), is_(equal_to(0)))

    def test_iterates_into_empty_list (self):
        assert_that(list(self.tree), is_(equal_to([])))

    def test_walks_into_empty_list (self):
        assert_that(list(self.tree.walk()), is_(equal_to([])))

    def test_values_iterate_into_empty_list (self):
        assert_that(list(self.tree.values()), is_(equal_to([])))

    def test_values_iterate_into_empty_list (self):
        assert_that(list(self.tree.walk_values()), is_(equal_to([])))

    def test_cannot_get_first_item (self):
        assert_that(calling(lambda t: t[0]).with_args(self.tree),
                    raises(IndexError))

    def test_is_equal_to_self (self):
        assert_that(self.tree, is_(equal_to(self.tree)))

    def test_is_equal_to_other_empty_tree (self):
        assert_that(self.tree, is_(equal_to(Tree())))

    def test_empty_tree_has_null_value (self):
        assert_that(self.tree.value, is_(none()))

    def test_cannot_modify_value_for_empty_tree (self):
        assert_that(calling(setattr).with_args(self.tree,
                                               "value",
                                               "hi"),
                    raises(AttributeError))

class GivenBasedOnMutableTree (unittest.TestCase):

    def setUp (self):
        self.mutable_tree = MutableTree()
        self.tree = Tree(self.mutable_tree)

    def test_evaluates_to_false (self):
        assert_that(self.tree, evaluates_to(False))

    def test_has_length_0 (self):
        assert_that(self.tree, has_length(0))

    def test_modifying_mutable_tree_has_no_effect_on_this_tree (self):
        self.mutable_tree.append_value(5)
        assert_that(self.mutable_tree, has_length(1))
        assert_that(self.tree, has_length(0))

class GivenLayeredTree (unittest.TestCase):

    def make_layered_mutable_tree (self):
        self.mutable_tree = MutableTree(value=1)
        self.mutable_tree.append_value(2)
        self.mutable_tree.append_value(3)
        self.mutable_tree[0].append_value(4)
        self.mutable_tree[0].append_value(5)
        self.mutable_tree[0][0].append_value(6)

    def setUp (self):
        self.make_layered_mutable_tree()
        self.tree = Tree(self.mutable_tree)

    def test_evaluates_to_true (self):
        assert_that(self.tree, evaluates_to(True))

    def test_has_length_2 (self):
        assert_that(self.tree, has_length(2))

    def test_has_full_length_5 (self):
        assert_that(self.tree.full_length(), is_(equal_to(5)))

    def test_iterates_into_list_of_children (self):
        children = list(self.tree)
        assert_that(children[0].value, is_(equal_to(2)))
        assert_that(children[1].value, is_(equal_to(3)))

        assert_that(children[0], has_length(2))
        assert_that(children[0].full_length(), is_(equal_to(3)))

    def test_walks_into_list_of_descendants (self):
        descendants = list(self.tree.walk())
        assert_that(descendants[0].value, is_(equal_to(2)))
