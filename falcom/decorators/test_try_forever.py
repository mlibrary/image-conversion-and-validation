# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from ..test.hamcrest import ComposedMatcher, evaluates_to, a_method
from .try_forever import try_forever

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

    def test_returns_object_without_positional_args (self):
        obj = try_forever()

    def test_raises_exception_with_too_many_arguments (self):
        assert_that(calling(try_forever).with_args(1, 2),
                    raises(TypeError))

    def test_can_set_limit (self):
        obj = try_forever(limit=4)
        assert_that(obj.limit, is_(equal_to(4)))

    def test_can_set_error (self):
        obj = try_forever(base_error=RuntimeError)
        assert_that(obj.base_error, is_(equal_to(RuntimeError)))

    def test_can_set_pause_seconds (self):
        obj = try_forever(seconds_between_attempts=2.5)
        assert_that(obj.seconds_between_attempts,
                    is_(close_to(2.5, 0.001)))

    def test_can_set_pause_minutes (self):
        obj = try_forever(minutes_between_attempts=5)
        assert_that(obj.seconds_between_attempts, is_(equal_to(300)))

    def test_can_set_pause_to_fractions_of_minutes (self):
        obj = try_forever(minutes_between_attempts=2.5)
        assert_that(obj.seconds_between_attempts,
                    is_(close_to(150, 0.001)))

    def test_can_set_pause_to_hours (self):
        obj = try_forever(hours_between_attempts=2)
        assert_that(obj.seconds_between_attempts, is_(equal_to(7200)))

    def test_cannot_set_minutes_and_seconds (self):
        assert_that(calling(try_forever)
                    .with_args(seconds_between_attempts=10,
                               minutes_between_attempts=5),
                    raises(TypeError))

    def test_unknown_kwargs_raise_error (self):
        assert_that(calling(try_forever).with_args(hello="sup"),
                    raises(TypeError))

class GivenDefaultTryForeverDecorator (unittest.TestCase):

    def setUp (self):
        self.decorator = try_forever()

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

class GivenMethodThatFailsThreeTimes (unittest.TestCase):

    def setUp (self):
        self.tough_method = FailThenSucceed(3)

    def init_looper (self, limit = 0, error = Exception):
        decorator = try_forever(limit=limit,
                                base_error=error,
                                seconds_between_attempts=0.001)
        return decorator(self.tough_method)

    def test_can_run_without_seeing_errors (self):
        looper = self.init_looper()
        looper() # raises no exception

    def test_fails_with_limit_of_three (self):
        looper = self.init_looper(3)
        assert_that(calling(looper), raises(RuntimeError))

    def test_succeeds_with_limit_of_four (self):
        looper = self.init_looper(4)
        looper() # raises no exception

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
