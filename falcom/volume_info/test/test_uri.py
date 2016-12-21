# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from http.client import HTTPResponse
import unittest

from ...general.slow_test import slow_test

from ..argument_collector import ArgumentCollector
from ..uri import URI

class TestURI (unittest.TestCase):

    def set_uri (self, *args, **kwargs):
        self.uri = URI(ArgumentCollector, *args, **kwargs)

    def get_variadic (func):
        def result (self, *args, **kwargs):
            return func(self.uri)(*args, **kwargs)

        return result

    @get_variadic
    def get_GET_uri (uri):
        return uri.get_uri

    @get_variadic
    def get_POST_uri (uri):
        return uri.post_uri

    @get_variadic
    def get_GET_data (uri):
        return uri.get

    @get_variadic
    def get_POST_data (uri):
        return uri.post

    def test_get (self):
        base = "https://lib.umich.edu/"
        self.set_uri(base, "barcode", key="secret")

        result = self.get_GET_uri("hello")

        barcode_hello = "barcode=hello".encode("ascii")
        key_secret = "key=secret".encode("ascii")

        self.assertTrue(isinstance(result, bytes))
        self.assertTrue(result.startswith(base.encode("ascii") + b"?"))
        self.assertNotEqual(-1, result.find(barcode_hello))
        self.assertNotEqual(-1, result.find(key_secret))
        self.assertEqual(len(result),
                len(base) + len(barcode_hello) + len(key_secret) + 2)

    def test_post (self):
        base = "https://lib.umich.edu/"
        self.set_uri(base)

        result = self.get_POST_uri(matt="is cool")
        self.assertTrue(isinstance(result, tuple))
        self.assertEqual(len(result), 2)

        result_uri, result_data = result
        self.assertEqual(result_uri, base.encode("ascii"))
        self.assertTrue(isinstance(result_data, bytes))
        self.assertEqual(result_data, b"matt=is+cool")

    def test_unicode (self):
        base = "https://lib.umich.edu/"
        self.set_uri(base)

        result = self.get_GET_uri(matt="💪")
        expected = base + "?matt=%F0%9F%92%AA"

        self.assertEqual(result, expected.encode("ascii"))

    @slow_test
    def test_get_response (self):
        self.set_uri("http://lib.umich.edu/", "matt")

        with self.get_GET_data("is cool") as response:
            self.assertTrue(isinstance(response, HTTPResponse))
            self.assertTrue(response.geturl().endswith(
                    "lib.umich.edu/?matt=is+cool"))
            self.assertTrue(isinstance(response.read(), bytes))

    @slow_test
    def test_post_response (self):
        self.set_uri("http://lib.umich.edu/", "matt")

        with self.get_POST_data("is cool") as response:
            self.assertTrue(isinstance(response, HTTPResponse))
            self.assertTrue(response.geturl().endswith(
                    "lib.umich.edu/"))
            self.assertTrue(isinstance(response.read(), bytes))

    def test_data_in_uri (self):
        self.set_uri("http://lib.umich.edu/etc/{barcode}/",
                "barcode")

        self.assertEqual(self.get_GET_uri("39015012345678"),
                b"http://lib.umich.edu/etc/39015012345678/")
        self.assertEqual(self.get_GET_uri("39015012345679", a="b"),
                b"http://lib.umich.edu/etc/39015012345679/?a=b")
