# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import unittest

from .exceptions import *

class TestBaseError (unittest.TestCase):

    def test_is_exception (self):
        self.assertTrue(issubclass(BaseError, Exception))

    def test_zero_arg_error (self):
        class ZeroArg (BaseError):
            """test description"""
            pass

        error = ZeroArg()

        self.assertIs(error.value, None)
        self.assertEqual(str(error), "test description")

    def test_one_arg_error (self):
        class OneArg (BaseError):
            """got {} is all"""
            pass

        matt = OneArg("matt")
        self.assertEqual(matt.value, "matt")
        self.assertEqual(str(matt), "got matt is all")

        five = OneArg(5)
        self.assertEqual(five.value, 5)
        self.assertEqual(str(five), "got 5 is all")

    def test_many_arg_error (self):
        class ManyArg (BaseError):
            """got {} and {}"""
            pass

        matt = ManyArg("matt", "he's cool")
        self.assertEqual(matt.value, ("matt", "he's cool"))
        self.assertEqual(str(matt), "got matt and he's cool")

        five = ManyArg(5, 5)
        self.assertEqual(five.value, (5, 5))
        self.assertEqual(str(five), "got 5 and 5")

    def test_newline_strip (self):
        class ZeroArg (BaseError):
            """some simple description

            and some other info
            """
            pass

        class OneArg (BaseError):
            """something something {}

            and some other info
            """
            pass

        zero = ZeroArg()
        self.assertIs(zero.value, None)
        self.assertEqual(str(zero), "some simple description")

        matt = OneArg("matt")
        self.assertEqual(matt.value, "matt")
        self.assertEqual(str(matt), "something something matt")

        five = OneArg(5)
        self.assertEqual(five.value, 5)
        self.assertEqual(str(five), "something something 5")

    def test_input_file_error (self):
        self.assertTrue(issubclass(InputFileError, BaseError))

    def test_cant_decode_encoding (self):
        with self.assertRaisesRegex(InputFileError,
                "Can't figure out file encoding for /path/to/file"):
            raise CantDecodeEncoding("/path/to/file")

    def test_invalid_controls (self):
        with self.assertRaisesRegex(CantDecodeEncoding,
                r"Unexpected control character \(0x0d\) in filename"):
            raise InvalidControls(13, "filename")

    def test_inconsistent_newlines (self):
        with self.assertRaisesRegex(InputFileError,
                "Some combination of LF, CR, and CRLFs in filename"):
            raise InconsistentNewlines("filename")

    def test_inconsistent_column_counts (self):
        with self.assertRaisesRegex(InputFileError,
                "Expected each row to have the same column count " \
                "in filename"):
            raise InconsistentColumnCounts("filename")

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

class TestCountedWord (unittest.TestCase):

    def init_counted_word (self, *args):
        self.word = CountedWord(*args)

    def assert_getstr (self, number, rhs):
        self.assertEqual(self.word(number), rhs)

    def test_different_simple_nouns (self):
        self.init_counted_word("thing")
        self.assert_getstr(0, "0 things")
        self.assert_getstr(1, "1 thing")
        self.assert_getstr(2, "2 things")

        self.init_counted_word("widget")
        self.assert_getstr(0, "0 widgets")
        self.assert_getstr(1, "1 widget")
        self.assert_getstr(2, "2 widgets")

    def test_custom_plural (self):
        self.init_counted_word("octopus", "octopodes")
        self.assert_getstr(0, "0 octopodes")
        self.assert_getstr(1, "1 octopus")
        self.assert_getstr(2, "2 octopodes")

    def test_repr (self):
        self.init_counted_word("beat")
        self.assertEqual(repr(self.word), "<CountedWord beat/beats>")

        self.init_counted_word("holler")
        self.assertEqual(repr(self.word),
                "<CountedWord holler/hollers>")

        self.init_counted_word("forum", "fora")
        self.assertEqual(repr(self.word), "<CountedWord forum/fora>")

    def test_repr_on_child_class (self):
        class SomeDerivativeOfCountedWord (CountedWord):
            pass

        w = SomeDerivativeOfCountedWord("rock")
        self.assertEqual(repr(w),
                "<SomeDerivativeOfCountedWord rock/rocks>")
