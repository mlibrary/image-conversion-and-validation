# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedAssertion
from ..uri import URI

# There are three URIs that I need to use:
#
# http://catalog.hathitrust.org/api/volumes/brief/oclc/[OCLC].json
# http://mirlyn-aleph.lib.umich.edu/cgi-bin/bc2meta?id=[BARCODE]&type=bc&schema=marcxml
# http://www.worldcat.org/webservices/catalog/content/libraries/[OCLC]?wskey=[WC_KEY]&format=json&maximumLibraries=50

class URITest (unittest.TestCase):

    def test_null_uri_yields_empty_string (self):
        uri = URI(None)
        assert_that(uri(), is_(equal_to("")))

    def test_simple_uri_yields_itself (self):
        uri = URI("hello")
        assert_that(uri(), is_(equal_to("hello")))

class GivenEmptyStrURI (unittest.TestCase):

    def setUp (self):
        self.uri = URI("")

    def test_when_called_without_args_yields_empty_str (self):
        assert_that(self.uri(), is_(equal_to("")))

    def test_when_called_with_single_kwarg_yields_get_str (self):
        assert_that(self.uri(matt="is cool"),
                    is_(equal_to("?matt=is+cool")))

    def test_when_called_with_two_kwargs_yields_both (self):
        assert_that(self.uri(hi="hello", sup="what up"),
                    any_of(is_(equal_to("?hi=hello&sup=what+up")),
                           is_(equal_to("?sup=what+up&hi=hello"))))
