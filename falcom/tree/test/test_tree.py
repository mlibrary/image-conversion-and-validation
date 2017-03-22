# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ..read_only_tree import Tree
from ..mutable_tree import MutableTree

class GivenNothing (unittest.TestCase):

    def test_can_init_tree (self):
        t = Tree()

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
