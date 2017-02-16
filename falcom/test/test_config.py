# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedMatcher, \
        evaluates_to_false, evaluates_to_true
from ..config import Config

class GivenNothing (unittest.TestCase):

    def test_can_init_config (self):
        config = Config()
        assert_that(config, evaluates_to_false())
