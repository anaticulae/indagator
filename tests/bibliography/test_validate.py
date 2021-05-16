# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import detector.path
import tests


def bachelor51(flat):
    assert len(flat) == 37  # VALIDATED


BACHELOR56 = """\
Breitmeier D. ; Seeland-Schulze I. ; Hecker H. ; Schneider U.
Beirness D. ; Vogel-Sprott M.
Borkenstein R. F. ; Crowther R. F. ; Shumate R. P. ; Ziel W. B. ; Zylman R.
Bundesministerium  der Justiz  und  für  Verbraucherschutz
Burian S.  E. ; Hensberry R. ; Liguori A.
Fillmore M.  T. ; Carscadden J.  L. ; Vogel-Sprott M.
Hansen M. A.
Harrison E. L. R. ; Fillmore M. T.
Heuer K.
Kazenwadel J. ; Vollrath M.
Kolasinski E. M.
Krampe A.
Krüger H.-P. ; Kazenwadel J. ; Vollrath M.
Kuratorium  für Verkehrssicherheit
Marczinski C. A. ; Fillmore M. T.
Martin T. L ; Solbeck P. A. M. ; Mayers D. J. ; Langille R. M. ; Buczek Y. ; Pelletier M. R.
Moskowitz H. ; Fiorentino D.
Moskowitz H. ; Fiorentino D.
Moskowitz H. ; Robinson C. D.
Rumph H.-J. ; Hapke U. ; John U.
Schmidt R. ; Dettmeyer R. ; Padosch S. ; Madea B.
Schnabel Eva
Sdao-Jarvie K. ; Vogel-Sprott M.
Statistisches Bundesamt
Statistisches Bundesamt
Strafgesetzbuch
Verkehrsunfallstatistik Braunschweig
Vogel-Sprott M.
Vogel-Sprott M. ; Sdao-Jarvie K.
Vollrath M.
Vollrath M. ; Krems J.
Würzburger  Institut  für Verkehrswissenschaften  GmbH
"""


def bachelor56(flat):
    raw = authors_raw(flat)
    assert raw == BACHELOR56.strip()


def bachelor63(flat):
    # zero is iamraw.NoPerson
    # numbers iamraw.Person
    expected = [2, 1, 1, 2, 0, 1, 1, 0, 1, 1, 2, 1]
    parsed = []
    for item in flat:
        authors = item.authors
        if not authors:
            parsed.append(None)
            continue
        if all([isinstance(item, iamraw.Person) for item in authors]):
            parsed.append(len(authors))
            continue
        # no person
        parsed.append(0)
    assert parsed == expected


def bachelor90(flat):
    references = [item.reference for item in flat]
    expected = [
        'Ju04', 'AT09', 'Bae08', 'BAU11', 'BKL+09', 'Bus98', 'But11', 'CJM12',
        'Dav72', 'DDG09', 'DIN08', 'Dor10', 'DRP01', 'emf12', 'FLS07', 'Fos10',
        'Güe06', 'Hal93', 'Hof08', 'Hue10', 'Ibr04', 'ISO03', 'ISO05', 'JL07',
        'K.11', 'Lig09', 'Mar07', 'Mat09', 'mat12a', 'mat12b', 'mat12c',
        'mis98', 'NN09', 'OK09', 'Ole10', 'Plu06', 'PP04', 'PR06', 'Rei12',
        'Rum05', 'SBD+10', 'Sch05', 'Sta73', 'Sta09', 'Ste12', 'TS07', 'TZ10',
        'VAC+08', 'VG06', 'WL11', 'WR10', 'ZSM11'
    ]
    assert references == expected


def master89(flat):
    first = flat[0]
    assert first.year == 2010
    assert first.authors == [('ABELS', 'Heinz'), ('KÖNIG', 'Alexandra')]

    second = flat[1]
    assert second.year == 2009
    assert second.authors == [('ANDRONIKASHVILI', 'Zaal')]

    last = flat[-1]
    assert last.year == 2009


def master75(flat):  # pylint:disable=W0613
    pass


def master110(flat):
    titles = [item.title for item in flat if item.title]
    assert len(titles) >= 66  # NOT VALIDATED


def master116(flat):
    expected = [
        'App14', 'Bah12', 'Bas14', 'Bor13', 'Bra11', 'Dit13', 'Don04', 'EB03',
        'EPA98', 'Fil15', 'Fis12', 'Fri15', 'Gas13', 'Gev13', 'Hei13', 'Hof11',
        'IAV15', 'Jaa13', 'Kac14', 'Kon13', 'Kur16', 'Les15', 'LG03', 'Mü13',
        'Mag14', 'MAT16', 'Min13', 'Mor09', 'Nit11', 'Pac12', 'Pap15', 'Pfe14',
        'Rö15', 'Rei10', 'Rie11', 'RNB12', 'Sch09', 'Sko11', 'Spi05', 'Stö10',
        'Tom12', 'Tsc12', 'Vö15', 'Wik07', 'Wik13', 'Wit13'
    ]
    references = [item.reference for item in flat]
    assert references == expected
    authors = [item.authors for item in flat]
    assert authors


def diss170(flat):
    # 11+11+11+12+11+11+11+11+11+13+11+13+5
    assert len(flat) == 146  # change to 142!


def diss272(flat):
    # 11 11 11 9 10 11 11 11 12 11 12 3 = 124
    assert len(flat) == 120  # TODO: CHANGES LATER


def bachelor128(flat):
    assert flat
    # 51: Validated by hand
    assert len(flat) == 47


def master91b(flat):
    assert flat
    assert len(flat) == 85  # VALIDATED


ORDER107 = """\
Büker Stella
Deppe Joachim
Deutsche Norm DIN 1421
Deutsche Norm DIN 1422 Teil 1
Deutsche Norm DIN 1422 Teil 3
Deutsche Norm DIN 1426
Dreyer Hilke ; Schmitt Richard
Duden. Die deutsche Rechtschreibung
Duden. Grammatik der deutschen Gegenwartssprache
Ebel Hans F. ; Bliefert Claus
ETH Zürich (Eidgenössische Technische Hochschule Zürich)
Kerans Mary Ellen
Kruse Otto
Langer Inghard ; Schulz von Thun Friedemann ; Tausch Reinhard
Meer Dorothee
o.A.
TU Berlin
Weber-Wulff Debora
Arndt Wulf-Holger
Esser Peter ; Lippert Jana und Tutorenteam (überarb.)
Gemünden Hans Georg
Herrmann Klaus
Köppel Johann ; Lippert Jana
Krallmann Hermann
Krystek Ulrich
Mirow Michael
o.A.
Straube Frank
Werder Axel v.
Zarnekow Rüdiger
Grafische  Gestaltung  von  Titelbild  und  Abbildungen  (wenn  nicht  anders angegeben)
""".strip()


def order107(flat):
    raw = authors_raw(flat)
    assert raw == ORDER107


MASTER155 = """\
Allen W.  D. ; Evans D.  A.
Altmann S. ; Falk A. ; Marklein F.
Anderson M.  J. ; Blue E.  R.
Ang J.  S. ; Schwarz T.
Arrow K.  J. ; Debreu G.
Ball S. B. ; Bazerman M. H. Caroll ; J. S.
Baye M. R. ; Morgan J. ; Scholten P.
Bazerman M. H. ; Magliozzi T. ; Neale M.  A.
Bester H.
Blackburn J.  M.
Bohm P.
Brandts J. ; Charness G.
Brandts J. ; Gerxheim K. ; Schram A. ; Ygosse-Battisti J.
Brehmer B.
Bundesregierung  der  Bundesrepublik  Deutschland
ab  01.01.1980.  Internet
Burdett K. ; Judd K. L.
Camerer C.  F. ; Hogarth R.  M.
Chamberlin E. H.
Charness G.
Charness G.
Chase W. G. ; Simon H. A.
Chen S.-H. ; Hsieh Y.-L.
Cheung S.  L. ; Palan S.
Cooper D. ; Kagel J. ; Lo W. ; Gu Q.
Davis D. ; Holt C.  A.
Diamond P.  A.
Diamond P. A. ; Maskin E.
Dorsch F. ; Häcker H. ; Stapf K.  H.  (Hrsg.)
Dürsch P. ; Oechssler J. ; Vadovic R.
Eagly A.  H. ; Carli L.  L.
Eckard E. W.
Eisenführ F. ; Weber M.
Erne M.
Fehr E.  Kirchler ; E. Weichbold ; A. Gächter ; S.
Fehr E. ; Gächter S. ; Kirchsteiger G.
Fehr E. ; Kirchsteiger G. ; Riedl A.
Fellner G. ; Maciejovsky B.
Fiedler M.
Fisher F. M.
Friberg R. ; Ganslandt M. ; Sandström M.
Gatti R. ; Kattuman P.
Gneezy U. ; Kapteyn A. ; Potters J.
Günther M ; Vossebein U. ; Wildner R.
Hammann P. ; Erichson B.
Hannan L. ; Kagel J. ; Moser D.
Harrison G.  W. ; Johnson E. ; McInnes M.  M. ; Rutström E.  E.
Holt C.  A.
Holt C. A. ; Laury S. K.
Hong H. Shum ; M.
Hudgens G. A. ; Fatkin L. T.
Irlenbusch B. ; Sliwka D.
Irlenbusch B. ; Sliwka D.
Jehle G.  A. ; Reny P.  J.
Kaase M.  (Hrsg.)
Kachelmeier S. ; Limberg S. ; Schadewald M.
Katzner D.  W.
Kujal P. ; Smith V. L.
Kuß A.
Kuß A. ; Eisend M.
Kußmaul H.
Leibbrandt A.
Leigh T.
Leigh T.
Levin I. P. ; Snyder M. A. ; Chapman D. P.
Lingen T.  v.
Major B. ; McFarlin D.  B. ; Gagnon D.
Malhotra N. K. ; Birks D. F.
Mankiw N.  G. ; Taylor M.  P.
March J.  G.
March J. G. ; Simon H. A.
Marshall A.
Matheson K.
Mortensen D.  A.
Neale M.  A. ; Huber V. ; Northcraft G.
Neale M.  A. ; Northcraft G.
Neu J. ; Graham J. L. ; Gilly M. C.
Oberender P. ; Zerth J.
Parson H.  M.
Powell M. ; Ansic D.
Pruitt D.  G.  Carnevale ; P.  J.  D. Forcey ; B. Van  Slyck ; M.  V.
Rancer A. S. ; Baukus R. A.
Rapoport A. ; Chammah M.
Cooperation. Ann Arbor
Riley W. B. ; Chow K. V.
Rubin J.  Z. ; Brown B.  R.
Rubinstein A.
Rubinstein A. ; Wolinsky A.
Savage L. J.
Schöler K.
Schubert R. ; Brown M. ; Gysler M. ; Brachinger H.  W.
Selten R.
Smith A.
Smith V.  L.
Smith V.  L.
Smith V.  L.
Sorensen A.
Stahl D.  O.
Stamato L.
Stearns S.  C.
Stigler G.  J.
Stigler G.  J.
Stiglitz J. E.
Sudman S. ; Blair E.
Teufel O.
Urban D. ; Mayerl J.
van  Baal S.
von  Neumann J. ; Morgenstern O.
Waldeck R.
Walters A. E. ; Stuhlmacher A. F. ; Meyer L. L.
Watson C.
"""


def master155(flat):
    raw = authors_raw(flat)
    assert raw == MASTER155.strip()


# TODO: UPDATE AFTER UPGRADE
BACHELOR109 = """\
ADM Arbeitskreis Deutscher Markt ; und Sozialforschungsinstitute e.V.
Alby T.
Altaner F.
Arbeitsgemeinschaft Social Media e. V.
Back A. ; Heidecke F.
Bundesamt  für  Statistik.
Batinic B. ; Bosnjak M.
Becker M.
Becker M.
Belliger A. ; Krieger D.
Berekoven L. ; Eckert W. ; Ellenrieder P.
Berlecon Research GmbH.
BITKOM. (Hrsg.).
BITKOM. (Hrsg.).
Brahm T.
Bremer C.
Buchem I. ; Appelt R. ; Kaiser S. ; Schön S. ; Ebner M.
Buck C.
Buhse W.
Bundesverband  Digitale  Wirtschaft  (BVDW)  e.  V.
Crameri A.
Crameri A.
Deriu U.
Deutsche Gesellschaft für Personalführung e. V. (Hrsg.).
Disterer G.
Döring N.
Dzeyk W.
Ebner M. ; Schiefner M.
Ehle A.
E ; teaching.org.
Hähnel M.
Häntschel-Erhart I.
Happel H.-J. ; Romberg T.
Hawaiian Dictionaries.
Hettler U.
Hilzensauer W. ; Hornung-Prähauser V.
Hippner H.
Hisserich J. ; Primsch J.
Hofer M. ; Negri C.
Huang Y. ; Singh P.  V. ; Ghose A.
Huber F. ; Matthes I. ; Stenneken N.
Hug T. ; Poscheschnik G.
ICR  Institute  for  Competitive  Recruiting.
Jacobsmühlen T.  zur.
Kaplan A.  M. ; Haenlein M.
Kaplan A. M. ; Haenlein M.
Kempski I. von.
Kerres M.
Kerres M. ; Preussler A.
Kiefer B.-U.
Klobas J.  E.
Koch M. ; Richter A.
Koch M. ; Richter A.
Koch M. ; Richter A. ; Schlosser A.
Komus A. ; Wauch F.
Krämer M.
Latham L. ; Lundy J.
Lefrancois G.  R.
Lehner F.
Maier R. ; Schmidt A.
Manz F.
Mayer H.  O.
McAfee A.  P.
Mentzel W.
Metz B. ; Pfeiffer J. ; Staiger M. ; Wichert A.
Möller E.
Manouchehri  Far S.
Mudra P.
Müller C. ; Gronau N.
O'Reilly T.
O'Reilly T.
Pleil T.
Probst G. ; Raub S. ; Romhardt K.
Puhakainen P. ; Siponen M.
Raabe A.
Raab-Steiner E. ; Benesch M.
Reinhardt W. ; Ebner M. ; Beham G. ; Costa C.
Reinmann-Rothmeier G. ; Mandl H. ; Erlach C. ; Neubauer A.
Reips U.  D.
Rennstich J. K.
Richardson W.
Richter A.
Richter A. ; Koch M.
Robes J.
Röll M.
Sauer M.
Sauerer A. ; Müller C. M.
Sauter A.  M. ; Sauter W.
Simon N. ; Bernhardt N.
Spath D. (Hrsg.) ; Günther J.
Thielsch M.  T.
Thoeny P.
Tosh D. ; Werdmuller B.
Trost A.
Trost A. ; Jenewein T.
Uhss B.
Universität Zürich.
Wicht G.
""".strip()


def bachelor109(flat):
    raw = authors_raw(flat)
    assert raw == BACHELOR109


BACHELOR111 = """\
Bhebhe Leo
Dahlman Erik ; Parkvall Stefan ; Sköld Johan ; Beming Per
Friedel Prof. Dr. Ing Rainer ; Mahler Dipl.-Ing. Hans-Detlev
Friedel Prof. Dr. Ing Rainer ; Mahler Dipl.-Ing. Hans-Detlev
Frank Karlheinz
Freeman Roger L.
Gessler Ralf ; Krause Thomas
Günther Andreas
Huber Josef F.
Iftode Liviu ; Borcea Cristian ; Ravi Nishkam ; Kang Porlin ; Zhou Peng
KNX Association
Kriesel Werner ; Sokollik Frank ; Helm Peter
Lehner Franz
Lin Feida ; Yen Weiguo
Merz Hermann ; Hansemann Thomas ; Hübner Christof
Walke Bernhard
Walke Bernhard
Zheng Pei ; Ni Lionel M.
""".strip()


def bachelor111(flat):
    raw = authors_raw(flat)
    assert raw == BACHELOR111


def authors_raw(flat) -> str:
    items = [' ; '.join([item.raw for item in line.authors]) for line in flat]
    items = [item.strip() for item in items]
    raw = utila.NEWLINE.join(items)
    return raw


# yapf:disable
@pytest.mark.parametrize('source, pages, expected, validate', [
    pytest.param(power.ORDER107_PDF, '104:108', 31, order107, id='order107'), # VALIDATED BY HAND
    pytest.param(power.BACHELOR051_PDF, '42:46', 37, bachelor51, id='bachelor51'),
    pytest.param(power.BACHELOR056_PDF, '49:53', 32, bachelor56, id='bachelor56'), # VALIDATED BY HAND
    pytest.param(power.BACHELOR063_PDF, '59', 12, bachelor63, id='bachelor63', marks=pytest.mark.xfail(reason='improve name detector')),
    pytest.param(power.BACHELOR090_PDF, '84:89', 52, bachelor90, id='bachelor90'),
    pytest.param(power.BACHELOR109_PDF, '72:79', 98, bachelor109, id='bachelor109'),
    pytest.param(power.BACHELOR111_PDF, '85:87', 18, bachelor111, id='bachelor111'), # VALIDATED BY HAND
    pytest.param(power.BACHELOR128_PDF, '96:103', None, bachelor128, id='bachelor128'),
    pytest.param(power.MASTER075_PDF, '70', 18, master75, id='master75'), # VALIDATED BY HAND
    pytest.param(power.MASTER089_PDF, None, 149, master89, id='master89', marks=pytest.mark.xfail(reason='improve parser')),
    pytest.param(power.MASTER091B_PDF, '82:89', 85, master91b, id='master91b'), # VALIDATED BY HAND
    pytest.param(power.MASTER110_PDF, '104:109', 71, master110, id='master110'),
    pytest.param(power.MASTER116_PDF, '97,98,99,100', 46, master116, id='master116'), # VALIDATED BY HAND
    pytest.param(power.MASTER155_PDF, '75:85', 111, master155, id='master155'), # VALIDATED BY HAND 109
    pytest.param(power.DISS170_PDF, '150:163', None, diss170, id='diss170'),
    pytest.param(power.DISS266_PDF, '215:247', 427, None, id='diss266', marks=pytest.mark.xfail(reason='improve parser')), # VALIDATED BY HAND
    pytest.param(power.DISS272_PDF, '259:271', None, diss272, id='diss272'),
])
# yapf:enable
@utilatest.longrun
def test_detector_bibliography_run(
        source,
        pages,
        expected,
        validate,
        testdir,
        monkeypatch,
):
    source = power.link(source)
    cmd = f'-i {source} -o {testdir.tmpdir} --bibliography --pages={pages}'
    tests.run(cmd, monkeypatch=monkeypatch)

    outpath = detector.path.bibliography_detected(testdir.tmpdir)
    loaded = serializeraw.load_bibliography_reference(outpath)
    flat = utila.flatten(loaded)
    assert len(flat) == expected or expected is None, str(loaded)

    if validate:
        validate(flat)
