# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import unittest

from .get_oclc_data import *

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

    def test_inconsistent_newlines (self):
        with self.assertRaisesRegex(InputFileError,
                "Some combination of LF, CR, and CRLFs in filename"):
            raise InconsistentNewlines("filename")
