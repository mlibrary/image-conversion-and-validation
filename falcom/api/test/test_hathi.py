# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import os
import unittest

from ...test.hamcrest import ComposedMatcher, evaluates_to
from ..hathi import get_oclc_counts_from_json, get_hathi_data_from_json

class yields_oclc_counts (ComposedMatcher):

    def __init__ (self, mdp, other):
        self.expected = (mdp, other)

    def assertion (self, item):
        actual = get_oclc_counts_from_json(*item)
        yield actual, is_(equal_to(self.expected))

class empty_hathi_data (ComposedMatcher):

    def assertion (self, item):
        yield item, evaluates_to(False)
        yield item.titles, empty()
        yield item.htids, empty()

class yields_empty_hathi_data (ComposedMatcher):

    def assertion (self, item):
        yield get_hathi_data_from_json(item), is_(empty_hathi_data())

class OclcCountHelpers (unittest.TestCase):
    htid = None

    def assert_oclc_counts (self, a, b):
        assert_that(get_oclc_counts_from_json(self.json,
                                              self.htid),
                    is_(equal_to((a, b))))

    def get_json_from_file (self, hathitrust_filename):
        files_dir = os.path.join(os.path.dirname(__file__), "files")
        full_filename = "hathitrust-{}.json".format(hathitrust_filename)
        file_path = os.path.join(files_dir, full_filename)

        with open(file_path, "r") as f:
            self.json = f.read()

class GivenNothing (OclcCountHelpers):

    def test_null_yields_0_0 (self):
        self.json = None
        self.assert_oclc_counts(0, 0)

    def test_empty_str_yields_0_0 (self):
        self.json = ""
        self.assert_oclc_counts(0, 0)

    def test_invalid_json_yields_0_0 (self):
        self.json = "{{{{"
        self.assert_oclc_counts(0, 0)

class GivenAstroJson:

    def setUp (self):
        self.get_json_from_file("706055947")
        self.htid = "mdp.39015081447313"

class TestAstroJson (GivenAstroJson, OclcCountHelpers):

    def test_count_is_1_0 (self):
        self.assert_oclc_counts(1, 0)

class GivenBusinessJson (OclcCountHelpers):

    def setUp (self):
        self.get_json_from_file("756167029")
        self.htid = "mdp.39015090867675"

    def test_count_is_1_0 (self):
        self.assert_oclc_counts(0, 0)

class GivenMidailyJson (OclcCountHelpers):

    def setUp (self):
        self.get_json_from_file("009651208")
        self.htid = "mdp.39015071755826"

    def test_count_is_1_0 (self):
        self.assert_oclc_counts(0, 1)

class GivenMultiJson (OclcCountHelpers):

    def setUp (self):
        self.get_json_from_file("multi-eg")
        self.htid = "mdp.39015071754159"

    def test_count_is_1_0 (self):
        self.assert_oclc_counts(1, 3)

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

    def test_empty_data_has_title_distance_of_1 (self):
        data = get_hathi_data_from_json()
        assert_that(data.min_title_distance("anything"),
                    is_(close_to(1, 0.001)))

class TestAstroJsonRecordData (GivenAstroJson, OclcCountHelpers):

    def setUp (self):
        super().setUp()
        self.data = get_hathi_data_from_json(self.json)

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

    def test_exact_match_yields_0 (self):
        title = "Astronomical tables : manuscript, [17th century?]."
        assert_that(self.data.min_title_distance(title),
                    is_(less_than(.001)))

    def test_near_match_yields_small_number (self):
        title = "Abtronomical tables : manuscript, [17th century?]."
        assert_that(self.data.min_title_distance(title),
                    all_of(greater_than(0), less_than(0.5)))
