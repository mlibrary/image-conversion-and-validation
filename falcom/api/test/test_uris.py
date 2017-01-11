# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedAssertion, \
        evaluates_to_true, evaluates_to_false
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

    def test_evaluates_to_false (self):
        assert_that(self.uri, evaluates_to_false())

    def test_equals_null_uri (self):
        assert_that(self.uri, is_(equal_to(URI(None))))

    def test_not_equal_to_simple_uri (self):
        assert_that(self.uri, is_not(equal_to(URI("hi"))))

    def test_not_equal_to_integer (self):
        assert_that(self.uri, is_not(equal_to(5)))

class GivenSimpleURI (unittest.TestCase):

    def setUp (self):
        self.uri = URI("hello")

    def test_simple_uri_yields_itself (self):
        assert_that(self.uri(), is_(equal_to("hello")))

    def test_evaluates_to_true (self):
        assert_that(self.uri, evaluates_to_true())
