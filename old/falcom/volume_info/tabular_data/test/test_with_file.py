# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from tempfile import mkstemp
import os
import unittest

from ..base import TabularData
from ..filesystem import TabularDataFromFilePath

from .base import BaseTabularDataTest

class TestTabularDataFromFilePath (unittest.TestCase,
        BaseTabularDataTest):

    repr_class_name = "TabularDataFromFilePath"

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
        return TabularDataFromFilePath(self.path)

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

    def test_is_tabular_data (self):
        self.assertTrue(issubclass(TabularDataFromFilePath, TabularData))
