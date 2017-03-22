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

    def test_can_init_from_mutable_tree (self):
        mtree = MutableTree(value=1)
        mtree.append_value(2)
        mtree.append_value(3)
        mtree[0].append_value(4)
        mtree[0].append_value(5)
        mtree[0][0].append_value(6)

        t = Tree(mtree)

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

    def test_empty_tree_has_null_value (self):
        assert_that(self.tree.value, is_(none()))

    def test_cannot_modify_value_for_empty_tree (self):
        assert_that(calling(setattr).with_args(self.tree,
                                               "value",
                                               "hi"),
                    raises(AttributeError))
