# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import unittest

from ....exceptions import BaseError

from ..base import TabularData

class TestExceptions (unittest.TestCase):

    def test_input_file_error (self):
        self.assertTrue(issubclass(
            TabularData.InputFileError, BaseError))

    def test_cant_decode_encoding (self):
        with self.assertRaisesRegex(TabularData.InputFileError,
                "Can't figure out file encoding for /path/to/file"):
            raise TabularData.CantDecodeEncoding("/path/to/file")

    def test_invalid_controls (self):
        with self.assertRaisesRegex(TabularData.CantDecodeEncoding,
                r"Unexpected control character \(0x0d\) in filename"):
            raise TabularData.InvalidControls(13, "filename")

    def test_inconsistent_newlines (self):
        with self.assertRaisesRegex(TabularData.InputFileError,
                "Some combination of LF, CR, and CRLFs in filename"):
            raise TabularData.InconsistentNewlines("filename")

    def test_inconsistent_column_counts (self):
        with self.assertRaisesRegex(TabularData.InputFileError,
                "Expected each row to have the same column count " \
                "in filename"):
            raise TabularData.InconsistentColumnCounts("filename")
