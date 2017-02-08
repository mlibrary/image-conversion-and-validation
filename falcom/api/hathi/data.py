# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from re import compile as re_compile

from ..common.read_only_data_structure import ReadOnlyDataStructure

class HathiData (ReadOnlyDataStructure):

    __re_symbol = re_compile(r"[^0-9A-Za-z\s]")
    __re_spaces = re_compile(r"\s+")

    @property
    def titles (self):
        return self.get("titles", ())

    @property
    def htids (self):
        return self.get("htids", ())

    def get_item_counts (self, htid):
        matching_count = len([x for x in self.htids if x == htid])
        nonmatching_count = len(self.htids) - matching_count

        return matching_count, nonmatching_count

    def has_title (self, title):
        soft_title = self.__soften(title)

        return any(self.__are_soft_equal(x, soft_title)
                for x in self.titles)

    def min_title_distance (self, title):
        return 1

    def __are_soft_equal (self, text, already_softened_text):
        return self.__soften(text) == already_softened_text

    def __soften (self, text):
        return self.__re_spaces.sub(" ", self.__re_symbol.sub("", text)).lower()
