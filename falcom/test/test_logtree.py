# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import evaluates_to_false
from ..logtree import Tree

class TreeTest (unittest.TestCase):

    def test_tree_is_a_class (self):
        t = Tree()
        assert_that(repr(t), starts_with("<Tree"))

    def test_empty_tree_is_false (self):
        t = Tree()
        assert_that(t, evaluates_to_false())
