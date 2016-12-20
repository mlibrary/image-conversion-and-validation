# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from http.client import HTTPResponse
import unittest

from ..uri import URI
from ...general.slow_test import slow_test

class TestURI (unittest.TestCase):

    def test_get (self):
        base = "https://lib.umich.edu/"
        uri = URI(base, "barcode", key="secret")

        result = uri.get_uri("hello")

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
        uri = URI(base)

        result = uri.post_uri(matt="is cool")
        self.assertTrue(isinstance(result, tuple))
        self.assertEqual(len(result), 2)

        result_uri, result_data = result
        self.assertEqual(result_uri, base.encode("ascii"))
        self.assertTrue(isinstance(result_data, bytes))
        self.assertEqual(result_data, b"matt=is+cool")

    def test_unicode (self):
        base = "https://lib.umich.edu/"
        uri = URI(base)

        result = uri.get_uri(matt="💪")
        expected = base + "?matt=%F0%9F%92%AA"

        self.assertEqual(result, expected.encode("ascii"))

    @slow_test
    def test_get_response (self):
        uri = URI("http://lib.umich.edu/", "matt")

        with uri.get("is cool") as response:
            self.assertTrue(isinstance(response, HTTPResponse))
            self.assertTrue(response.geturl().endswith(
                    "lib.umich.edu/?matt=is+cool"))
            self.assertTrue(isinstance(response.read(), bytes))

    @slow_test
    def test_post_response (self):
        uri = URI("http://lib.umich.edu/", "matt")

        with uri.post("is cool") as response:
            self.assertTrue(isinstance(response, HTTPResponse))
            self.assertTrue(response.geturl().endswith(
                    "lib.umich.edu/"))
            self.assertTrue(isinstance(response.read(), bytes))

    def test_data_in_uri (self):
        uri = URI("http://lib.umich.edu/etc/{barcode}/",
                "barcode")

        self.assertEqual(uri.get_uri("39015012345678"),
                b"http://lib.umich.edu/etc/39015012345678/")
        self.assertEqual(uri.get_uri("39015012345679", a="b"),
                b"http://lib.umich.edu/etc/39015012345679/?a=b")
