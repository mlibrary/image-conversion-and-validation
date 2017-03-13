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
        def method (arg):
            return arg

        assert_that(method(5), is_(equal_to(5)))
        assert_that(method("hi"), is_(equal_to("hi")))

class GivenDefaultTryForeverDecorator (unittest.TestCase):

    def setUp (self):
        self.decorator = TryForever()

    def test_is_callable (self):
        assert_that(self.decorator, is_(a_method()))

    def test_will_wait_one_minute (self):
        assert_that(self.decorator.seconds_between_attempts,
                    is_(equal_to(60)))

    def test_will_catch_any_normal_exception (self):
        assert_that(self.decorator.base_error, is_(equal_to(Exception)))

    def test_will_loop_without_limit (self):
        assert_that(self.decorator.limit, is_(equal_to(0)))

    def test_can_be_used_as_a_decorator (self):
        @self.decorator
        def return_five():
            return 5

        assert_that(return_five(), is_(equal_to(5)))

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
