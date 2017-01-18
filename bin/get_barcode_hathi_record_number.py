#!/usr/bin/env python3
# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from argparse import ArgumentParser
from urllib.request import urlopen

from falcom.api.uri import URI, APIQuerier
from falcom.api.marc import get_marc_data_from_xml

AlephURI = URI("http://mirlyn-aleph.lib.umich.edu/cgi-bin/bc2meta")
aleph_api = APIQuerier(AlephURI, url_opener=urlopen)

parser = ArgumentParser(description="Get info for barcodes")
parser.add_argument("barcodes", nargs="+")

args = parser.parse_args()

for barcode in args.barcodes:
    marc = get_marc_data_from_xml(aleph_api.get(
                    id=barcode,
                    type="bc",
                    schema="marcxml"))

    if not marc:
        marc = get_marc_data_from_xml(aleph_api.get(
                        id="mdp."+barcode,
                        schema="marcxml"))

    if marc.bib:
        print("\t".join((barcode, marc.bib)))
