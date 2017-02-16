# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedMatcher, \
        evaluates_to_false, evaluates_to_true
from ..config import Config

class GivenEmptyConfig (unittest.TestCase):

    def setUp (self):
        self.config = Config()

    def test_can_init_config (self):
        assert_that(self.config, evaluates_to_false())
        assert_that(self.config, has_length(0))

    def test_default_key_is_default (self):
        assert_that(self.config.default_key, is_(equal_to("default")))
