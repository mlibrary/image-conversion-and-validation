# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ..test.hamcrest import ComposedMatcher, evaluates_to, a_method
from .try_forever import try_forever, TryForever

class FailThenSucceed:

    def __init__ (self, number_of_failures, error = RuntimeError):
        self.countdown = number_of_failures
        self.error = error

    def __call__ (self):
        if self.__we_need_to_raise_an_error():
            self.__decrement_counter_and_raise_the_error()

    def __we_need_to_raise_an_error (self):
        return self.countdown > 0

    def __decrement_counter_and_raise_the_error (self):
        self.countdown -= 1
        raise self.error

class DecoratorTest (unittest.TestCase):

    def test_can_set_decorator (self):
        @try_forever
        def method():
            pass

        method()

class TryForeverClassTest (unittest.TestCase):

    def test_try_forever_returns_object (self):
        obj = TryForever()

class FailThenSucceedTest (unittest.TestCase):

    def test_we_can_fail_then_succeed (self):
        method = FailThenSucceed(5)
        for i in range(5):
            assert_that(calling(method), raises(RuntimeError))

        method() # raises no exception this time

    def test_we_can_use_any_error (self):
        method = FailThenSucceed(1, KeyError)
        assert_that(calling(method), raises(KeyError))
        method() # raises no exception this time
