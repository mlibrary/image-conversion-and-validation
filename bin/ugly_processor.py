#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import namedtuple
from falcom.api.reject_list import VolumeDataFromBarcode
from re import compile as re_compile

RE_14_BARCODE = re_compile(r"^[0-9]{14}$")
RE_PROTO_BARCODE = re_compile(r"^[Bb][0-9]+$")

UM_INSTITUTIONS = [
  "EYM",
  "BEU",
  "E8W",
  "EER",
  "EKL",
  "EMI",
  "EUQ",
  "EYD",
  "HJ8",
  "U2T",
  "UMSPO",
  "UMDON",
]

HATHI_INSTITUTIONS = [
  "HATHI",
]

CIC_INSTITUTIONS = [
  # University of Chicago
  "CGU",
  "IAB",
  "KEH",

  # University of Illinois
  "UIU",
  "ILG",
  "IAL",
  "LSI",
  "RHU",
  "RQF",
  "RQR",

  # Indiana University
  "AAAMC",
  "FSIUL",
  "I3U",
  "IJZ",
  "IUB",
  "IUG",
  "IUL",
  "IULGB",
  "IULSP",
  "RQQ",
  "XUL",
  "XYA",

  # University of Iowa
  "NUI",
  "LUI",
  "UIL",
  "UKO",

  # Michigan State University
  "EEM",
  "EVK",
  "MIMSU",
  "MSUTA",
  "MSUTP",

  # University of Minnesota
  "MNU",
  "DIF",
  "HOR",
  "MCR",
  "MLL",
  "MND",
  "MNH",
  "MNU",
  "MNUDS",
  "MNX",
  "MNY",
  "NRI",
  "UMM",
  "UMMBL",
  "XOR",

  # Northwestern University
  "INU",
  "FSINU",
  "INL",
  "INM",
  "INUQR",
  "JCR",
  "TSINU",
  "YO5",

  # Ohio State University
  "OSU",
  "OHL",
  "OS0",
  "OS1",
  "OS6",
  "ZH5",
  "ZH6",

  # Pennsylvania State University
  "UPM",
  "UPC",

  # Purdue University
  "IPL",
  "IPC",
  "IPN",
  "IUP",
  "HV6",

  # University of Wisconsin - Madison
  "GZI",
]

DataRow = namedtuple("DataRow",
                     ("bib",
                      "oclc",
                      "callno",
                      "author",
                      "title",
                      "desc",
                      "year1",
                      "year2",
                      "unique",
                      "numcic",
                      "numoth",
                      "numum",
                      "dumb",
                      "ht_mdp",
                      "ht_other"))

header_row = DataRow(
    "bib",
    "oclc",
    "callno",
    "author",
    "title",
    "desc",
    "pubdate",
    "",
    "unique",
    "cic",
    "noncic",
    "uofm",
    "whocares",
    "hathitrust_mdp",
    "hathitrust_other")

REQUIRED_FIELDS = {
    "bib":    "aleph bib number",
    "callno": "call number",
    "title":  "title",
    "year1":  "dates",
}

parser = ArgumentParser(description="Extend spreadsheets")
parser.add_argument("spreadsheets", nargs="+")
args = parser.parse_args()

tables = [ ]

for spreadsheet in args.spreadsheets:
    with open(spreadsheet, "r") as f:
        data = f.read().rstrip("\n")

    assert "\r" not in data, \
            "couldn't figure out newlines " + spreadsheet

    table = [r.split("\t") for r in data.split("\n") if r.strip("\t")]
    assert table, "empty table " + spreadsheet

    cols = len(table[0])
    for row in table[1:]:
        assert len(row) == cols, \
                "inconsistent column counts " + spreadsheet

    maybe_a_barcode = table[0][0]
    match = RE_14_BARCODE.match(maybe_a_barcode)

    if match is None:
        match = RE_PROTO_BARCODE.match(maybe_a_barcode)

    if match is not None:
        table.insert(0, [""] * cols)

    for row in table[1:]:
        assert row[-1] in {"DC", "DX", "DY", "DZ"}, \
                "invalid status {} in {}".format(repr(row[-1]),
                                                 spreadsheet)

    tables.append(table)

for table in tables:
    for row in table[1:]:
        print("{}\t{}".format(row[0], row[-1]))
