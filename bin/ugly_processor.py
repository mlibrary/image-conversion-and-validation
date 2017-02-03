#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import namedtuple
from datetime import datetime
from falcom.api.reject_list import VolumeDataFromBarcode
from re import compile as re_compile

RE_14_BARCODE = re_compile(r"^[0-9]{14}$")
RE_PROTO_BARCODE = re_compile(r"^[Bb][0-9]+$")

UM_INSTITUTIONS = {
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
}

HATHI_INSTITUTIONS = {
  "HATHI",
}

CIC_INSTITUTIONS = {
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
}

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

tables = { }

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

    tables[spreadsheet] = table

barcode_filename = datetime.now().strftime("barcode-%Y%m%d.txt")

for filename, table in tables.items():
    print("Processing {} ...".format(filename))
    new_table = [table[0] + list(header_row)]
    barcode_lines = [ ]

    for i in range(1, len(table)):
        row = table[i]
        barcode = row[0]
        status = row[-1]

        print("  {:<14s} ({:d}/{:d}) ...".format(
                        barcode, i, len(table) - 1))

        data = VolumeDataFromBarcode(barcode)

        if data.marc:
            numcic = 0
            numoth = 0
            numum = 0
            dumb = 0
            for code in data.worldcat:
                if code in HATHI_INSTITUTIONS:
                    dumb += 1
                elif code in UM_INSTITUTIONS:
                    numum += 1
                elif code in CIC_INSTITUTIONS:
                    numcic += 1
                else:
                    numoth += 1

            if numcic > 0:
                is_unique = numcic + numoth < 3

            else:
                is_unique = numcic + numoth < 5

            extension = DataRow(
                    data.marc.bib,
                    data.marc.oclc,
                    data.marc.callno,
                    data.marc.author,
                    data.marc.title,
                    data.marc.description,
                    data.marc.years[0],
                    data.marc.years[1],
                    "unique" if is_unique else "",
                    "{:d}".format(numcic),
                    "{:d}".format(numoth),
                    "{:d}".format(numum),
                    "{:d}".format(dumb),
                    "{:d}".format(data.oclc_counts[0]),
                    "{:d}".format(data.oclc_counts[1]))

            new_row = row + list(extension)
            new_table.append("" if x is None else x
                             for x in new_row)

            barcode_lines.append("{}\t{}\n".format(barcode, status))

    with open(filename, "w") as spreadsheet_file:
        for row in new_table:
            spreadsheet_file.write("\t".join(row) + "\n")

    with open(barcode_filename, "a") as barcode_file:
        barcode_file.write("".join(barcode_lines))

print("Done.")
