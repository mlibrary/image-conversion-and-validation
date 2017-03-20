# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from distance import levenshtein
from re import compile as re_compile

from ..common.read_only_data_structure import ReadOnlyDataStructure

class HathiData (ReadOnlyDataStructure):

    auto_properties = (
        ("titles", ()),
        ("htids", ()),
    )

    __re_symbol = re_compile(r"[^0-9A-Za-z\s]")
    __re_spaces = re_compile(r"\s+")

    def get_item_counts (self, htid):
        matching_count = len([x for x in self.htids if x == htid])
        nonmatching_count = len(self.htids) - matching_count

        return matching_count, nonmatching_count

    def has_title (self, title):
        return self.min_title_distance(title) < 0.01

    def min_title_distance (self, title):
        try:
            return min(self.__title_distances(title))

        except ValueError:
            return 1

    def __title_distances (self, title):
        soft_title = self.__soften(title)

        return (self.__soft_distance(t, soft_title)
                for t in self.titles)

    def __soft_distance (self, text, already_softened_text):
        return levenshtein(already_softened_text,
                           self.__soften(text),
                           normalized=True)

    def __soften (self, text):
        without_symbols = self.__re_symbol.sub("", text)
        collapsed_spaces = self.__re_spaces.sub(" ", without_symbols)
        return collapsed_spaces.lower()
