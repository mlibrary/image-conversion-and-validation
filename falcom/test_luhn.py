# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedAssertion
from .luhn import get_check_digit

class yields_null_check_digit (ComposedAssertion):

    def assertion (self, item):
        digit = get_check_digit(item)
        yield digit, is_(none())

class yields_check_digit (ComposedAssertion):

    def __init__ (self, digit):
        self.digit = digit

    def assertion (self, item):
        yield get_check_digit(item), is_(equal_to(self.digit))

class LuhnTest (unittest.TestCase):

    def test_empty_yields_null (self):
        digit = get_check_digit()
        assert_that(digit, is_(none()))

    def test_null_yields_null (self):
        assert_that(None, yields_null_check_digit())

    def test_empty_str_yields_null (self):
        assert_that("", yields_null_check_digit())

    def test_single_digits (self):
        assert_that("0", yields_check_digit(0))
