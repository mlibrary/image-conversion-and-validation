# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from tempfile import mkstemp
import os
import unittest

from .get_oclc_data import *

class TestInputData (unittest.TestCase):

    def setUp (self):
        # The InputData class needs a path in the filesystem, so I
        # probably need to create a file.
        fd, self.path = mkstemp(dir="/tmp", suffix=".txt")

        # I don't want to deal with this low-level nonsense.
        os.close(fd)

    def tearDown (self):
        # Delete the temporary file I created.
        os.unlink(self.path)

    def write_file (self, content):
        if isinstance(content, str):
            mode = "w"

        else:
            assert isinstance(content, bytes)
            mode = "wb"

        with open(self.path, mode) as obj:
            obj.write(content)

    def data_from_str (self, content):
        self.write_file(content)
        return InputData(self.path)

    def test_is_sequence (self):
        self.assertTrue(issubclass(InputData, Sequence))

    def test_bad_bytes (self):
        for i in b"\x81\x8d\x8f\x90\x9d":
            self.write_file(i.to_bytes(1, "big"))
            with self.assertRaises(CantDecodeEncoding):
                data = InputData(self.path)

    def test_bad_control_characters (self):
        ranges = (
            (0x00, 0x09), # skip HT, LF
            (0x0b, 0x0d), # skip CR
            (0x0e, 0x20), # skip [ -~] aka visible characters
            (0x7f, 0xa0), # not worrying about non-ASCII controls
        )

        for low, high in ranges:
            for i in range(low, high):
                self.write_file("something{}something\n".format(chr(i)))
                regex = "0x{:02x}".format(i)
                with self.assertRaisesRegex(InvalidControls, regex):
                    data = InputData(self.path)

    def test_error_on_stupid_newlines (self):
        self.write_file("first line\nsecond line\r\nthird line\rfourth")

        with self.assertRaises(InconsistentNewlines):
            data = InputData(self.path)

    def test_error_on_LF_and_CRLF (self):
        self.write_file("first line\nsecond line\r\nthird line")

        with self.assertRaises(InconsistentNewlines):
            data = InputData(self.path)

    def test_error_on_inconsistent_columns (self):
        self.write_file("shipment\tvolume\n1234567\t8974326\t7843927")

        with self.assertRaises(InconsistentColumnCounts):
            data = InputData(self.path)

    def set_to_3x3_grid (self):
        return self.data_from_str("\n".join((
                "first\tsecond\tthird",
                "matthew\talexander\tlachance",
                "un (french for one)\tdeux\ttrois")))

    def set_to_2x4_grid (self):
        return self.data_from_str("\n".join((
                "first\tsecond",
                "matthew\tlachance",
                "flibbity flobbity\tfloop",
                "un\tdeux")))

    def test_len_3x3 (self):
        data = self.set_to_3x3_grid()
        self.assertEqual(len(data), 3)
        self.assertEqual(data.rows, 3)
        self.assertEqual(data.cols, 3)

    def test_len_2x4 (self):
        data = self.set_to_2x4_grid()
        self.assertEqual(len(data), 4)
        self.assertEqual(data.rows, 4)
        self.assertEqual(data.cols, 2)

    def test_len_0x0 (self):
        data = self.data_from_str("")
        self.assertEqual(len(data), 0)
        self.assertEqual(data.rows, 0)
        self.assertEqual(data.cols, 0)

    def test_set_header (self):
        data = self.set_to_2x4_grid()

        self.assertFalse(data.header)
        data.header = True
        self.assertTrue(data.header)

        self.assertEqual(len(data), 3)
        self.assertEqual(data.rows, 3)
        self.assertEqual(data.cols, 2)

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
