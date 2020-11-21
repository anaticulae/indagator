# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import detector.bibliography.reference.freeand as freeand

LONGTEXT = """\
Rumph, H.-J., Hapke, U. & John, U. (1997). Lübecker Alkoholabhängigkeits- und
-missbrauchs-Screening-Test. Göttingen: Hogrefe Verlag GmbH & Co. KG.

Schmidt, R., Dettmeyer, R., Padosch, S. & Madea, B. (2004). Beweiswert
rechtsmedizinischer Begutachtungskriterien zur Feststellung der relativen
alkoholbedingten Fahruntüchtigkeit. Blutalkohol, 41, 1-10.

Schnabel, Eva (2011). Alcohol and driving-related performance - A
comprehensive meta-analysis focussing the significance of the
nonsignificant. Unveröffentlichte Dissertation, Philosophische Fakultät
II der Julius Maximilians-Universität, Würzburg.

Becker, W.; Ulrich, P.; Botzkowski, T.; Eurich, S. (2015): Data Analytics
in Familienunternehmen – Implikationen für das Controlling, in:
Zeitschrift für erfolgsorientierte Unternehmenssteuerung, Heft 27, 2015,
S. 263–268

Hahn, Hans Henning; Traba, Robert (Hrsg.) (2012-2015): Deutsch-Polnische
Erinnerungsorte. I. Geteilt/Gemeinsam; Deutsch-Polnische Erinnerungsorte
II. Geteilt gemeinsam; Deutsch-Polnische Erinnerungsorte III.
Parallelen; Deutsch-Polnische Erinnerungsorte IV. Reflexionen;
DeutschPolnische Erinnerungsorte V. Erinnerung auf Polnisch. Texte zu
Theorie und Praxis des sozialen Gedächtnisses. Paderborn u.a.:
Schöningh.

Keller, Thomas (2007a): Die Sainte Victoire – ein deutsch-französischer
Ort und seine Schatten. Cahiers d’Etudes Germaniques 53, H. 2, 93-122.
""".split('\n\n')


@pytest.mark.parametrize('text, title, authors, pages, year, publisher', [
    pytest.param(
        LONGTEXT[0],
        'Lübecker Alkoholabhängigkeits- und -missbrauchs-Screening-Test',
        [['Rumph', 'H.-J.'], ['Hapke', 'U.'], ['John', 'U.']],
        None,
        1997,
        None,
        id='luebecker',
    ),
    pytest.param(
        LONGTEXT[1],
        ('Beweiswert rechtsmedizinischer Begutachtungskriterien zur '
         'Feststellung der relativen alkoholbedingten Fahruntüchtigkeit'),
        [['Schmidt', 'R.'], ['Dettmeyer', 'R.'], ['Padosch', 'S.'],
         ['Madea', 'B.']],
        (1, 10),
        2004,
        None,
        id='schmidt',
    ),
    pytest.param(
        LONGTEXT[2],
        ('Alcohol and driving-related performance - A comprehensive '
         'meta-analysis focussing the significance of the nonsignificant'),
        [['Schnabel', 'Eva']],
        None,
        2011,
        None,
        id='schnabel',
    ),
    pytest.param(
        LONGTEXT[3],
        None,
        [['Becker', 'W.'], ['Ulrich', 'P.'], ['Botzkowski', 'T.'],
         ['Eurich', 'S.']],
        (263, 268),
        2015,
        None,
        id='becker',
    ),
    pytest.param(
        LONGTEXT[4],
        None,
        [['Hahn', 'Hans Henning'], ['Traba', 'Robert (Hrsg.)']],
        None,
        2012,
        None,
        id='hahn',
    ),
    pytest.param(
        LONGTEXT[5],
        'Die Sainte Victoire – ein deutsch-französischer Ort und seine Schatten',
        [['Keller', 'Thomas']],
        (93, 122),
        2007,
        None,
        id='keller',
    ),
])
def test_parse_freeand_long(text, title, authors, pages, year, publisher):  # pylint:disable=W0613
    extracted = freeand.parse_longtext(text)
    if title:
        assert extracted.title == title
    if pages:
        assert extracted.page == pages[0]
        if len(pages) == 2:
            assert extracted.pageend == pages[1]
    if year:
        assert extracted.year == year
    if authors:
        assert extracted.authors == authors


LONGTEXT_LINK = """\
Trim, John; North, Brian; Coste, Daniel (2001): Gemeinsamer Europäischer
Referenzrahmen für Sprachen: lernen, lehren, beurteilen.
http://student.unifr.ch/pluriling/assets/files/Referenzrahmen2001.pdf
Berlin; München: Langenscheidt KG.

Stratenschulte, Eckart D. (2014): Gründung der Europäischen
Gemeinschaften.
http://www.bpb.de/internationales/europa/europaeische-union/42989/europaeischegemeinschaften?p=all
(27.05.2018).

Macron, Emmanuel; Merkel, Angela (2018): Die deutsch-französische
Freundschaft geht alle etwas an!
https://www.youtube.com/watch?v=RXbcAYxuZxw (23.08.2018).

Landeszentrale für politische Bildung Baden-Württemberg (o.J.): Der
Elysée-Vertrag. https://www.lpb-bw.de/elysee-vertrag.html (01.07.2018).

Bundeskanzleramt Österreich (Hrsg.) (1992): Zentrale Orte Raumordnungsprogramm (NÖ)
https://www.ris.bka.gv.at/Dokumente/LgblNO/LRNI_1992062/LRNI_1992062.pdf (25.01.2018)
""".split('\n\n')


@pytest.mark.parametrize('text, authors, year, hyperlink, accessed, title', [
    pytest.param(
        LONGTEXT_LINK[0],
        None,
        2001,
        'http://student.unifr.ch/pluriling/assets/files/Referenzrahmen2001.pdf',
        None,
        None,
        id='trim',
    ),
    pytest.param(
        LONGTEXT_LINK[1],
        [['Stratenschulte', 'Eckart D.']],
        2014,
        'http://www.bpb.de/internationales/europa/europaeische-union/42989/europaeischegemeinschaften?p=all',
        (2018, 5, 27),
        None,
        id='stratenschulte',
    ),
    pytest.param(
        LONGTEXT_LINK[2],
        [['Macron', 'Emmanuel'], ['Merkel', 'Angela']],
        2018,
        'https://www.youtube.com/watch?v=RXbcAYxuZxw',
        (2018, 8, 23),
        None,
        id='macron',
    ),
    pytest.param(
        LONGTEXT_LINK[3],
        None,
        'no year',
        'https://www.lpb-bw.de/elysee-vertrag.html',
        (2018, 7, 1),
        None,
        id='landeszentrale',
    ),
    pytest.param(
        LONGTEXT_LINK[4],
        None,
        1992,
        'https://www.ris.bka.gv.at/Dokumente/LgblNO/LRNI_1992062/LRNI_1992062.pdf',
        (2018, 1, 25),
        'Zentrale Orte Raumordnungsprogramm (NÖ)',
        id='raumordnung',
    ),
])
def test_parse_freeand_with_link(
        text,
        authors,
        year,
        hyperlink,
        accessed,
        title,
):  # pylint:disable=W0613
    extracted = freeand.parse_longtext(text)
    assert extracted.year == year
    assert extracted.hyperlink == hyperlink
    assert extracted.accessed == accessed  # pylint:disable=E1101
    assert extracted.title == title or title is None
