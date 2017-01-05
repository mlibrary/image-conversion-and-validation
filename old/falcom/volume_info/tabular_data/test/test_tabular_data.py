# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from collections.abc import Sequence
import unittest

from ..base import TabularData

from .base import BaseTabularDataTest

class TestTabularData (unittest.TestCase, BaseTabularDataTest):

    repr_class_name = "TabularData"

    def setUp (self):
        self.data_bytes = b""

    def init_tabular_data (self):
        """Return TabularData initted with our temporary file."""
        return TabularData(self.data_bytes)

    def write_file (self, content):
        """Shortcut to write bytes or a str to a file."""

        if isinstance(content, str):
            # If the content is a str, then I can write all like normal
            # at a high level.
            self.data_bytes = content.encode("utf-8")

        else:
            # Otherwise, I need to write bytes, and I should ensure that
            # I actually have bytes to write with.
            assert isinstance(content, bytes)
            self.data_bytes = content

    def test_is_sequence (self):
        self.assertTrue(issubclass(TabularData, Sequence))
