# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class MARCData:

    @property
    def bib (self):
        return self.__marc_dict.get("bib", None)

    @property
    def callno (self):
        return self.__marc_dict.get("callno", None)

    @property
    def oclc (self):
        return self.__marc_dict.get("oclc", None)

    @property
    def author (self):
        return self.__marc_dict.get("author", None)

    @property
    def title (self):
        return self.__marc_dict.get("title", None)

    @property
    def description (self):
        return self.__marc_dict.get("description", None)

    @property
    def years (self):
        return self.__marc_dict.get("years", (None, None))

    def __init__ (self, **kwargs):
        self.__marc_dict = kwargs
        null_keys = [k for k, v in kwargs.items() if v is None]
        for key in null_keys:
            del kwargs[key]

    def __bool__ (self):
        return bool(self.__marc_dict)
