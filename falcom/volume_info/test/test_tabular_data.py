# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from collections.abc import Sequence
from tempfile import mkstemp
import os
import unittest

from ..tabular_data import TabularData
from ...exceptions import \
        CantDecodeEncoding, \
        InconsistentColumnCounts, \
        InconsistentNewlines, \
        InvalidControls

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