# Changelog

Every noteable change is logged here.

## v0.40.0 (2022-12-21)

### Feature

* use modern data approach (1fdf8d61f712)

### Chore

* remove default behavior (7fea4932237b)
* extend resource generator (858649cd637a)
* use quick install (124d9b3ff2a3)
* upgrade requirements.txt (a7eee54357e8)
* upgrade pipeline (3ab9178ae163)

## v0.39.3 (2022-10-16)

### Chore

* do not lock resources (bc699c39490d)
* publish resources if all fails (c3d17708a2a0)
* add pipe library (63c3bfecd7cf)
* convert nightly to all (77408ac9ffaf)
* upgrade requirements.txt (ee6e737d2fd6)
* upgrade baw (a1e566bc0473)
* do not run in privileged mode (49477a5f25fe)

## v0.39.2 (2022-10-02)

### Chore

* adjust worker count (a07efec0b3a9)

## v0.39.1 (2022-10-02)

### Fix

* skip step if ghost is not installed (8e6bcd8135ca)

### Chore

* upgrade requirements.txt (f6fb70db0cbf)

## v0.39.0 (2022-09-28)

### Feature

* shrink year parser (c26f28749c3d)

### Documentation

* extend interface documentation (b5042a7f3263)

### Chore

* use image with opengl (a9e1d3985907)
* add generator step (6b98bc1fe496)
* do not use too many worker (0ad4a4da55aa)
* increase worker count on ci (a58ea2751907)
* remove default value (0ed8ee4ccd14)
* add missing test data generator (8b72d1333b1f)
* add Jenkinsfile (30f6b92d698c)
* upgrade requirements.txt (f071889cca20)
* upgrade requirements.txt (c9d3e9eed695)

## v0.38.0

### Feature

* add another pattern (68883547cab9)
* make parser more robust (21cd3608e811)
* extend person after parser (cf73609386e8)
* extend prof person parser (c8f1e7d71a37)
* profile persons parser (6e43363b263a)

### Fix

* fix raw replace (e27e603b1c06)
* shrink regex runtime (abc4482de7dc)
* reduce regex runtime (0215b026f2fe)

### Documentation

* add another format (f4b7bf7bef96)

## v0.37.0

## v0.36.0

### Feature

* extend bib parser (6ca9538b48b6)
* add strategy name to bib result (e1912a9c124b)
* extend person pattern (3dd06c68bf02)

### Fix

* adjust page number for non zero page start (f623a1aef5dd)

## v0.35.1

### Feature

* increase colors to pass book173 example (580ab9dd6d5c)

### Fix

* do not fail on too few colors (c9e5e2c25432)

## v0.35.0

### Feature

* use real holy values (44dd22d6e9d6)
* improve speed due using PIL native methods (74ed3932fb45)
* use generator approach to reduce amount of memory (7e31f4ba7144)

### Fix

* convert year to int (efacd378e47c)
* convert empty string to none (fbed351868c6)

## v0.34.1

### Fix

* rename cli to avoid conflict with windows color option (d3ccb5d5989e)

## v0.34.0

### Feature

* add index detector (66b1c4d5d015)

## v0.33.0

### Feature

* add method to load extracted colors (c56d8a98b014)
* add statistics runner (f5f8c4f0c4bd)
* add method to determine histogram (c58bcce5c896)
* add method to detect colors of a pdf page (a6f8faaea23b)
* add pdf color detector (6b4154cf2e7f)

## v0.32.0

### Feature

* add headline and pages to BibliographyTable (76407fc49b2e)
* use bib table (3abc311a8678)

## v0.31.0

### Feature

* add optional white space to academic title patter (a908de8cb7ff)
* make regex more robust (8773daa50aad)
* add improved title detector (1874c1fb2125)
* strip title (5e631fe4e29e)
* use complex pattern to support more cases (3e7b2f9f6237)
* use date as first split also (5fde58773027)
* move strong http pattern to the front (39eb77424bc6)
* detect year inside brackets at bib start (66c96e1b7b50)
* use improved regex splitter (49ee68b70647)
* shrink possible year (89dc2404b4a1)
* do not create ghost pattern (dc1ae19db274)

### Fix

* ensure that person parser runs fast enough (f334eb28cdd8)
* set min name length to 3 (c0c8c45f2339)
* adjust image selector (bd8429c0f6ea)
* improve magic parser (d832268778ae)
* skip empty selection (451c6f21041d)

## v0.30.0

### Feature

* use regex to improve institution parser (07d82331920e)
* improve text preparation (206f652e4a5a)
* use improved institution parser (c559f1901e73)
* use picture to convert text in images to normal text (b3e6229cf153)
* skip very long possible authors (b329bcc78325)
* split quote before colon if possible (6fb8dcbab017)
* add strategy with database lookup (c3b1627fca02)
* allow space inside doc type def (cce66b2aa490)
* do not skip bibs with detected reference (47e5787c8c73)
* increase debugging information (990596e88949)

### Fix

* do not create ghost pattern (4617f57bd576)
* allow more than one institution (61e3bdd73fcb)
* avoid regex attack (1060ac95d248)

### Documentation

* adjust modules path (6aa86459cdd7)
* Happy New Year! (f1780600dae6)

## v0.29.3

### Feature

* split optional number at the front of the line (dccc12079198)
* allow splitting number-dot-pattern at front (041424b5d6af)

## v0.29.2

### Fix

* skip empty left column (1fe41c3792ce)

## v0.29.1

### Feature

* do not strip bracket angles (000178ff3be1)

## v0.29.0

### Feature

* disable column verification after improving results (15017c6430a7)
* improve column detector (87f3f26b5487)
* extend bib evaluation (5c4c84c14546)
* add improved bib detector (84858c318e5f)
* add improved bib parser (deacdde753fd)
* disable debugging (38a0a07eb225)
* using caching to reduce execution time (862b5eabaa52)

### Fix

* adjust after changing interface (d6d8dd679297)

## v0.28.2

### Feature

* replace with holy values (8b8859f2fca1)

## v0.28.1

### Fix

* do not parse author if no quotation mark is collected (c7698cf61667)

## v0.28.0

### Feature

* extend after pattern (34a4f5cd145f)
* add title validator (d432fc4fe569)
* add BSC as academic title (9ee2b0e8f7a8)
* add brackets to title parser (7f15a676de38)
* add persons title extractor (dc3adb305d6f)

### Fix

* reduce number of false positive detection (a5742c7f91e0)
* replace with stars (b69f068457b3)
* fix after academic title determiner (e7dcecc900a6)

## v0.27.1

### Fix

* adjust data type (23dbf09d7a55)

## v0.27.0

### Feature

* add ebd person parser (369994c88cfb)

## v0.26.0

### Feature

* improve title page parser (33cf7f5542a4)
* add more potential person intros (c046d47a550b)
* add option white space in academic title (d2ddef3bad37)

### Fix

* improve person after parser (03ecdef2c5d8)

## v0.25.0

### Feature

* extend person start pattern (f2e4ec8191f6)
* detect more than the first result (f30e053fcc2f)
* add line start and end limit (0e1abdd4effe)
* add student prefix (222d6de401af)
* improve persons parser (20aeb20dfee2)

## v0.24.0

### Feature

* replace and/und with separator (60f7cbc5eb4a)
* improve bib number parser (503626232939)
* merge multiple NoPerson's (a5f563f33841)
* add quotes extractor (b953d8f20967)
* add strategy to search authors (afca0e44b67b)
* reduce verbosity (2ed6f93b4c14)

### Fix

* do not hand `and` in authors as separator (190f423762c2)

## v0.23.0

### Feature

* improve bib parser (d63423d5144e)
* store more than one hyperlink (205002d55514)

### Fix

* do not split inside links (93575c5a1b0e)

## v0.22.0

### Feature

* make parser more optimistic (604327de2833)
* skip results with too many year errors (cc78489746c0)
* skip invalid results (dbecfb06f21a)
* use global vspace strategy (a70f20f8bccc)
* make parser less strict (dbb5b062f94f)
* improve year and hyperlink selector (2c18b8ff4aab)
* adjust freeand parser (a8590259fcd6)
* improve freeand parser (2a2eb57345c0)
* add referent as potential examiner (d55ea3cc441b)
* extend person title after parser (0374a736a793)
* make person decider more robust (cb4f8d69b159)

### Fix

* adjust freeand parser (fc2e805d2631)
* include more sentence signs (d4dffdb24f4d)
* add szett as valid character (21681f8dc062)

### Documentation

* add information about very bad example (ae9e222f24f6)
* add module documentation (2adbf32daec9)

## v0.21.1

### Feature

* ignore cases and ease using regex (edd51d837fd3)
* extend semester pattern (3e5ebb0d1082)

## v0.21.0

### Feature

* use more specific parser first (07d9cadf2e76)
* extend debugging information (8fde94d652a2)
* use improved newline converter (493aa5e60392)
* improve freeand parser (078e3e112a74)
* normalize white spaces to ease regex (c336e846872b)
* add optional extern flag (b6e9b7052355)
* add master title to title after person pattern (ce983854fd1c)
* add optional month part (fafe3d64057a)
* add location of parsed bib to result (afc4bb841ad8)

### Fix

* support character simplification (a355a8dd66a4)

## v0.20.0

### Feature

* add rest parser to solve order107 (10f6972cce35)
* change order in bib detection strategy (bfdb921f9e46)
* return None to signal invalid input (9a47360f90ae)
* use less strict bib pattern (327ac04ff8b3)
* add option to parse multiple bib pattern (3e2a2a84682c)
* add option change used regex (08e4af79d63b)
* add noperson bib parser (c93e5ad672e3)

## v0.19.0

### Feature

* decrease verbosity (2504fa00eaff)

## v0.18.0

### Feature

* decrease verbosity of logging (5fddb4ffaffe)
* count valid bibs only (bd8199ad88ab)
* extend bib pattern support (7754bb3a22ea)
* increase vspace max variation range (99919476a5bc)

## v0.17.0

### Feature

* skip none parsings in alternate layout (d9c1a50b3d30)
* use magic parser in alternate layout (62d1e8657938)
* add very less accurate `magic` parser (dc39c6b8efd1)
* use layout optimize to gather better results (0ae30b3cfef0)
* increase maximum label char width (b86fdb779417)
* add method to skip invalid parsed academic titles (76af10785b41)
* spread pattern over more than one line (090212b4b46f)

## v0.16.1

### Fix

* add missing import (974ac3fb71f8)

## v0.16.0

### Feature

* add new [1]-pattern parser to alternate parser (d3106301929a)
* add numbered reference[1]-parser (ee7d4af13b6b)

## v0.15.0

### Feature

* extend title page parser and judger (7730a9e84017)
* extend person pattern (3b8d0f9beeae)
* simplify titlepage extractor loader (9686d9cef10c)

## v0.14.0

### Feature

* add double column optimizer (873a1fee2133)
* enable second bib column detector strategy (490a0bfd6c44)
* add special double column parser (4043d9776e0c)

## v0.13.3

### Fix

* adjust unit test to new Person data structure (1683395a5ca6)

## v0.13.2

### Feature

* improve tech parser (01309da842f6)

### Fix

* remove year fragment (fe101ea42b8f)

### Documentation

* extend interface documentation (7a48fd533472)

## v0.13.0

### Feature

* add numbers pattern to tech parser (e62c6d34acaf)
* add number label detection pattern (77e5782ffb36)

### Fix

* add simple year to extend more bib pattern (4227a1a8c715)

### Documentation

* Happy New Year! (99053cd20e90)

## v0.12.2

### Feature

* add page follows to tech label parser (bfb9bedd5e6e)
* add page shortcut to tech label parser (e4e8b79bec48)

## v0.12.0

### Feature

* convert parsed author to higher abstraction (510cc69a9802)

## v0.11.3

### Feature

* extend tech label parser (c79d03740926)
* use improved authors parser (c1a7ab591114)
* remove more than one link out of rest content (fa9ac97d70e9)
* convert short year to ac (0a6a893a599d)

### Fix

* skip empty publisher (0b6ba927a902)

### Documentation

* extend documentation (b3dfcdb85505)
* extend documentation (f91733f566d0)

## v0.11.2

### Feature

* add author comma pattern (f287b2441bcf)
* use number of parser authors to tie equal successful pattern (f8ffe6f8510e)
* disable too much negative bib results (97cea61e1c29)

### Fix

* handle border of invalid parsing correctly (c7cf60c620d3)
* do not handle empty title as invalid title (fb4c05819e9a)
* reduce min length of valid author (187823023706)
* detect fewer false positive freeand bib (51b17cfb6796)

## v0.11.0

### Feature

* extend reference parser (4eb3cbbf2992)
* extend link pattern parser (6a1978527e62)
* extend bib decider strategy (b28b477560b3)
* add vspace strategy (7b19870b811f)
* improve parser due using page text content (00d837112533)

## v0.10.0

### Feature

* extend person parser (10b6eab19ca5)
* extend examiner parser (672b95e61306)
* extend institution parser (2d7b79a3c40f)
* extend matrikel parser (e653e29a882b)
* convert raw formula to formula (92f81a76bcd7)
* add method to determine path to extracted formula (829e5da6e0a6)

## v0.9.0

### Feature

* extend person parser (ea0d2a04d5bd)

## v0.8.3

### Fix

* fix link to package description (2427db197684)

## v0.8.0

### Feature

* add extracted title pdf page to titlepage (bfa0b0d00b89)

### Documentation

* fix outdated interface documentation (98b97e29e4a6)

## v0.7.0

### Feature

* add error level checker to skip male extractions (ea72e4cc3c07)

### Fix

* disable default parser cause of to many fault parsing (5254d84e6921)

## v0.6.0

### Feature

* extend university list (bc33db0e90b0)

## v0.5.1

### Fix

* add missing import (28f100496a73)

## v0.5.0

### Feature

* add formula extraction step (f35628da7c73)

## v0.4.1

### Fix

* fix selecting required resources (80ca66136674)

## v0.4.0

### Feature

* change default behavior for bib grouping (5a58ded93a5b)

## v0.3.0

### Feature

* ensure to have connected pages input for bib parsing (ae427807c7be)

### Fix

* fix theissen sort - support `no year` sorting (2265a88b1fa5)

## v0.2.1

### Fix

* add missing import (c7da366db6f6)

## v0.2.0

### Feature

* add further accessed pattern (4b1f22d7dfeb)
* add zero day pattern to accessed parser (e9e5e0c0f367)
* extend accessed parser (95b54cd3643b)
* parse obvious items first (a1de6c379ae8)
* add without date pattern (30d86ae4d992)
* add accessed time parser (2bcc164a326f)
* add hyperlink parser (19aa9c28f9f6)
* extend pages parser (1fa4463ef546)

### Fix

* store correct raw content (fa9c34c177eb)

## v0.1.0

### Feature

* move code from hey project v2.9.0 (65b006884343)

## v0.0.0 Initial release
