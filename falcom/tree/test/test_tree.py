# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ..read_only_tree import Tree

class GivenNothing (unittest.TestCase):

    def test_can_init_tree (self):
        t = Tree()

    def test_cannot_init_tree_with_value (self):
        assert_that(calling(Tree).with_args(value="hi"),
                    raises(TypeError))
