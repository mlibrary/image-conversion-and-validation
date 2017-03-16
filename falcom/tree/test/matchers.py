# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest.core.base_matcher import BaseMatcher

class TreeMatcher (BaseMatcher):
    actual_desc = ""

    def get_compare_value (self, item):
        return item

    def __init__ (self, expected_value):
        self.expected_value = expected_value

    def _matches (self, item):
        return self.get_compare_value(item) == self.expected_value

    def describe_to (self, description):
        description.append_text(self.expectation + " ") \
                   .append_description_of(self.expected_value)

    def describe_mismatch (self, item, description):
        if self.actual_desc:
            description.append_text("was ") \
                       .append_description_of(item) \
                       .append_text(" {} ".format(self.actual_desc)) \
                       .append_description_of(
                               self.get_compare_value(item))

        else:
            super().describe_mismatch(item, description)

class has_full_length (TreeMatcher):
    expectation = "a tree with a full length of"
    actual_desc = "with full length of"

    def get_compare_value (self, item):
        return item.full_length()

class iterates_into_list (TreeMatcher):
    expectation = "a tree that iterates into"
    actual_desc = "iterating into"

    def get_compare_value (self, item):
        return list(item)

class walks_into_list (TreeMatcher):
    expectation = "a tree that iterates recursively into"
    actual_desc = "recursively iterating into"

    def get_compare_value (self, item):
        return list(item.walk())

class has_node_value (TreeMatcher):
    expectation = "a tree node with a value of"

    def get_compare_value (self, item):
        return item.value
