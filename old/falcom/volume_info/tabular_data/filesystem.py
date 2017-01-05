# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

from .base import TabularData

class TabularDataFromFilePath (TabularData):

    def __init__ (self, path_to_file):
        """Initialize input data based on path to file."""
        with open(path_to_file, "rb") as input_file:
            bytes_obj = input_file.read()

        super(TabularDataFromFilePath, self).__init__(bytes_obj,
                path_to_file)
