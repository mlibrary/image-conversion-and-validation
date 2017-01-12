# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import os
import unittest

from .hamcrest import ComposedAssertion
from ..hathi import get_oclc_counts_from_json

FILE_BASE = os.path.join(os.path.dirname(__file__), "files")

def readfile (filename):
    with open(os.path.join(FILE_BASE, filename), "r") as f:
        result = f.read()

    return result

EG_HATHI_ASTRO = (readfile("hathitrust-706055947.json"),
                  "39015081447313")
EG_HATHI_BUSINESS = (readfile("hathitrust-756167029.json"),
                     "39015090867675")
EG_HATHI_MIDAILY = (readfile("hathitrust-009651208.json"),
                    "39015071755826")
EG_MULTI = (readfile("hathitrust-multi-eg.json"),
            "39015071754159")

class yields_oclc_counts (ComposedAssertion):

    def __init__ (self, mdp, other):
        self.expected = (mdp, other)

    def assertion (self, item):
        actual = get_oclc_counts_from_json(*item)
        yield actual, is_(equal_to(self.expected))

class HathiJsonTest (unittest.TestCase):

    def test_null_yields_0_0 (self):
        assert_that((None,), yields_oclc_counts(0, 0))

    def test_empty_str_yields_0_0 (self):
        assert_that(("",), yields_oclc_counts(0, 0))

    def test_invalid_json_yields_0_0 (self):
        assert_that(("{{{{",), yields_oclc_counts(0, 0))

    def test_astro_json_yields_1_0 (self):
        assert_that(EG_HATHI_ASTRO, yields_oclc_counts(1, 0))

    def test_business_json_yields_0_0 (self):
        assert_that(EG_HATHI_BUSINESS, yields_oclc_counts(0, 0))

    def test_midaily_json_yields_0_1 (self):
        assert_that(EG_HATHI_MIDAILY, yields_oclc_counts(0, 1))

    def test_multi_json_yields_1_3 (self):
        assert_that(EG_MULTI, yields_oclc_counts(1, 3))
