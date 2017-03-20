# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from os.path import join, dirname
from unittest import TestCase

class ExampleFileTest (TestCase):

    def setUp (self):
        with open(self.__file_path(), "r") as f:
            self.file_data = f.read()

    def __file_path (self):
        return join(self.__files_dir(), self.__full_filename())

    def __files_dir (self):
        return join(dirname(self.this__file__), "files")

    def __full_filename (self):
        format_str = getattr(self, "format_str", "{}")
        return format_str.format(self.filename)
