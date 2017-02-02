#!/usr/bin/env python3
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

COLUMN_HEADERS = [
  [:bib,      "bib"],
  [:oclc,     "oclc"],
  [:callno,   "callno"],
  [:author,   "author"],
  [:title,    "title"],
  [:desc,     "desc"],
  [:year1,    "pubdate"],
  [:year2,    ""],
  [:unique,   "unique"],
  [:numcic,   "cic"],
  [:numoth,   "noncic"],
  [:numum,    "uofm"],
  [:dumb,     "whocares"],
  [:ht_mdp,   "hathitrust_mdp"],
  [:ht_other, "hathitrust_other"],
]

REQUIRED_FIELDS = {
  :bib    => "aleph bib number",
  :callno => "call number",
  :title  => "title",
  :year1  => "dates",
}
