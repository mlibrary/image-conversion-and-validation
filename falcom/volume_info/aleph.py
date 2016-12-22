# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import xml.etree.ElementTree as ET

INDEX_OF_FIRST_YEAR_SUBSTR = 7
INDEX_OF_SECOND_YEAR_SUBSTR = 11
NUMBER_OF_CHARS_IN_A_YEAR = 4
MARC_NULL_YEAR = "^^^^"

class MARCData:

    xmlns = "http://www.loc.gov/MARC21/slim"
    description = None # should be datafield(MDP, z)

    def __init__ (self, xml):
        self.__root = ET.fromstring(xml)
        self.bib = self.__get_controlfield("001")
        self.callno = self.__get_datafield("MDP", "h")
        self.author = self.__get_datafield("100", "a")
        self.title = self.__get_datafield("245", "a")

        self.__set_years()

    def __get_controlfield (self, tag):
        return self.__get_text_if_not_none(
                ".//{{{xmlns}}}controlfield[@tag='{}']".format(
                        tag, xmlns=self.xmlns))

    def __get_datafield (self, tag, code):
        return self.__get_text_if_not_none(
                ".//{{{xmlns}}}datafield[@tag='{}']/"
                "{{{xmlns}}}subfield[@code='{}']".format(
                        tag, code, xmlns=self.xmlns))

    def __get_text_if_not_none (self, xpath):
        elt = self.__root.find(xpath)

        return getattr(elt, "text", None)

    def __set_years (self):
        full_str = self.__get_controlfield("008")
        self.years = self.__get_first_year(full_str), \
                self.__get_second_year(full_str)

    def __get_first_year (self, full_str):
        return self.__get_year_substr(full_str,
                INDEX_OF_FIRST_YEAR_SUBSTR)

    def __get_second_year (self, full_str):
        return self.__get_year_substr(full_str,
                INDEX_OF_SECOND_YEAR_SUBSTR)

    def __get_year_substr (self, full_str, start_index):
        result = full_str[start_index:start_index +
                NUMBER_OF_CHARS_IN_A_YEAR]

        return None if result == MARC_NULL_YEAR else result
