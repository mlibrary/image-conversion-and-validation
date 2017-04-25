# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ..generate_pageview import Pagetags

class GivenEmptyPagetags (unittest.TestCase):

    def setUp (self):
        self.tags = Pagetags()

    def test_can_generate_pageview (self):
        assert_that(self.tags.generate_pageview(), is_(equal_to("")))

    def test_default_confidence_is_100 (self):
        assert_that(self.tags.default_confidence, is_(equal_to(100)))

    def test_can_alter_default_confidence (self):
        for confid in (900, 100, 444):
            self.tags.default_confidence = confid
            assert_that(self.tags.default_confidence,
                        is_(equal_to(confid)))

    def test_cannot_set_confidence_to_weird_values (self):
        for confid in (0, 99, 901, 1000, 500.5, "500"):
            assert_that(calling(setattr).with_args(self.tags,
                                                   "default_confidence",
                                                   confid),
                        raises(ValueError))

    def test_can_add_tags (self):
        self.tags.add_raw_tags({"tags": []})

    def test_cannot_add_tag_data_when_missing_tags (self):
        for data in ({}, {"hi": "hello"}):
            assert_that(calling(self.tags.add_raw_tags).with_args(data),
                        raises(ValueError))

    def test_outputs_pages_as_given (self):
        self.tags.add_raw_tags(
                {"tags": [{"number": "1", "feature": "TITLE"},
                          {"number": "2", "feature": ""},
                          {"number": "c", "feature": "INDEX"}]})

        assert_that(self.tags.generate_pageview(),
                    is_(equal_to("\n".join((
                        "00000001.tif\t00000001\t00000001\t100\tTITLE",
                        "00000002.tif\t00000002\t00000002\t100\t",
                        "00000003.tif\t00000003\t0000000c\t100\tINDEX")
                    ))))
