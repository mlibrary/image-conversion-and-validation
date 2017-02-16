# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedMatcher, \
        evaluates_to_false, evaluates_to_true

class NothingTest (unittest.TestCase):

    def test_working_environment (self):
        pass
