# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest.core.base_matcher import BaseMatcher

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
        self.problem = None

    def _matches (self, item):
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

def has_marc_attrs(**kwargs):
    return HasAttrs("MARC attrs", **kwargs)
