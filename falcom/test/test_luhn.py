# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedMatcher, evaluates_to
from ..luhn import get_check_digit, verify_check_digit, LuhnNumber

class yields_null_check_digit (ComposedMatcher):

    def assertion (self, item):
        digit = get_check_digit(item)
        yield digit, is_(none())

class yields_check_digit (ComposedMatcher):

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

    def test_float_yields_null (self):
        assert_that(5.5, yields_null_check_digit())

    def test_non_int_str_yields_null (self):
        assert_that("B637281", yields_null_check_digit())

    def test_zero_yields_zero (self):
        assert_that(0, yields_check_digit(0))

    def test_single_digits (self):
        assert_that("0", yields_check_digit(0))
        assert_that("1", yields_check_digit(8))
        assert_that("2", yields_check_digit(6))
        assert_that("3", yields_check_digit(4))
        assert_that("4", yields_check_digit(2))
        assert_that("5", yields_check_digit(9))
        assert_that("6", yields_check_digit(7))
        assert_that("7", yields_check_digit(5))
        assert_that("8", yields_check_digit(3))
        assert_that("9", yields_check_digit(1))

    def test_double_digits (self):
        assert_that("10", yields_check_digit(9))
        assert_that("11", yields_check_digit(7))
        assert_that("12", yields_check_digit(5))
        assert_that("13", yields_check_digit(3))
        assert_that("14", yields_check_digit(1))
        assert_that("15", yields_check_digit(8))
        assert_that("16", yields_check_digit(6))
        assert_that("17", yields_check_digit(4))
        assert_that("18", yields_check_digit(2))
        assert_that("19", yields_check_digit(0))

        assert_that("22", yields_check_digit(4))
        assert_that("32", yields_check_digit(3))
        assert_that("42", yields_check_digit(2))
        assert_that("52", yields_check_digit(1))
        assert_that("62", yields_check_digit(0))
        assert_that("72", yields_check_digit(9))
        assert_that("82", yields_check_digit(8))
        assert_that("92", yields_check_digit(7))

        assert_that("27", yields_check_digit(3))
        assert_that("37", yields_check_digit(2))
        assert_that("47", yields_check_digit(1))
        assert_that("57", yields_check_digit(0))
        assert_that("67", yields_check_digit(9))
        assert_that("77", yields_check_digit(8))
        assert_that("87", yields_check_digit(7))
        assert_that("97", yields_check_digit(6))

    def test_some_example_barcodes (self):
        assert_that(3901507463984, yields_check_digit(3))
        assert_that(3901507463986, yields_check_digit(8))
        assert_that(3901508742754, yields_check_digit(1))

class CheckDigitVerifiesAs (ComposedMatcher):

    def __init__ (self, expected):
        self.__expected = expected

    def assertion (self, item):
        yield verify_check_digit(item), equal_to(self.__expected)

def an_invalid_luhn_number():
    return CheckDigitVerifiesAs(False)

def a_valid_luhn_number():
    return CheckDigitVerifiesAs(True)

class VerifyTest (unittest.TestCase):

    def test_empty_yields_false (self):
        assert_that(verify_check_digit(), is_(equal_to(False)))

    def test_null_yields_false (self):
        assert_that(None, is_(an_invalid_luhn_number()))

    def test_empty_str_yields_false (self):
        assert_that("", is_(an_invalid_luhn_number()))

    def test_non_int_str_yields_false (self):
        assert_that("B127380", is_(an_invalid_luhn_number()))

    def test_single_digit_yields_false (self):
        for i in range(1, 10):
            assert_that(i, is_(an_invalid_luhn_number()))

    def test_zero_is_valid (self):
        assert_that(0, is_(a_valid_luhn_number()))
        assert_that("0", is_(a_valid_luhn_number()))

    def test_some_valid_double_digits (self):
        assert_that(18, is_(a_valid_luhn_number()))
        assert_that(26, is_(a_valid_luhn_number()))
        assert_that(34, is_(a_valid_luhn_number()))
        assert_that(42, is_(a_valid_luhn_number()))
        assert_that(59, is_(a_valid_luhn_number()))
        assert_that(67, is_(a_valid_luhn_number()))
        assert_that(75, is_(a_valid_luhn_number()))
        assert_that(83, is_(a_valid_luhn_number()))
        assert_that(91, is_(a_valid_luhn_number()))

    def test_some_invalid_double_digits (self):
        assert_that(11, is_(an_invalid_luhn_number()))
        assert_that(22, is_(an_invalid_luhn_number()))
        assert_that(33, is_(an_invalid_luhn_number()))
        assert_that(44, is_(an_invalid_luhn_number()))

class invalid_luhn_number_input (ComposedMatcher):

    def assertion (self, item):
        obj = LuhnNumber(item)
        yield obj, evaluates_to(False)

class LuhnNumberClassTest (unittest.TestCase):

    def test_no_args (self):
        obj = LuhnNumber()
        assert_that(obj, evaluates_to(False))

    def test_null (self):
        assert_that(None, is_(invalid_luhn_number_input()))

    def test_empty_str (self):
        assert_that("", is_(invalid_luhn_number_input()))

    def test_invalid_str (self):
        assert_that("B9032", is_(invalid_luhn_number_input()))

    def test_float (self):
        assert_that(41.7, is_(invalid_luhn_number_input()))

    def test_zero (self):
        assert_that(LuhnNumber(0), evaluates_to(True))
        assert_that(LuhnNumber("0"), evaluates_to(True))

    def test_one (self):
        assert_that(LuhnNumber(1), evaluates_to(True))
        assert_that(LuhnNumber("1"), evaluates_to(True))
