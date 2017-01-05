# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .marc import *
from .hamcrest_marc import contains_marc_fields

class NothingTest (unittest.TestCase):

    def test_nothing (self):
        marc_data = get_marc_data_from_xml(None)
        assert_that(marc_data, contains_marc_fields())

if __name__ == "__main__":
    unittest.main()
