# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest.core.base_matcher import BaseMatcher

class ComposedAssertion (BaseMatcher):

    def _matches (self, item):
        self.failed_matcher = None
        self.mismatch_item = None
        self.extra_message = None

        for possible_tuple in self.assertion(item):
            true_item = item
            extra_message = None

            if isinstance(possible_tuple, tuple):
                if len(possible_tuple) == 3:
                    true_item, matcher, extra_message = possible_tuple

                else:
                    true_item, matcher = possible_tuple

            else:
                matcher = possible_tuple

            if not matcher.matches(true_item):
                self.failed_matcher = matcher
                self.mismatch_item = true_item
                self.extra_message = extra_message
                return False

        return True

    def describe_to (self, description):
        if self.extra_message is not None:
            description.append_text("{} ".format(self.extra_message))

        self.failed_matcher.describe_to(description)

    def describe_mismatch (self, item, description):
        self.failed_matcher.describe_mismatch(self.mismatch_item,
                                              description)
