# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ..generate_pageview import Pagetags

class GivenEmptyPagetags (unittest.TestCase):

    def setUp (self):
        self.tags = Pagetags()

    def test_can_init_pagetags (self):
        assert_that(self.tags.generate_pageview(), is_(equal_to("")))

    def test_can_add_tags (self):
        self.tags.add_raw_tags({"tags": []})
