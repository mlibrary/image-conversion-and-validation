# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from os import environ
from urllib.request import urlopen

from .uri import URI, APIQuerier
from .marc import get_marc_data_from_xml
from .worldcat import get_worldcat_data_from_json
from .hathi import get_oclc_counts_from_json
from .common import ReadOnlyDataStructure

AlephURI = URI("http://mirlyn-aleph.lib.umich.edu/cgi-bin/bc2meta")
WorldCatURI = URI("http://www.worldcat.org/webservices/catalog"
                  "/content/libraries/{oclc}")
HathiURI = URI("http://catalog.hathitrust.org/api/volumes/brief"
               "/oclc/{oclc}.json")

aleph_api = APIQuerier(AlephURI, url_opener=urlopen)
worldcat_api = APIQuerier(WorldCatURI, url_opener=urlopen)
hathi_api = APIQuerier(HathiURI, url_opener=urlopen)

wc_key = environ.get("MDP_REJECT_WC_KEY", "none")

class VolumeDataFromBarcode:

    def __init__ (self, barcode):
        self.barcode = barcode
        self.marc = get_marc_data_from_xml(aleph_api.get(
                        id=barcode,
                        type="bc",
                        schema="marcxml"))

        if not self.marc:
            self.marc = get_marc_data_from_xml(aleph_api.get(
                            id="mdp." + barcode,
                            schema="marcxml"))

        if self.marc.oclc is None:
            worldcat, hathi = None, None

        else:
            worldcat = worldcat_api.get(
                    oclc=self.marc.oclc,
                    wskey=wc_key,
                    format="json",
                    maximumLibraries="50")
            hathi = hathi_api.get(oclc=self.marc.oclc)

        self.worldcat = get_worldcat_data_from_json(worldcat)
        self.hathi = get_oclc_counts_from_json(hathi, "mdp." + barcode)
