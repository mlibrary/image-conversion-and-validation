# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from os.path import join, dirname
from unittest import TestCase

class ExampleFileTest (TestCase):

    def setUp (self):
        format_str = getattr(self, "format_str", "{}")
        full_filename = format_str.format(self.filename)

        files_dir = join(dirname(self.this__file__), "files")
        file_path = join(files_dir, full_filename)

        with open(file_path, "r") as f:
            self.file_data = f.read()
