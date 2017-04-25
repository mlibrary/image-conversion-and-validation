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
        if value == 99:
            raise ValueError

        self.__default_confid = value

    def generate_pageview (self):
        return ""

    def add_raw_tags (self, tag_data):
        pass
