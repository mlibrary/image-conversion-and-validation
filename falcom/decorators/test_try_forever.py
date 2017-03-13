# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ..test.hamcrest import ComposedMatcher, evaluates_to
from .try_forever import try_forever

class NothingTest (unittest.TestCase):

    def test_nothing (self): pass
