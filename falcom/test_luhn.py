# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .luhn import get_check_digit

class LuhnTest (unittest.TestCase):

    def test_empty_yields_null (self):
        digit = get_check_digit()
        assert_that(digit, is_(none()))

    def test_null_yields_null (self):
        digit = get_check_digit(None)
