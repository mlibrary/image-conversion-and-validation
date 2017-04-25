# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ..generate_pageview import Pagetags

class TestPagetags (unittest.TestCase):

    def test_can_init_pagetags (self):
        tags = Pagetags()
        assert_that(tags.generate_pageview(), is_(equal_to("")))
