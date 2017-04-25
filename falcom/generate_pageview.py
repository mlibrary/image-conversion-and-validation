# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class Pagetags:

    def __init__ (self):
        self.default_confidence = 100
        self.__tags = ()

    @property
    def default_confidence (self):
        return self.__default_confid

    @default_confidence.setter
    def default_confidence (self, value):
        self.__assert_valid_confid(value)
        self.__default_confid = value

    def generate_pageview (self):
        return "\n".join(self.__get_pageview_row(i)
                         for i in range(len(self.__tags)))

    def add_raw_tags (self, tag_data):
        if "tags" not in tag_data:
            raise ValueError

        self.__tags = tag_data["tags"]

    __pageview_row = "0{s:07d}.tif\t0{s:07d}\t{n:>08s}\t{c:d}\t{f:s}"

    def __assert_valid_confid (self, confid):
        if not isinstance(confid, int) or confid < 100 or confid > 900:
            raise ValueError

    def __get_pageview_row (self, i):
        tags = self.__tags[i]
        return self.__pageview_row.format(s=i+1,
                                          n=tags.get("number", ""),
                                          c=self.default_confidence,
                                          f=tags.get("feature", ""))
