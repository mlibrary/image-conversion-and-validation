# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import re
import xml.etree.ElementTree as ET

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

def get_marc_data_from_xml (xml):
    if xml is None:
        return MARCData()

    if not isinstance(xml, ET.Element):
        try:
            xml = ET.fromstring(xml)

        except ET.ParseError:
            return MARCData()

    marc = { }
    xmlns = "http://www.loc.gov/MARC21/slim"

    marc["bib"] = getattr(
            xml.find(".//{{{}}}controlfield[@tag='001']".format(xmlns)),
            "text", None)

    marc["callno"] = getattr(
            xml.find(".//{{{xmlns}}}datafield[@tag='MDP']/" \
                     "{{{xmlns}}}subfield[@code='h']".format(
                            xmlns=xmlns)),
            "text", None)

    marc["title"] = getattr(
            xml.find(".//{{{xmlns}}}datafield[@tag='245']/" \
                     "{{{xmlns}}}subfield[@code='a']".format(
                            xmlns=xmlns)),
            "text", None)

    oclcs = xml.findall(".//{{{xmlns}}}datafield[@tag='035']/" \
                     "{{{xmlns}}}subfield[@code='a']".format(
                            xmlns=xmlns))

    for maybe in oclcs:
        match = re.match(r"^\(OCoLC\).*?([0-9]+)$", maybe.text)
        if match:
            marc["oclc"] = match.group(1)
            break

    years = xml.find(".//{{{}}}controlfield[@tag='008']".format(xmlns))

    if years is not None:
        year1, year2 = years.text[7:11], years.text[11:15]
        if year1 == "^^^^": year1 = None
        if year2 == "^^^^": year2 = None
        marc["years"] = (year1, year2)

    return MARCData(**marc)
