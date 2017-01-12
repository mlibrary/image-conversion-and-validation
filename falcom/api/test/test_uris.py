# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import unittest

from .hamcrest import ComposedAssertion, \
        evaluates_to_true, evaluates_to_false
from ..uri import URI, APIQuerier

# There are three URIs that I need to use:
#
# http://catalog.hathitrust.org/api/volumes/brief/oclc/[OCLC].json
# http://mirlyn-aleph.lib.umich.edu/cgi-bin/bc2meta?id=[BARCODE]&type=bc&schema=marcxml
# http://www.worldcat.org/webservices/catalog/content/libraries/[OCLC]?wskey=[WC_KEY]&format=json&maximumLibraries=50

class AbstractSpy:

    def __init__ (self):
        self.calls = [ ]

    def append (self, func, args = None, kwargs = None):
        if args is None:
            args = ()

        if kwargs is None:
            kwargs = {}

        self.calls.append((func, args, kwargs))

    def report (self):
        return self.calls

    def most_recent (self):
        if len(self.calls) == 0:
            return None

        else:
            return self.calls[-1]

    def __len__ (self):
        return len(self.calls)

    def __enter__ (self):
        self.append("__enter__")
        return self

    def __exit__ (self, exc_type, exc_value, traceback):
        self.append("__exit__", (exc_type, exc_value, traceback))
        return False

class HTTPResponseSpy (AbstractSpy):

    def read (self, *args, **kwargs):
        self.append("read", args, kwargs)

class UrlopenerSpy (AbstractSpy):

    def __init__ (self):
        super().__init__()
        self.response_spy = HTTPResponseSpy()

    def __call__ (self, *args, **kwargs):
        self.append(None, args, kwargs)
        return self.response_spy

class UrlopenerStub:

    class HTTPResponseStub:

        def __init__ (self, output_data):
            self.output_data = output_data

        def read (self, *args, **kwargs):
            return self.output_data

        def __enter__ (self):
            return self

        def __exit__ (self, exc_type, exc_value, traceback):
            pass

    def __init__ (self, output_data):
        self.output_data = output_data

    def __call__ (self, *args, **kwargs):
        return self.HTTPResponseStub(self.output_data)

class URITest (unittest.TestCase):

    def test_null_uri_yields_empty_string (self):
        uri = URI(None)
        assert_that(uri(), is_(equal_to("")))

    def test_no_arg_uri_yields_empty_string (self):
        uri = URI()
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

    def test_when_called_with_single_kwarg_yields_get_str (self):
        assert_that(self.uri(matt="is cool"),
                    is_(equal_to("hello?matt=is+cool")))

    def test_equals_same_simple_uri (self):
        assert_that(self.uri, is_(equal_to(URI("hello"))))

    def test_does_not_equal_some_other_uri (self):
        assert_that(self.uri, is_not(equal_to(URI("hi"))))

class GivenComposedURI (unittest.TestCase):

    def setUp (self):
        self.uri = URI("http://coolsite.gov/api/{hello}/{yes}.json")

    def test_when_called_without_args_raises_error (self):
        assert_that(calling(self.uri).with_args(),
                    raises(URI.MissingRequiredArg))

    def test_when_called_with_args_uses_args (self):
        assert_that(self.uri(hello="hi", yes="yee"), is_(equal_to(
                "http://coolsite.gov/api/hi/yee.json")))

    def test_when_called_with_extra_args_uses_get_for_them (self):
        assert_that(self.uri(hello="yo", yes="1", no="2"), is_(equal_to(
                "http://coolsite.gov/api/yo/1.json?no=2")))

    def test_spaces_are_not_pluses_for_composed_args (self):
        assert_that(self.uri(hello="a b", yes="c d e"), is_(equal_to(
                "http://coolsite.gov/api/a b/c d e.json")))

class APIQuerierTestHelpers (unittest.TestCase):

    def set_api_spy (self, uri):
        self.spy = UrlopenerSpy()
        self.api = APIQuerier(URI(uri), url_opener=self.spy)

    def set_api_stub (self, output_data):
        self.api = APIQuerier(URI(),
                              url_opener=UrlopenerStub(output_data))

class APIQuerierTest (APIQuerierTestHelpers):

    def setUp (self):
        self.set_api_spy("")

    def test_when_called_with_get_returns_get_urlopen_call (self):
        self.api.get()
        assert_that(self.spy.most_recent(),
                    is_(equal_to((None, ("",), { }))))

    def test_when_called_with_args_get_returns_urlopen_with_args (self):
        self.api.get(matt="is cool")
        assert_that(self.spy.most_recent(),
                    is_(equal_to((None, ("?matt=is+cool",), { }))))

    def test_when_calling_get_api_runs_read_in_a_context_manager (self):
        self.api.get()
        assert_that(len(self.spy.response_spy), is_(greater_than(2)))

        assert_that(self.spy.response_spy.report()[0],
                    is_(equal_to(("__enter__", (), {}))))
        assert_that(self.spy.response_spy.report()[-1],
                    is_(equal_to(("__exit__", (None, None, None), {}))))

        for func, args, kwargs in self.spy.response_spy.report()[1:-1]:
            assert_that(func, is_(equal_to("read")))

class APIQuerierDataTest (APIQuerierTestHelpers):

    def test_when_calling_get_api_returns_response_read_data (self):
        self.set_api_stub("hello")
        assert_that(self.api.get(), is_(equal_to("hello")))
