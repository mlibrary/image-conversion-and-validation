# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedMatcher, evaluates_to
from ..config import Config

class GivenEmptyConfig (unittest.TestCase):

    def setUp (self):
        self.config = Config()

    def test_evaluates_to_false (self):
        assert_that(self.config, evaluates_to(False))

    def test_has_zero_length (self):
        assert_that(self.config, has_length(0))

    def test_default_key_is_default (self):
        assert_that(self.config.default_key, is_(equal_to("default")))

    def test_default_key_is_in_there (self):
        assert_that(self.config.default_key in self.config,
                    "{} in {}".format(repr(self.config.default_key),
                                      repr(self.config)))

    def test_default_dict_is_empty (self):
        assert_that(dict(self.config.default), is_(equal_to({})))

    def test_default_dict_can_be_accessed_by_key (self):
        direct_accession = self.config.default
        key_accession = self.config[self.config.default_key]

        assert_that(key_accession, is_(equal_to(direct_accession)))

    def test_is_iterable (self):
        assert_that(list(self.config), is_(equal_to([])))

    def test_no_other_keys_exist (self):
        other_key = "not" + self.config.default_key
        assert_that(other_key not in self.config,
                    "{} not in {}".format(repr(other_key),
                                          repr(self.config)))
