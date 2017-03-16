# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest.core.base_matcher import BaseMatcher

class TreeMatcher (BaseMatcher):

    def __init__ (self, expected_value):
        self.expected_value = expected_value

    def describe_to (self, description):
        description.append_text(
                self.expectation.format(repr(self.expected_value)))

class has_full_length (TreeMatcher):
    expectation = "a tree with a full length of {}"

    def _matches (self, item):
        return item.full_length() == self.expected_value

class iterates_into_list (TreeMatcher):
    expectation = "a tree that iterates into {}"

    def _matches (self, item):
        return list(item) == self.expected_value

class iterates_recursively_into_list (TreeMatcher):
    expectation = "a tree that iterates recursively into {}"

    def _matches (self, item):
        return list(item.walk()) == self.expected_value

class has_value (TreeMatcher):
    expectation = "a tree node with a value of {}"

    def _matches (self, item):
        return item.value == self.expected_value
