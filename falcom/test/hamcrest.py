# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest.core.base_matcher import BaseMatcher

class ComposedAssertion (BaseMatcher):

    def _matches (self, item):
        self.failed_matcher = None
        self.mismatch_item = None
        self.extra_message = None

        for true_item, matcher, extra_message in \
                self.__assertion_triples(item):
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

    def __assertion_triples (self, item):
        return (self.__get_triple(x, item)
                        for x in self.assertion(item))

    def __get_triple (self, possible_tuple, item):
        if isinstance(possible_tuple, tuple):
            return self.__get_triple_from_tuple(possible_tuple, item)

        else:
            return item, possible_tuple, None

    def __get_triple_from_tuple (self, definite_tuple, item):
        if len(definite_tuple) == 3:
            return definite_tuple

        else:
            assert len(definite_tuple) == 2
            return definite_tuple + (None,)

class HasTruthiness (BaseMatcher):

    def __init__ (self, expected):
        self.expected = expected

    def _matches (self, item):
        return self.__get_bool_for(item) == self.expected

    def describe_to (self, description):
        description.append_text("an object with {} truthiness".format(
                repr(self.expected)))

    def describe_mismatch (self, item, description):
        actual = self.__get_bool_for(item)

        if actual is None:
            description.append_text("no truthiness ") \
                    .append_description_of(item)

        else:
            description.append_text("was {} ".format(actual)) \
                    .append_description_of(item)

    def __get_bool_for (self, item):
        try:
            result = bool(item)
            if result is True or result is False:
                return result

        except:
            pass

class HasAttrs (BaseMatcher):

    def __init__ (self, description_text, **kwargs):
        if description_text is None:
            description_text = "attrs"

        self.desc = description_text
        self.kwargs = kwargs

    def _matches (self, item):
        self.problem = None

        try:
            for key, value in self.kwargs.items():
                if not hasattr(item, key) \
                        or getattr(item, key) != value:
                    self.problem = key
                    return False

            return True

        except:
            return False

    def describe_to (self, description):
        if self.problem is None:
            attrs = ", ".join("s.{}={}".format(k, repr(v))
                    for (k, v) in self.kwargs.items())

        else:
            attrs = "including s.{}={}".format(
                    self.problem, repr(self.kwargs[self.problem]))

        description.append_text("a structure with {} {}".format(
                self.desc, attrs))

    def describe_mismatch (self, item, description):
        if self.problem is None:
            super().describe_mismatch(item, description)

        elif hasattr(item, self.problem):
            description.append_text("had s.{}={}".format(
                    self.problem, repr(getattr(item, self.problem))))

        else:
            description.append_text("didn't have s." + self.problem)

def evaluates_to_true():
    return HasTruthiness(True)

def evaluates_to_false():
    return HasTruthiness(False)
