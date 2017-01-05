# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from hamcrest.core.base_matcher import BaseMatcher

class ContainsMarcFields (BaseMatcher):

    marc_fields = (
            "bib",
            "callno",
            "oclc",
            "author",
            "title",
            "description",
            "years",
    )

    def _matches (self, item):
        try:
            return all(x in item for x in self.marc_fields) \
                    and len(item) == len(self.marc_fields)

        except:
            return False

    def describe_to (self, description):
        marc_str = ", ".join(repr(x) for x in self.marc_fields)

        description.append_text("a dictionary containing MARC fields") \
                   .append_text(" (i.e. {})".format(marc_str))

def contains_marc_fields():
    return ContainsMarcFields()
