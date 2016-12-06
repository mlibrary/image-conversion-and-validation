# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from tempfile import mkstemp
import os
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

class TestTabularData (unittest.TestCase):

    def setUp (self):
        # The TabularData class needs a path in the filesystem, so I
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
        return TabularData(self.path)

    def test_is_sequence (self):
        self.assertTrue(issubclass(TabularData, Sequence))

    def test_bad_bytes (self):
        for i in b"\x81\x8d\x8f\x90\x9d":
            self.write_file(i.to_bytes(1, "big"))
            with self.assertRaises(CantDecodeEncoding):
                data = TabularData(self.path)

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
                    data = TabularData(self.path)

    def test_error_on_stupid_newlines (self):
        self.write_file("first line\nsecond line\r\nthird line\rfourth")

        with self.assertRaises(InconsistentNewlines):
            data = TabularData(self.path)

    def test_error_on_LF_and_CRLF (self):
        self.write_file("first line\nsecond line\r\nthird line")

        with self.assertRaises(InconsistentNewlines):
            data = TabularData(self.path)

    def test_error_on_inconsistent_columns (self):
        self.write_file("shipment\tvolume\n1234567\t8974326\t7843927")

        with self.assertRaises(InconsistentColumnCounts):
            data = TabularData(self.path)

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

    def test_values_3x3 (self):
        data = self.set_to_3x3_grid()

        self.assertEqual(data[0][0], "first")
        self.assertEqual(data[0][1], "second")
        self.assertEqual(data[0][2], "third")
        self.assertEqual(data[1][0], "matthew")
        self.assertEqual(data[1][1], "alexander")
        self.assertEqual(data[1][2], "lachance")
        self.assertEqual(data[2][0], "un (french for one)")
        self.assertEqual(data[2][1], "deux")
        self.assertEqual(data[2][2], "trois")

        for i in range(3):
            self.assertTrue(isinstance(data[i], tuple))

            with self.assertRaises(IndexError):
                should_not_exist = data[i][3]

        with self.assertRaises(IndexError):
            row_should_not_exist = data[3]

    def test_values_2x4 (self):
        data = self.set_to_2x4_grid()

        self.assertEqual(data[0][0], "first")
        self.assertEqual(data[0][1], "second")
        self.assertEqual(data[1][0], "matthew")
        self.assertEqual(data[1][1], "lachance")
        self.assertEqual(data[2][0], "flibbity flobbity")
        self.assertEqual(data[2][1], "floop")
        self.assertEqual(data[3][0], "un")
        self.assertEqual(data[3][1], "deux")

        for i in range(4):
            self.assertTrue(isinstance(data[i], tuple))

            with self.assertRaises(IndexError):
                should_not_exist = data[i][2]

        with self.assertRaises(IndexError):
            row_should_not_exist = data[4]

    def test_values_0x0 (self):
        data = self.data_from_str("")

        with self.assertRaises(IndexError):
            row_should_not_exist = data[0]

    def test_slice_accession (self):
        data = self.set_to_3x3_grid()
        self.assertTrue(isinstance(data[:], list))

        data.header = True
        self.assertTrue(isinstance(data[:], list))

    def test_repr (self):
        data = self.set_to_3x3_grid()
        self.assertEqual(repr(data),
                "<TabularData header=False"
                + " ('first', 'second', 'third'),"
                + " ('matthew', 'alexander', 'lachance'),"
                + " ('un (french for one)', 'deux', 'trois')>")

class TestArgumentCollector (unittest.TestCase):

    def test_is_mapping (self):
        self.assertTrue(issubclass(ArgumentCollector, Mapping))

    def test_wrong_args (self):
        accepts_five = ArgumentCollector("a", "b", "c", "d", "e")

        with self.assertRaises(TypeError):
            accepts_five.update(1, 2, 3, 4)

        with self.assertRaises(TypeError):
            accepts_five.update(1, 2, 3, 4, 5, 6)

        with self.assertRaises(TypeError):
            accepts_five.update(1, 2, 3, 4, c = 5)

    def test_basic_args (self):
        accepts_five = ArgumentCollector("a", "b", "c", "d", "e")

        accepts_five.update(1, 2, 3, 4, 5)
        self.assertEqual(len(accepts_five), 5)
        self.assertEqual(accepts_five, {
                        "a": 1,
                        "b": 2,
                        "c": 3,
                        "d": 4,
                        "e": 5})

        accepts_five.update(5, 4, 3, 2, 1)
        self.assertEqual(len(accepts_five), 5)
        self.assertEqual(accepts_five, {
                        "e": 1,
                        "d": 2,
                        "c": 3,
                        "b": 4,
                        "a": 5})

        accepts_five.update(1, 2, 3, 4, 5, ok="what")
        self.assertEqual(len(accepts_five), 6)
        self.assertEqual(accepts_five, {
                        "ok": "what",
                        "a": 1,
                        "b": 2,
                        "c": 3,
                        "d": 4,
                        "e": 5})

        accepts_five.update(1, 2, 3, 4, 5)
        self.assertEqual(len(accepts_five), 5)
        self.assertEqual(accepts_five, {
                        "a": 1,
                        "b": 2,
                        "c": 3,
                        "d": 4,
                        "e": 5})

    def test_kwargs (self):
        with_defaults = ArgumentCollector("a", "b", c=1, d=2, e=3)

        with_defaults.update(1, 2)
        self.assertEqual(len(with_defaults), 5)
        self.assertEqual(with_defaults, {
                        "a": 1,
                        "b": 2,
                        "c": 1,
                        "d": 2,
                        "e": 3})

        with_defaults.update(123, 234, d=345)
        self.assertEqual(len(with_defaults), 5)
        self.assertEqual(with_defaults, {
                        "a": 123,
                        "b": 234,
                        "c": 1,
                        "d": 345,
                        "e": 3})

        with_defaults.update("hi", "hello")
        self.assertEqual(len(with_defaults), 5)
        self.assertEqual(with_defaults, {
                        "a": "hi",
                        "b": "hello",
                        "c": 1,
                        "d": 2,
                        "e": 3})

        with_defaults.update(1, 2, f="matt")
        self.assertEqual(len(with_defaults), 6)
        self.assertEqual(with_defaults, {
                        "a": 1,
                        "b": 2,
                        "c": 1,
                        "d": 2,
                        "e": 3,
                        "f": "matt"})

        with_defaults.update(1, 2)
        self.assertEqual(len(with_defaults), 5)
        self.assertEqual(with_defaults, {
                        "a": 1,
                        "b": 2,
                        "c": 1,
                        "d": 2,
                        "e": 3})

    def test_repr (self):
        eg_ac = ArgumentCollector("a", "b", hi="hello", d="hey")
        eg_ac.update(1, 2, c=3, d=4)

        start = "<ArgumentCollector {"
        end = "}>"
        length = len(start) + len(end)

        repr_str = repr(eg_ac)

        self.assertTrue(repr_str.startswith(start))
        self.assertTrue(repr_str.endswith(end))

        i = 0
        for key, value in eg_ac.items():
            i += 1
            findstr = "{}: {}".format(repr(key), repr(value))
            self.assertNotEqual(-1, repr_str.find(findstr))
            length += len(findstr) + 2

        self.assertEqual(i, 5)

        self.assertEqual(len(repr_str), length - 2)

    def test_copy (self):
        a = ArgumentCollector("a", "b", hi="hello", d="hey")
        a.update(1, 2, c=3, d=4)

        b = a.copy()
        self.assertEqual(a, b)
        self.assertEqual(len(a), len(b))

        for key in a:
            self.assertIn(key, b)
            self.assertEqual(a[key], b[key])

        for key in b:
            self.assertIn(key, a)
            self.assertEqual(a[key], b[key])

        b.update(3, 4)

        # a should be unchanged.
        self.assertEqual(a["a"], 1)
        self.assertEqual(a["b"], 2)
        self.assertEqual(a["c"], 3)
        self.assertEqual(a["d"], 4)
        self.assertEqual(a["hi"], "hello")

        # b should reflect the change (even with the default value for
        # "d").
        self.assertEqual(b["a"], 3)
        self.assertEqual(b["b"], 4)
        self.assertEqual(b["hi"], "hello")
        self.assertEqual(b["d"], "hey")

    def test_base (self):
        a = ArgumentCollector("a", z="zee")
        a.update(5)

        b = a.base("b")
        b.update(4)

        self.assertEqual(a, {
            "a":    5,
            "z":    "zee"})

        self.assertEqual(b, {
            "a":    5,
            "b":    4,
            "z":    "zee"})

        a.update(8)

        self.assertEqual(a["a"], 8)
        self.assertEqual(b["a"], 5)

        b.update(b=4, z="matt is cool")

        self.assertEqual(a["z"], "zee")
        self.assertEqual(b["z"], "matt is cool")

    def test_truthiness (self):
        a = ArgumentCollector("hey", matt="is cool")
        self.assertFalse(a)

        a.update("holler")
        self.assertTrue(a)

        a = ArgumentCollector(matt="is still cool")
        self.assertTrue(a)

        a = ArgumentCollector()
        self.assertFalse(a)

        a.update(matt="just got cooler")
        self.assertTrue(a)

        a.update()
        self.assertFalse(a)
