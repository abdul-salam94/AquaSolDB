# -*- coding: utf-8 -*-
"""The DATA's own rules, re-checked in a downloader's clone (R-DB3-18).

`test_package.py` beside this file tests the READER.  This file tests the RELEASE: it
opens the shipped CSVs with the standard library and asks whether they still obey the
rules the release states about itself -- the schema, the vocabularies, the ion rule, the
row-for-row provenance, the plausibility bands.  Every one of those rules is enforced by
the build that wrote the files; the point of running them again here is that a clone is
the only place a reader can check, and a file edited by hand after publication is the one
thing that must never go unnoticed.

Nothing is restated.  The vocabularies, the tolerance, the forbidden markers, the row
totals and the bands are READ out of the shipped `SCHEMA.md` block titled "Machine-readable
rule constants", and the per-file schema is read out of the shipped
`csv/column_dictionary.csv`.  So a rule cannot be changed in the build and left standing
here, or the other way round: there is only one copy, and it travels with the data.

The fixtures refuse to run on an unparseable release rather than passing over it: a rule
block that lost a key, or a table that read as empty, fails immediately with its own
message.  A test that cannot fail is not a test.
"""
import csv
import os
import re
from collections import Counter, defaultdict

import pytest

from aquasoldb.brine import ION_CHARGE_NUMBER

csv.field_size_limit(10 ** 7)

MEASUREMENT_FILES = ("solubility", "watercontent", "liquidwatercontent",
                     "mixtures", "phaseboundaries")
ALL_FILES = MEASUREMENT_FILES + ("sources",)
CROSSWALK = ("provenance", "row_crosswalk.csv")
SCREENED = ("provenance", "screened_rows.csv")

RULE_HEADING = "## Machine-readable rule constants"
RULE_FENCE = "```"

#: Keys the block must carry.  A block that lost one is a release this file cannot check,
#: which is a failure and never a silent skip.
REQUIRED_RULE_KEYS = (
    "flags", "method", "method_extra", "source_type", "ion_columns",
    "ion_charge_balance_tolerance", "value_labels", "forbidden_cell_values",
    "forbidden_columns", "published_rows", "screened_rows", "audited_rows",
)

#: Floor on the number of published rows, so a reader that silently returns nothing
#: cannot turn every test below into a pass over an empty set.
PUBLISHED_ROW_FLOOR = 1000
DICTIONARY_ROW_FLOOR = 20


# --------------------------------------------------------------------- fixtures
def _read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader.fieldnames or []), list(reader)


@pytest.fixture(scope="session")
def rules(root):
    """The rule block of the shipped SCHEMA.md, as {key: [value, ...]}."""
    with open(os.path.join(root, "SCHEMA.md"), encoding="utf-8") as fh:
        text = fh.read()
    assert RULE_HEADING in text, (
        "the shipped SCHEMA.md carries no %r section, so this release states no rules "
        "for its own data and nothing below can be checked" % RULE_HEADING)
    body = text.split(RULE_HEADING, 1)[1].split(RULE_FENCE)
    assert len(body) >= 3, "the rule block in SCHEMA.md is not fenced"
    out = {}
    for line in body[1].strip().splitlines():
        key, sep, value = line.partition(":")
        assert sep, "unparseable rule line: %r" % line
        out[key.strip()] = [v.strip() for v in value.split(",") if v.strip()]
    missing = [k for k in REQUIRED_RULE_KEYS if k not in out]
    assert not missing, (
        "the rule block is missing %s -- the parser or the block has changed and these "
        "tests would silently check less than they claim" % ", ".join(missing))
    assert any(k.startswith("range ") for k in out), "the rule block states no bands"
    return out


@pytest.fixture(scope="session")
def dictionary(root):
    """The shipped column dictionary: [(column, applies_to set), ...]."""
    _header, rows = _read(os.path.join(root, "csv", "column_dictionary.csv"))
    assert len(rows) >= DICTIONARY_ROW_FLOOR, (
        "the column dictionary holds %d rows, floor %d" % (len(rows), DICTIONARY_ROW_FLOOR))
    return [(r["column"], {p.strip() for p in r["applies_to"].split(",") if p.strip()})
            for r in rows]


@pytest.fixture(scope="session")
def shipped(root):
    """{stem: (header list, [row dict])} for the six shipped CSVs."""
    out = {}
    for stem in ALL_FILES:
        out[stem] = _read(os.path.join(root, "csv", stem + ".csv"))
    published = sum(len(rows) for stem, (_h, rows) in out.items()
                    if stem in MEASUREMENT_FILES)
    assert published >= PUBLISHED_ROW_FLOOR, (
        "read %d published rows, floor %d -- the reader has gone blind and every check "
        "below would pass over nothing" % (published, PUBLISHED_ROW_FLOOR))
    return out


def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------------ the schema
def test_every_csv_header_is_exactly_the_columns_the_dictionary_gives_it(
        shipped, dictionary):
    """A column in a file and not in the dictionary is a column with no meaning; a
    column in the dictionary and not in its file is a promise the release does not keep."""
    for stem in ALL_FILES:
        header, _rows = shipped[stem]
        declared = {name for name, applies in dictionary if stem in applies}
        assert set(header) == declared, (
            "csv/%s.csv and the column dictionary disagree: %s"
            % (stem, sorted(set(header) ^ declared)))
        assert len(header) == len(set(header)), "csv/%s.csv repeats a column name" % stem


def test_no_column_anywhere_names_a_fit_tier_or_a_fit_role(shipped, dictionary, rules):
    """R-DB3-3, fit neutrality: whether a row was used in somebody's model fit is a
    property of the fit, and no column of this database encodes it."""
    forbidden = {w.lower() for w in rules["forbidden_columns"]}
    assert forbidden, "the rule block names no forbidden columns"
    named = set()
    for stem in ALL_FILES:
        named |= {c.strip().lower() for c in shipped[stem][0]}
    named |= {name.strip().lower() for name, _ in dictionary}
    offenders = sorted(named & forbidden)
    assert not offenders, "fit-role or tier columns in the published schema: %s" % offenders


# ------------------------------------------------------------- the vocabularies
def test_every_flag_on_every_row_is_in_the_published_flag_vocabulary(shipped, rules):
    vocabulary = set(rules["flags"])
    assert len(vocabulary) >= 3, vocabulary
    seen = Counter()
    for stem in MEASUREMENT_FILES:
        for row in shipped[stem][1]:
            for flag in (row.get("flags") or "").split(";"):
                if flag.strip():
                    seen[flag.strip()] += 1
    assert seen, "not one flag was read out of the release; the parser has gone blind"
    outside = sorted(set(seen) - vocabulary)
    assert not outside, "flags outside the published vocabulary: %s" % outside


def test_every_method_value_is_in_the_published_method_vocabulary(shipped, rules):
    vocabulary = set(rules["method"]) | set(rules["method_extra"])
    seen = Counter(row.get("method", "") for stem in MEASUREMENT_FILES
                   for row in shipped[stem][1])
    assert seen, "no method values read"
    blank = seen.pop("", 0)
    assert not blank, "%d published rows carry no method value" % blank
    outside = sorted(set(seen) - vocabulary)
    assert not outside, "method values outside the published vocabulary: %s" % outside


def test_every_source_carries_exactly_one_source_type_word(shipped, rules):
    """R-DB3-19(a): one word per source, out of the six the release publishes."""
    vocabulary = set(rules["source_type"])
    assert len(vocabulary) == 6, sorted(vocabulary)
    _header, rows = shipped["sources"]
    seen = Counter((r.get("source_type") or "").strip() for r in rows)
    assert not seen.pop("", 0), "sources with an empty source_type"
    outside = sorted(set(seen) - vocabulary)
    assert not outside, "source_type values outside the published vocabulary: %s" % outside


def test_a_url_is_a_well_formed_https_record_and_never_sits_beside_a_doi(shipped):
    """R-DB3-19(a).  The release carries no network test -- these tests must run in a
    clone with no internet -- so what is checked is the SHAPE of the locator and the rule
    that a source with a DOI has no second locator to keep in step with it."""
    _header, rows = shipped["sources"]
    pattern = re.compile(r"^https://[^\s\"'<>]+\.[^\s\"'<>]+$")
    malformed, doubled = [], []
    for r in rows:
        url = (r.get("url") or "").strip()
        doi = (r.get("doi") or "").strip()
        if url and not pattern.match(url):
            malformed.append((r["source_id"], url))
        if url and doi:
            doubled.append(r["source_id"])
    assert not malformed, "urls that are not well-formed https locators: %s" % malformed
    assert not doubled, "sources carrying both a doi and a url: %s" % doubled


# ---------------------------------------------------------------- the cells
def test_no_cell_in_any_shipped_csv_is_a_sentinel_or_a_placeholder(shipped, rules):
    """A missing value is an EMPTY CELL. Never `-999`, never `NA`, never `TBD`.

    Matched on the whole stripped cell and case-sensitively, which is the rule the
    release states: `none` in lower case is the `salt` value for pure water, while `NONE`
    in a data cell is a stand-in for a value nobody filled in.
    """
    forbidden = set(rules["forbidden_cell_values"])
    assert len(forbidden) >= 10, sorted(forbidden)
    hits = []
    for stem in ALL_FILES:
        header, rows = shipped[stem]
        for row in rows:
            for column in header:
                if (row.get(column) or "").strip() in forbidden:
                    hits.append((stem, column, row.get(column)))
    assert not hits, "%d sentinel or placeholder cells: %s" % (len(hits), hits[:5])


def test_every_number_lies_inside_the_band_the_release_publishes_for_it(shipped, rules):
    """The bands are plausibility, not precision: wide enough that no published row sits
    near an edge, narrow enough that a unit slip lands outside. A red here is a value to
    investigate against the printed page, never a band to widen."""
    bands = {key.split(" ", 1)[1]: (float(v[0]), float(v[1]))
             for key, v in rules.items() if key.startswith("range ") and len(v) == 2}
    assert len(bands) >= 6, sorted(bands)
    checked, offenders = 0, []
    for stem in MEASUREMENT_FILES:
        header, rows = shipped[stem]
        for column, (low, high) in sorted(bands.items()):
            if column not in header:
                continue
            for row in rows:
                cell = (row.get(column) or "").strip()
                if not cell:
                    continue
                value = _number(cell)
                if value is None:
                    offenders.append((stem, row["point_id"], column, cell, "not a number"))
                    continue
                checked += 1
                if not (low <= value <= high):
                    offenders.append((stem, row["point_id"], column, cell,
                                      "outside %g..%g" % (low, high)))
    assert checked >= PUBLISHED_ROW_FLOOR, (
        "only %d numbers were checked against a band; the columns have been renamed and "
        "this test is looking at nothing" % checked)
    assert not offenders, "%d values outside their band: %s" % (len(offenders),
                                                                offenders[:5])


# ------------------------------------------------------------------- the ions
def test_the_six_ion_columns_ship_whole_or_blank_and_balance_charge(shipped, rules):
    """R-DB3-3. Three rules in one: the six columns are in every measurement file; a row
    fills all six or none; and a filled row balances charge inside the published
    tolerance. The tolerance is read from the release, and is a ceiling."""
    ions = rules["ion_columns"]
    assert len(ions) == 6, ions
    assert set(ions) == set(ION_CHARGE_NUMBER), (
        "the release's ion columns and the reader's charge table disagree: %s"
        % sorted(set(ions) ^ set(ION_CHARGE_NUMBER)))
    tolerance = float(rules["ion_charge_balance_tolerance"][0])
    assert tolerance > 0
    partial, unbalanced, filled = [], [], 0
    for stem in MEASUREMENT_FILES:
        header, rows = shipped[stem]
        missing = [c for c in ions if c not in header]
        assert not missing, "csv/%s.csv is missing ion columns %s" % (stem, missing)
        for row in rows:
            cells = [(row.get(c) or "").strip() for c in ions]
            given = [c for c in cells if c]
            if not given:
                continue
            if len(given) != len(ions):
                partial.append((stem, row["point_id"]))
                continue
            filled += 1
            values = [_number(c) for c in cells]
            if any(v is None for v in values):
                unbalanced.append((stem, row["point_id"], "non-numeric ion cell"))
                continue
            residual = sum(v * ION_CHARGE_NUMBER[c] for c, v in zip(ions, values))
            if abs(residual) > tolerance:
                unbalanced.append((stem, row["point_id"], residual))
    assert filled >= PUBLISHED_ROW_FLOOR, (
        "only %d rows carry a filled ion composition; the columns have been renamed and "
        "the charge balance is being checked on nothing" % filled)
    assert not partial, "%d rows carry some but not all six ions: %s" % (len(partial),
                                                                         partial[:5])
    assert not unbalanced, ("%d filled rows miss charge balance by more than %g: %s"
                            % (len(unbalanced), tolerance, unbalanced[:5]))


# -------------------------------------------------------------- the provenance
def test_one_crosswalk_row_per_published_row_and_one_published_row_per_crosswalk_row(
        root, shipped):
    """The release's core traceability promise: every published row names the internal
    record behind it, and the crosswalk names no row this release does not publish."""
    _header, cross = _read(os.path.join(root, *CROSSWALK))
    assert cross, "provenance/row_crosswalk.csv is empty"
    published = set()
    for stem in MEASUREMENT_FILES:
        published |= {r["point_id"] for r in shipped[stem][1]}
    listed = Counter(r["public_point_id"] for r in cross)
    repeated = sorted(k for k, n in listed.items() if n > 1)
    assert not repeated, "crosswalk names %d point_ids twice: %s" % (len(repeated),
                                                                     repeated[:5])
    assert len(cross) == len(published), (
        "%d crosswalk rows for %d published rows" % (len(cross), len(published)))
    assert set(listed) == published, sorted(set(listed) ^ published)[:10]


def test_the_published_and_screened_rows_account_for_every_audited_row(
        root, shipped, rules):
    """The screened list is the other half of the crosswalk: the audited rows this
    release does NOT publish, each with its reason. Published plus screened must be the
    audited total the release states -- a number that comes from the compilation's own
    records, not from adding these two files together."""
    _header, screened = _read(os.path.join(root, *SCREENED))
    assert screened, "provenance/screened_rows.csv is empty"
    reasonless = [r for r in screened if not (r.get("reason") or "").strip()]
    assert not reasonless, "%d screened rows carry no reason" % len(reasonless)
    published = sum(len(shipped[stem][1]) for stem in MEASUREMENT_FILES)
    stated_published = int(rules["published_rows"][0])
    stated_screened = int(rules["screened_rows"][0])
    audited = int(rules["audited_rows"][0])
    assert published == stated_published, (
        "the CSVs hold %d rows, the release states %d" % (published, stated_published))
    assert len(screened) == stated_screened, (
        "the screened list holds %d rows, the release states %d"
        % (len(screened), stated_screened))
    assert published + len(screened) == audited, (
        "%d published + %d screened = %d, but the release states %d audited rows"
        % (published, len(screened), published + len(screened), audited))


def test_every_replicate_flag_sits_on_both_rows_of_a_byte_identical_pair(shipped, rules):
    """`replicate` means the paper prints this measurement more than once and BOTH rows
    are kept.  So the flag is never true of a row on its own: a flagged row must have at
    least one other row byte-identical to it -- the same in every published column but
    `point_id`, the flag included.  Drop the flag from one member of a pair and this goes
    red, which is what makes it a check.

    Deliberately ONE-DIRECTIONAL, and the reason is worth stating because the converse
    looks tempting.  Two rows of one paper can print the same digits without being the
    same measurement: this release holds 214 groups of rows identical but for `point_id`
    and only 34 of them are printed replicates.  `replicate` is a statement about the
    record behind the row, and a published row that merely coincides with a pair is not
    one, so "every identical pair is flagged" is FALSE here and is not asserted.
    """
    assert "replicate" in set(rules["flags"]), rules["flags"]
    lonely, flagged = [], 0
    for stem in MEASUREMENT_FILES:
        header, rows = shipped[stem]
        if not rows:
            continue
        key_columns = [c for c in header if c != "point_id"]
        grouped = defaultdict(list)
        for row in rows:
            grouped[tuple(row.get(c) or "" for c in key_columns)].append(row)
        for members in grouped.values():
            if not any("replicate" in (m.get("flags") or "") for m in members):
                continue
            flagged += len(members)
            if len(members) < 2:
                lonely.append((stem, members[0]["point_id"]))
    assert flagged, ("no row in this release carries the `replicate` flag, so this test "
                     "checked nothing; the flag was in the vocabulary when it was written")
    assert not lonely, ("%d rows are flagged `replicate` and have no identical twin: %s"
                        % (len(lonely), lonely[:5]))
