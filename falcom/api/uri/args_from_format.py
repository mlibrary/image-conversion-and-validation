# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class FakeMappingThatRecordsAccessions:

    def __init__ (self):
        self.__set = set()

    def __getitem__ (self, key):
        self.__set.add(key)
        return 0

    def get_set (self):
        return self.__set

def get_expected_args_from_format_str (format_str):
    mapping = FakeMappingThatRecordsAccessions()
    format_str.format_map(mapping)

    return mapping.get_set()
