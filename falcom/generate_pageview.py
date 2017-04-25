# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class Pagetags:

    def __init__ (self):
        self.default_confidence = 100

    @property
    def default_confidence (self):
        return self.__default_confid

    @default_confidence.setter
    def default_confidence (self, value):
        self.__assert_valid_confid(value)
        self.__default_confid = value

    def generate_pageview (self):
        return ""

    def add_raw_tags (self, tag_data):
        if "hi" in tag_data:
            raise ValueError

    def __assert_valid_confid (self, confid):
        if not isinstance(confid, int) or confid < 100 or confid > 900:
            raise ValueError
