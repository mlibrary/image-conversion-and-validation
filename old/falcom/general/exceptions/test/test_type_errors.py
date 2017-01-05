# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import unittest

from ..type_errors import MissingPositionalArgsError, \
        MultipleValuesOneArgError, \
        TooManyArgumentsError

class TestCustomTypeErrors (unittest.TestCase):

    class_to_test = TypeError

    def assert_error_equal (self, *args):
        rhs = args[-1]
        args = args[:-1]

        error = self.class_to_test(*args)
        self.assertTrue(isinstance(error, TypeError))
        self.assertEqual(str(error), rhs)

    def test_is_TypeError (self):
        self.assertTrue(issubclass(self.class_to_test, TypeError))

class TestTooManyArgumentsError (TestCustomTypeErrors):

    class_to_test = TooManyArgumentsError

    def test_expected_zero (self):
        self.assert_error_equal("hi", 0, 1,
                "hi() takes 0 positional arguments but 1 was given")

        self.assert_error_equal("two", 0, 2,
                "two() takes 0 positional arguments but 2 were given")

        self.assert_error_equal("three", 0, 3,
                "three() takes 0 positional arguments but 3 were given")

    def test_expected_one (self):
        self.assert_error_equal("four", 1, 2,
                "four() takes 1 positional argument but 2 were given")

        self.assert_error_equal("five", 1, 3,
                "five() takes 1 positional argument but 3 were given")

    def test_expected_two (self):
        self.assert_error_equal("six", 2, 3,
                "six() takes 2 positional arguments but 3 were given")

class TestMultipleValuesOneArgError (TestCustomTypeErrors):

    class_to_test = MultipleValuesOneArgError

    def test_degenerate (self):
        self.assert_error_equal("hey", "what",
                "hey() got multiple values for keyword argument 'what'")

        self.assert_error_equal("two", "ok",
                "two() got multiple values for keyword argument 'ok'")

class TestMissingPositionalArgsError (TestCustomTypeErrors):

    class_to_test = MissingPositionalArgsError

    def test_variadic_args (self):
        self.assert_error_equal("hello", "missing1",
                "hello() missing 1 required positional argument: "
                "'missing1'")

        self.assert_error_equal("hello", "missing1", "missing2",
                "hello() missing 2 required positional arguments: "
                "'missing1' and 'missing2'")

        self.assert_error_equal("hello", "one", "two", "three",
                "hello() missing 3 required positional arguments: "
                "'one', 'two', and 'three'")

        self.assert_error_equal("hello", "one", "two", "three", "four",
                "hello() missing 4 required positional arguments: "
                "'one', 'two', 'three', and 'four'")

    def test_different_function_names (self):
        self.assert_error_equal("what", "arg",
                "what() missing 1 required positional argument: 'arg'")

        self.assert_error_equal("yooo", "arg",
                "yooo() missing 1 required positional argument: 'arg'")
