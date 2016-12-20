# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from http.client import HTTPResponse
from tempfile import mkstemp
import os
import unittest

from .get_oclc_data import *

SLOW_TESTS = os.environ.get("SLOW_TESTS", False)
slow_test = unittest.skipUnless(SLOW_TESTS, "slow test")

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

    class_to_test = None

    def assert_error_equal (self, *args):
        rhs = args[-1]
        args = args[:-1]

        error = self.class_to_test(*args)
        self.assertTrue(isinstance(error, TypeError))
        self.assertEqual(str(error), rhs)

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

    @unittest.skipUnless(False, "later")
    def test_degenerate (self):
        self.assert_error_equal("hello", "missing1",
                "hello() missing 1 required positional argument: "
                "'missing1'")

        self.assert_error_equal("hello", "missing1", "missing2",
                "hello() missing 2 required positional arguments: "
                "'missing1' and 'missing2'")

class TestCountedWord (unittest.TestCase):

    def init_counted_word (self, *args):
        self.word = CountedWord(*args)

    def assert_getstr (self, number, rhs):
        self.assertEqual(self.word.getstr(number), rhs)

    def test_degenerate (self):
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

    def init_tabular_data (self):
        """Return TabularData initted with our temporary file."""
        return TabularData(self.path)

    def set_header (self, data, value = True):
        """Set the header to the given value (or to True)."""
        data.header = value

    def assert_header (self, data, value):
        """Get the data's header and assert its equality."""
        self.assertEqual(data.header, value)

    def assert_rows (self, data, value):
        """Get the data's row count and assert its equality."""
        self.assertEqual(data.rows, value)

    def assert_cols (self, data, value):
        """Get the data's column count and assert its equality."""
        self.assertEqual(data.cols, value)

    def write_file (self, content):
        """Shortcut to write bytes or a str to a file."""

        if isinstance(content, str):
            # If the content is a str, then I can write all like normal
            # at a high level.
            mode = "w"

        else:
            # Otherwise, I need to write bytes, and I should ensure that
            # I actually have bytes to write with.
            assert isinstance(content, bytes)
            mode = "wb"

        with open(self.path, mode) as obj:
            # Write the content into the temporary file we've created at
            # setup.
            obj.write(content)

    def data_from_str (self, content):
        """Shortcut for writing content to a file and opening it."""
        self.write_file(content)
        return self.init_tabular_data()

    def test_is_sequence (self):
        self.assertTrue(issubclass(TabularData, Sequence))

    def test_bad_bytes (self):
        for i in b"\x81\x8d\x8f\x90\x9d":
            self.write_file(i.to_bytes(1, "big"))
            with self.assertRaises(CantDecodeEncoding):
                data = self.init_tabular_data()

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
                    data = self.init_tabular_data()

    def test_error_on_stupid_newlines (self):
        self.write_file("first line\nsecond line\r\nthird line\rfourth")

        with self.assertRaises(InconsistentNewlines):
            data = self.init_tabular_data()

    def test_error_on_LF_and_CRLF (self):
        self.write_file("first line\nsecond line\r\nthird line")

        with self.assertRaises(InconsistentNewlines):
            data = self.init_tabular_data()

    def test_error_on_inconsistent_columns (self):
        self.write_file("shipment\tvolume\n1234567\t8974326\t7843927")

        with self.assertRaises(InconsistentColumnCounts):
            data = self.init_tabular_data()

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
        self.assert_rows(data, 3)
        self.assert_cols(data, 3)

    def test_len_2x4 (self):
        data = self.set_to_2x4_grid()
        self.assertEqual(len(data), 4)
        self.assert_rows(data, 4)
        self.assert_cols(data, 2)

    def test_len_0x0 (self):
        data = self.data_from_str("")
        self.assertEqual(len(data), 0)
        self.assert_rows(data, 0)
        self.assert_cols(data, 0)

    def test_set_header (self):
        data = self.set_to_2x4_grid()

        self.assert_header(data, False)
        self.set_header(data)
        self.assert_header(data, True)

        self.assertEqual(len(data), 3)
        self.assert_rows(data, 3)
        self.assert_cols(data, 2)

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

        self.set_header(data)
        self.assertTrue(isinstance(data[:], list))

    def test_repr (self):
        data = self.set_to_3x3_grid()
        self.assertEqual(repr(data),
                "<TabularData header=False"
                + " ('first', 'second', 'third'),"
                + " ('matthew', 'alexander', 'lachance'),"
                + " ('un (french for one)', 'deux', 'trois')>")

class TestArgumentCollector (unittest.TestCase):

    def test_zero_args (self):
        ac = ArgumentCollector()
        self.assertFalse(bool(ac))
        self.assertEqual(len(ac), 0)

        ac.update(hey = "hello")
        self.assertTrue(bool(ac))
        self.assertEqual(len(ac), 1)
        self.assertTrue("hey" in ac)
        self.assertFalse("what" in ac)

        ac.update(what = "whaddup")
        self.assertTrue(bool(ac))
        self.assertEqual(len(ac), 1)
        self.assertFalse("hey" in ac)
        self.assertTrue("what" in ac)

    def test_one_arg (self):
        ac = ArgumentCollector("matt")
        self.assertFalse(bool(ac))
        self.assertEqual(len(ac), 0)

    def test_one_arg_one_kwarg (self):
        ac = ArgumentCollector("hi", matt="is cool")
        self.assertFalse(bool(ac))
        self.assertEqual(len(ac), 1)

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
        a = ArgumentCollector("matt", matt="is cool")
        self.assertTrue(a)

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

    def test_skip_iter (self):
        a = ArgumentCollector()
        a.skip_iter("hey", "matt")
        a.update(hey="hello", matt="is cool", ok="yes")

        self.assertEqual(len(a), 1)
        self.assertEqual(list(a), ["ok"])
        self.assertEqual(a["hey"], "hello")
        self.assertEqual(a["matt"], "is cool")
        self.assertEqual(a["ok"], "yes")

    def test_skip_iter_zero_length (self):
        a = ArgumentCollector()
        a.skip_iter("nothing")
        self.assertEqual(len(a), 0)

class TestDecoyMapping (unittest.TestCase):

    def assert_keys (self, format_string, values):
        """Run extract_format_keys and compare its result."""
        self.assertEqual(extract_format_keys(format_string), values)

    def test_format_empty (self):
        self.assert_keys("no field names", set())

    def test_format_one (self):
        self.assert_keys("what if it's {hi}", {"hi"})

    def test_format_multiple (self):
        self.assert_keys("{hey} and {whatsup}", {"hey", "whatsup"})

    def test_format_decimal (self):
        self.assert_keys("{holler:d}", {"holler"})

    def test_format_float (self):
        self.assert_keys("{holler:f}", {"holler"})

class TestURI (unittest.TestCase):

    def test_get (self):
        base = "https://lib.umich.edu/"
        uri = URI(base, "barcode", key="secret")

        result = uri.get_uri("hello")

        barcode_hello = "barcode=hello".encode("ascii")
        key_secret = "key=secret".encode("ascii")

        self.assertTrue(isinstance(result, bytes))
        self.assertTrue(result.startswith(base.encode("ascii") + b"?"))
        self.assertNotEqual(-1, result.find(barcode_hello))
        self.assertNotEqual(-1, result.find(key_secret))
        self.assertEqual(len(result),
                len(base) + len(barcode_hello) + len(key_secret) + 2)

    def test_post (self):
        base = "https://lib.umich.edu/"
        uri = URI(base)

        result = uri.post_uri(matt="is cool")
        self.assertTrue(isinstance(result, tuple))
        self.assertEqual(len(result), 2)

        result_uri, result_data = result
        self.assertEqual(result_uri, base.encode("ascii"))
        self.assertTrue(isinstance(result_data, bytes))
        self.assertEqual(result_data, b"matt=is+cool")

    def test_unicode (self):
        base = "https://lib.umich.edu/"
        uri = URI(base)

        result = uri.get_uri(matt="💪")
        expected = base + "?matt=%F0%9F%92%AA"

        self.assertEqual(result, expected.encode("ascii"))

    @slow_test
    def test_get_response (self):
        uri = URI("http://lib.umich.edu/", "matt")

        with uri.get("is cool") as response:
            self.assertTrue(isinstance(response, HTTPResponse))
            self.assertTrue(response.geturl().endswith(
                    "lib.umich.edu/?matt=is+cool"))
            self.assertTrue(isinstance(response.read(), bytes))

    @slow_test
    def test_post_response (self):
        uri = URI("http://lib.umich.edu/", "matt")

        with uri.post("is cool") as response:
            self.assertTrue(isinstance(response, HTTPResponse))
            self.assertTrue(response.geturl().endswith(
                    "lib.umich.edu/"))
            self.assertTrue(isinstance(response.read(), bytes))

    def test_data_in_uri (self):
        uri = URI("http://lib.umich.edu/etc/{barcode}/",
                "barcode")

        self.assertEqual(uri.get_uri("39015012345678"),
                b"http://lib.umich.edu/etc/39015012345678/")
        self.assertEqual(uri.get_uri("39015012345679", a="b"),
                b"http://lib.umich.edu/etc/39015012345679/?a=b")
