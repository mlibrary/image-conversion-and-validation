# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .marc import *
from .hamcrest_marc import evaluates_to_true, evaluates_to_false

class NothingTest (unittest.TestCase):

    def test_marc_data_of_None_yields_empty_MARC_data (self):
        marc_data = get_marc_data_from_xml(None)

        assert_that(marc_data, evaluates_to_false())
        assert_that(marc_data.bib, is_(none()))

if __name__ == "__main__":
    unittest.main()
