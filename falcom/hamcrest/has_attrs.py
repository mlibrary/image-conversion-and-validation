# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest.core.base_matcher import BaseMatcher

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
