# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .marc import *
from .hamcrest_marc import ComposedAssertion, \
        has_marc_attrs, evaluates_to_true, evaluates_to_false

class IsEmptyMarcData (ComposedAssertion):

    def assertion (self, item):
        yield evaluates_to_false()
        yield has_marc_attrs(
                bib=None,
                callno=None,
                oclc=None,
                author=None,
                title=None,
                description=None,
                years=(None, None))

def is_empty_marc_data(): return IsEmptyMarcData()

class NothingTest (unittest.TestCase):

    def test_marc_data_of_None_yields_empty_MARC_data (self):
        marc_data = get_marc_data_from_xml(None)
        assert_that(marc_data, is_empty_marc_data())

    def test_marc_data_of_empty_str_yields_empty_MARC_data (self):
        marc_data = get_marc_data_from_xml("")
        assert_that(marc_data, is_empty_marc_data())

if __name__ == "__main__":
    unittest.main()
