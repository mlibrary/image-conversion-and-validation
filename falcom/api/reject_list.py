# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from os import environ
from time import sleep
from urllib.request import urlopen

from .uri import URI, APIQuerier
from .marc import get_marc_data_from_xml
from .worldcat import get_worldcat_data_from_json
from .hathi import get_oclc_counts_from_json, get_hathi_data_from_json

AlephURI = URI("http://mirlyn-aleph.lib.umich.edu/cgi-bin/bc2meta")
WorldCatURI = URI("http://www.worldcat.org/webservices/catalog"
                  "/content/libraries/{oclc}")
HathiURI = URI("http://catalog.hathitrust.org/api/volumes/brief"
               "/oclc/{oclc}.json")
BibURI = URI("http://catalog.hathitrust.org/api/volumes/brief"
             "/recordnumber/{bib}.json")

aleph_api = APIQuerier(AlephURI, url_opener=urlopen)
worldcat_api = APIQuerier(WorldCatURI, url_opener=urlopen)
hathi_oclc_api = APIQuerier(HathiURI, url_opener=urlopen)
hathi_bib_api = APIQuerier(BibURI, url_opener=urlopen)

wc_key = environ.get("MDP_REJECT_WC_KEY", "none")

class VolumeDataFromBarcode:

    barcode = None
    marc = None
    worldcat = None
    oclc_counts = None

    def __init__ (self, barcode):
        self.barcode = barcode

        while True:
            try:
                self.__get_marc_data()
                self.__get_oclc_data()
                break

            except ConnectionError:
                sleep(60*30)

    def hathi_title_match_percent (self):
        if self.marc.title is None:
            return "0.0"

        else:
            return self.__hathi_bib_data_has_title(self.marc.title)

    def __get_marc_data (self):
        self.marc = self.__marc_via_internal_barcode()

        if not self.marc:
            self.marc = self.__marc_via_htid()

    def __marc_via_internal_barcode (self):
        return get_marc_data_from_xml(aleph_api.get(
                        id=self.barcode,
                        type="bc",
                        schema="marcxml"))

    def __marc_via_htid (self):
        return get_marc_data_from_xml(aleph_api.get(
                        id="mdp." + self.barcode,
                        schema="marcxml"))

    def __get_oclc_data (self):
        worldcat, hathi = self.__get_json_through_oclc()

        self.worldcat = get_worldcat_data_from_json(worldcat)
        self.oclc_counts = get_oclc_counts_from_json(hathi)

    def __get_json_through_oclc (self):
        if self.marc.oclc is None:
            return None, None

        else:
            return self.__get_worldcat_json(), \
                    self.__get_hathi_json_via_oclc()

    def __get_worldcat_json (self):
        return worldcat_api.get(
                oclc=self.marc.oclc,
                wskey=wc_key,
                format="json",
                maximumLibraries="50")

    def __get_hathi_json_via_oclc (self):
        return hathi_oclc_api.get(oclc=self.marc.oclc)

    def __hathi_bib_data_has_title (self, title):
        hathi_json = self.__get_hathi_json_via_bib()
        hathi_data = get_hathi_data_from_json(hathi_json)

        return "{:.1f}".format(
                100 * (1 - hathi_data.min_title_distance(title)))

    def __get_hathi_json_via_bib (self):
        if self.marc.bib is None:
            return None

        else:
            return hathi_bib_api.get(bib=self.marc.bib)
