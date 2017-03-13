# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest.core.base_matcher import BaseMatcher

class a_method (BaseMatcher):

    def _matches (self, item):
        return callable(item)

    def describe_to (self, description):
        description.append_text("a function or callable object")
