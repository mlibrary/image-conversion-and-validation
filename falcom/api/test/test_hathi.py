# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import os
import unittest

from ...test.hamcrest import ComposedMatcher, \
        evaluates_to_true, evaluates_to_false
from ..hathi import get_oclc_counts_from_json, get_hathi_data_from_json

FILE_BASE = os.path.join(os.path.dirname(__file__), "files")

def readfile (filename):
    with open(os.path.join(FILE_BASE, filename), "r") as f:
        result = f.read()

    return result

EG_HATHI_ASTRO = (readfile("hathitrust-706055947.json"),
                  "mdp.39015081447313")
EG_HATHI_BUSINESS = (readfile("hathitrust-756167029.json"),
                     "mdp.39015090867675")
EG_HATHI_MIDAILY = (readfile("hathitrust-009651208.json"),
                    "mdp.39015071755826")
EG_MULTI = (readfile("hathitrust-multi-eg.json"),
            "mdp.39015071754159")

class yields_oclc_counts (ComposedMatcher):

    def __init__ (self, mdp, other):
        self.expected = (mdp, other)

    def assertion (self, item):
        actual = get_oclc_counts_from_json(*item)
        yield actual, is_(equal_to(self.expected))

class empty_hathi_data (ComposedMatcher):

    def assertion (self, item):
        yield item, evaluates_to_false()
        yield item.titles, empty()
        yield item.htids, empty()

class yields_empty_hathi_data (ComposedMatcher):

    def assertion (self, item):
        yield get_hathi_data_from_json(item), is_(empty_hathi_data())

class HathiOclcCountsTest (unittest.TestCase):

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

class HathiRecordDataTest (unittest.TestCase):

    def test_no_args_yields_no_data (self):
        data = get_hathi_data_from_json()
        assert_that(data, is_(empty_hathi_data()))

    def test_null_yields_no_data (self):
        assert_that(None, yields_empty_hathi_data())

    def test_empty_str_yields_no_data (self):
        assert_that("", yields_empty_hathi_data())

    def test_invalid_json_yields_no_data (self):
        assert_that("{{{{]]", yields_empty_hathi_data())

    def test_json_with_no_data_yields_no_data (self):
        assert_that('{"records":{},"items":[]}',
                    yields_empty_hathi_data())

class HathiRecordDataGivenAstroJson (unittest.TestCase):

    def setUp (self):
        self.data = get_hathi_data_from_json(EG_HATHI_ASTRO[0])

    def test_yields_one_title_and_one_htid (self):
        assert_that(self.data.titles, has_length(1))
        assert_that(self.data.htids, has_length(1))

    def test_yields_no_title_matching_hey_sup (self):
        assert_that(not self.data.has_title("hey sup"))

    def test_yields_true_for_an_exact_match (self):
        assert_that(self.data.has_title(
                "Astronomical tables : manuscript, [17th century?]."))

    def test_yields_true_for_a_loose_match (self):
        assert_that(self.data.has_title(
                "astronomical tables manuscript 17th century"))

    def test_hey_sup_more_than_fifty_percent_distant (self):
        assert_that(self.data.min_title_distance("hey sup"),
                    is_(greater_than(0.5)))
