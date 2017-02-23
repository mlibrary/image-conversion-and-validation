# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ..logtree import Tree

class TreeTest (unittest.TestCase):

    def test_degenerate (self):
        t = Tree()
        assert_that(repr(t), starts_with("<Tree"))
