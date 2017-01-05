# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .marc import *

class NothingTest (unittest.TestCase):

    def test_nothing (self):
        marc_data = get_marc_data_from_xml(None)

if __name__ == "__main__":
    unittest.main()
