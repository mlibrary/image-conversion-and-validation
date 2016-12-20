# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
import unittest

from ..aleph import MARCData

EG_MARC_39015079130699 = """\
<record xmlns="http://www.loc.gov/MARC21/slim" xmlns:xsi="http://www.w3\
.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/MA\
RC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">
<controlfield tag="FMT">BK</controlfield>
<controlfield tag="LDR">00000ntm^^22^^^^^^a^4500</controlfield>
<controlfield tag="001">006822264</controlfield>
<controlfield tag="005">20131023140847.0</controlfield>
<controlfield tag="006">m^^^^^^^^d^^^^^^^^</controlfield>
<controlfield tag="007">cr^bn^---auaua</controlfield>
<controlfield tag="008">090623q17901791tu^^^^^^^^^^^^00|^||ota^d</contr\
olfield>
<datafield tag="040" ind1=" " ind2=" ">
<subfield code="a">MiU</subfield>
<subfield code="c">MiU</subfield>
<subfield code="e">amremm</subfield>
</datafield>
<datafield tag="041" ind1="0" ind2=" ">
<subfield code="a">ota</subfield>
</datafield>
<datafield tag="043" ind1=" " ind2=" ">
<subfield code="a">n-us-mi</subfield>
<subfield code="a">a-tu---</subfield>
</datafield>
<datafield tag="066" ind1=" " ind2=" ">
<subfield code="c">(3</subfield>
</datafield>
<datafield tag="245" ind1="0" ind2="0">
<subfield code="6">03</subfield>
<subfield code="a">[Calligraphic specimen,</subfield>
<subfield code="f">1205?, i.e. 1790 or 1791?].</subfield>
</datafield>
<datafield tag="245" ind1="0" ind2="0">
<subfield code="6">03</subfield>
<subfield code="a">[مرقع حسن الخط,</subfield>
<subfield code="f">1205ه؟, 1790 او 1791م؟].</subfield>
</datafield>
<datafield tag="260" ind1=" " ind2=" ">
<subfield code="c">[1790 or 1791?].</subfield>
</datafield>
<datafield tag="300" ind1=" " ind2=" ">
<subfield code="a">8 leaves :</subfield>
<subfield code="b">paper ;</subfield>
<subfield code="c">175 x 468 (98 x 395) mm.</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Ms. codex.</subfield>
</datafield>
<datafield tag="520" ind1="8" ind2=" ">
<subfield code="a">Exquisite album of calligraphy (muraqqaʻ or murakkaa\
) with design for a monumental inscription to appear in stone on a comm\
emorative range marker (menzil taşı) of Bilâl Ağa (d.1807?), likely exe\
cuted by Yesari Mehmed Esad Efendi (d.1798), the great Ottoman master o\
f nastaʻlīq (talik).</subfield>
</datafield>
<datafield tag="546" ind1=" " ind2=" ">
<subfield code="a">Ottoman Turkish.</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Title supplied by cataloguer.</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Incipit: "جناب حضرت سلطان سليم خان جهانبانك ..."</su\
bfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Explicit: "قيروب بيك ايكيوز بش سالى دستى پيك اديم ير\
ده"</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Collation: Eight heavy leaves or 'panels' hinged tog\
ether.</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Layout: Written in a single line per page (opens ver\
tically with lines running parallel to the spine).</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Script: Exquisite specimen of Ottoman calligraphy ; \
text throughout in an elegant, large nastaʻlīq (celi talik) in a heavy \
line ; pin-pricks surround each letter, presumably for transfer to the \
commemorative stone by pouncing.</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Decoration: Written area surrounded by frame consist\
ing of inner orange band and heavy gold outer band, outlined in black f\
illets.</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Support: Well-burnished laid paper (with roughly 8 v\
ertical laid lines per cm.) mounted on heavy paper with pieced marbled \
paper (kumlu or kılçıklı ebru in blue and cream) framing the written ar\
ea.</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Binding: Pasteboards faced in cream silk with dark r\
ed leather over spine and edges / turn-ins (silk faced, leather edged, \
framed binding) ; Type III binding (without flap) ; boards and recto of\
 opening and final panel lined in marbled paper (kumlu or kılçıklı ebru\
 in pink, light blue, and dark blue) ; upper and lower covers carry gol\
d-tooled border in a series of s-shaped stamps ; panels hinged together\
 with dark red leather ; in somewhat poor condition with lifting of sil\
k and leather, delamination of boards, much abrasion, staining, panels \
detaching from spine, etc.</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Former shelfmark: "538 T. De M. [i.e. Tammaro De Mar\
inis]" inscribed in pencil on upper cover.</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Origin: Date at close, 1205 [1790 or 91] during the \
reign of Sultan Selim III (r.1789-1807). Most likely executed by the ma\
ster calligrapher Mehmet Esat Yesari (d.1798) as proposed by Muhittin S\
erin (see note on catalog card dated "20.4.1993") and Mohamed Zakariya \
and confirmed by Uğur Derman.</subfield>
</datafield>
<datafield tag="561" ind1=" " ind2=" ">
<subfield code="a">Inscription in pencil on upper cover "538 T. De M. [\
i.e. Tammaro De Marinis]" ; clean copy.</subfield>
</datafield>
<datafield tag="541" ind1=" " ind2=" ">
<subfield code="c">Purchase ;</subfield>
<subfield code="a">Acquired by purchase (funds donated by Horace Rackha\
m).</subfield>
<subfield code="d">1924.</subfield>
</datafield>
<datafield tag="510" ind1="4" ind2=" ">
<subfield code="a">Brocade of the pen : the art of Islamic writing. Car\
ol Garrett Fisher, ed. (East Lansing, MI: Kresge Art Museum, Michigan S\
tate University, 1991),</subfield>
<subfield code="c">no.12, p.84</subfield>
</datafield>
<datafield tag="510" ind1="4" ind2=" ">
<subfield code="a">Zakariya, Mohamed. "Islamic calligraphy: A technical\
 overview." In Brocade of the pen: the art of Islamic writing. Carol Ga\
rrett Fisher, ed. (East Lansing, MI: Kresge Art Museum, Michigan State \
University, 1991):</subfield>
<subfield code="c">1-17</subfield>
</datafield>
<datafield tag="510" ind1="4" ind2=" ">
<subfield code="a">Derman, M. Uğur. Letters in gold : Ottoman calligrap\
hy from the Sakıp Sabancı collection, Istanbul. (New York : Metropoliti\
an Museum of Art : Distributed by H.N. Abrams, c1998),</subfield>
<subfield code="c">100-1.</subfield>
</datafield>
<datafield tag="538" ind1=" " ind2=" ">
<subfield code="a">Mode of access: Internet.</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Shelfmark: Ann Arbor, University of Michigan, Specia\
l Collections Library, Isl. Ms. 402</subfield>
</datafield>
<datafield tag="650" ind1=" " ind2="0">
<subfield code="a">Islamic calligraphy</subfield>
<subfield code="z">Turkey</subfield>
<subfield code="v">Specimens.</subfield>
</datafield>
<datafield tag="650" ind1=" " ind2="0">
<subfield code="a">Calligraphy, Turkish</subfield>
<subfield code="v">Specimens.</subfield>
</datafield>
<datafield tag="650" ind1=" " ind2="0">
<subfield code="a">Writing, Arabic</subfield>
<subfield code="v">Specimens.</subfield>
</datafield>
<datafield tag="650" ind1=" " ind2="0">
<subfield code="a">Manuscripts, Turkish</subfield>
<subfield code="z">Michigan</subfield>
<subfield code="z">Ann Arbor.</subfield>
</datafield>
<datafield tag="700" ind1="0" ind2=" ">
<subfield code="6">05</subfield>
<subfield code="a">Yesari Mehmet Esat Efendi,</subfield>
<subfield code="d">d. 1798,</subfield>
<subfield code="e">calligrapher.</subfield>
</datafield>
<datafield tag="700" ind1="0" ind2=" ">
<subfield code="6">05</subfield>
<subfield code="a">يسارى محمد اسعد افندى,</subfield>
<subfield code="e">خطاط.</subfield>
</datafield>
<datafield tag="700" ind1="0" ind2=" ">
<subfield code="a">Abdülhamid</subfield>
<subfield code="b">II,</subfield>
<subfield code="c">Sultan of the Turks,</subfield>
<subfield code="d">1842-1918,</subfield>
<subfield code="e">former owner.</subfield>
</datafield>
<datafield tag="773" ind1="0" ind2=" ">
<subfield code="a">Abdul Hamid Collection.</subfield>
</datafield>
<datafield tag="997" ind1=" " ind2=" ">
<subfield code="a">MARS</subfield>
</datafield>
<datafield tag="998" ind1=" " ind2=" ">
<subfield code="a">EK 6-23-09 ; examined EK May-11 ; EK 5-18-11</subfie\
ld>
</datafield>
<datafield tag="MDP" ind1=" " ind2=" ">
<subfield code="h">Isl. Ms. 402</subfield>
<subfield code="u">mdp.39015079130699</subfield>
<subfield code="b">SPEC</subfield>
<subfield code="c">ISLM</subfield>
</datafield>
</record>"""

class TestMARCData (unittest.TestCase):

    def test_degenerate (self):
        marc = MARCData(EG_MARC_39015079130699)
        self.assertEqual(marc.bib, "006822264")
