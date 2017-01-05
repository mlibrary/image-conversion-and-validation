# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest.core.base_matcher import BaseMatcher

class IsDictWithExpectedKeys (BaseMatcher):

    def __init__ (self, description, *args):
        self.description = description
        self.fields = args

    def _matches (self, item):
        try:
            return all(x in item for x in self.fields) \
                    and len(item) == len(self.fields)

        except:
            return False

    def describe_to (self, description):
        field_list = ", ".join(repr(x) for x in self.fields)
        text = "a dictionary containing {} and only {} (i.e {})".format(
                self.description, self.description, field_list)

        description.append_text(text)

def contains_marc_fields():
    return IsDictWithExpectedKeys(
            "MARC fields",
            "bib",
            "callno",
            "oclc",
            "author",
            "title",
            "description",
            "years")
