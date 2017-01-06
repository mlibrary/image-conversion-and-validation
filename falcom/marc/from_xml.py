# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import re
import xml.etree.ElementTree as ET

from .marcdata import MARCData

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
