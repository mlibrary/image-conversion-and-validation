# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest import *
import os
import unittest

from ...test.hamcrest import evaluates_to
from ...test.read_example_file import ExampleFileTest
from ..hathi import get_oclc_counts_from_json, get_hathi_data_from_json

class HathiFileTest (ExampleFileTest):
    this__file__ = __file__
    format_str = "hathitrust-{}.json"

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

class TestNewFileReader (HathiFileTest):
    filename = "706055947"

    def test_we_read_any_data (self):
        assert_that(self.file_data, is_not(empty()))

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

class ExpectingEmptyHathiData:

    def setUp (self):
        self.data = get_hathi_data_from_json(*self.args)

    def test_evaluates_to_false (self):
        assert_that(self.data, evaluates_to(False))

    def test_has_no_titles (self):
        assert_that(self.data.titles, is_(empty()))

    def test_has_no_htids (self):
        assert_that(self.data.htids, is_(empty()))

    def test_empty_data_has_title_distance_of_1 (self):
        assert_that(self.data.min_title_distance("anything"),
                    is_(close_to(1, 0.001)))

class GivenNoArgs (ExpectingEmptyHathiData, unittest.TestCase):
    args = ()

class GivenNull (ExpectingEmptyHathiData, unittest.TestCase):
    args = (None,)

class GivenEmptyStr (ExpectingEmptyHathiData, unittest.TestCase):
    args = ("",)

class GivenInvalidJson (ExpectingEmptyHathiData, unittest.TestCase):
    args = ("{{{{]]",)

class GivenJsonWithNoData (ExpectingEmptyHathiData, unittest.TestCase):
    args = ('{"records":{},"items":[]}',)

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
