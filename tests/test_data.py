# -*- coding: utf-8 -*-
"""The DATA's own rules, re-checked in a downloader's clone.

`test_package.py` beside this file tests the READER.  This file tests the RELEASE: it
opens the shipped CSVs with the standard library and asks whether they still obey the
rules the release states about itself -- the schema, the vocabularies, the ion rule, the
row-for-row detail, the plausibility bands.  Every one of those rules is enforced by the
build that wrote the files; the point of running them again here is that a clone is the
only place a reader can check, and a file edited by hand after publication is the one
thing that must never go unnoticed.

Nothing is restated.  The vocabularies, the tolerance, the forbidden cell values, the row
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
from aquasoldb.subset import FLAG_VOCABULARY, PURE_WATER

csv.field_size_limit(10 ** 7)

MEASUREMENT_FILES = ("csv/solubility.csv", "csv/water_content.csv", "csv/mixtures.csv",
                     "csv/phase_boundaries.csv", "csv/other_quantities.csv")
SOURCES = "csv/sources.csv"
DICTIONARY = "csv/column_dictionary.csv"
PRINTED_VALUES = "detail/printed_values.csv"
EXCLUDED_SOURCES = "detail/excluded_sources.csv"
ID_CHANGES = "detail/id_changes.csv"
ALL_FILES = MEASUREMENT_FILES + (SOURCES, DICTIONARY, PRINTED_VALUES, EXCLUDED_SOURCES,
                                 ID_CHANGES)

RULE_HEADING = "## Machine-readable rule constants"
RULE_FENCE = "```"
DROPPED_ZERO = re.compile(r"Dropped as always zero: ([A-Za-z0-9_, ]+)\.")

#: Keys the block must carry.  A block that lost one is a release this file cannot check,
#: which is a failure and never a silent skip.
REQUIRED_RULE_KEYS = (
    "flags", "method", "source_type", "ion_columns", "ion_charge_balance_tolerance",
    "value_labels", "forbidden_cell_values", "published_rows", "screened_rows",
    "audited_rows",
)

#: Words that would make a column a statement about somebody's model fit rather than about
#: the measurement: no column name of the release may carry one (matched as whole parts of
#: the name between underscores).
MODEL_ROLE_WORDS = {"fit", "fitted", "fitting", "tier", "regression", "route", "holdout",
                    "training", "validation"}

#: Floor on the number of published rows, so a reader that silently returns nothing
#: cannot turn every test below into a pass over an empty set.
PUBLISHED_ROW_FLOOR = 1000
DICTIONARY_ROW_FLOOR = 20


# --------------------------------------------------------------------- fixtures
def _read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader.fieldnames or []), list(reader)


def _stem(name):
    return name.rsplit("/", 1)[1][:-len(".csv")]


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
    """The shipped column dictionary: [(table, column, meaning), ...] in file order."""
    header, rows = _read(os.path.join(root, *DICTIONARY.split("/")))
    assert header[:2] == ["table", "column"], header
    assert len(rows) >= DICTIONARY_ROW_FLOOR, (
        "the column dictionary holds %d rows, floor %d" % (len(rows), DICTIONARY_ROW_FLOOR))
    return [(r["table"], r["column"], r["meaning"]) for r in rows]


@pytest.fixture(scope="session")
def shipped(root):
    """{"csv/<name>.csv" or "detail/<name>.csv": (header list, [row dict])}."""
    out = {name: _read(os.path.join(root, *name.split("/"))) for name in ALL_FILES}
    published = sum(len(out[name][1]) for name in MEASUREMENT_FILES)
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
    column in the dictionary and not in its file is a promise the release does not keep.
    Both folders, csv/ and detail/, and in the file's own order."""
    for name in ALL_FILES:
        header, _rows = shipped[name]
        declared = [column for table, column, _m in dictionary if table == _stem(name)]
        assert header == declared, (
            "%s and the column dictionary disagree: %s"
            % (name, sorted(set(header) ^ set(declared)) or "order"))
        assert len(header) == len(set(header)), "%s repeats a column name" % name
    files = {_stem(n) for n in ALL_FILES}
    assert {table for table, _c, _m in dictionary} == files


def test_no_column_anywhere_names_a_role_in_a_model_fit(shipped, dictionary):
    """Whether a row was used in somebody's model fit is a property of the fit, and no
    column of this database encodes it."""
    named = set()
    for name in ALL_FILES:
        named |= {c.strip().lower() for c in shipped[name][0]}
    named |= {column.strip().lower() for _t, column, _m in dictionary}
    offenders = sorted(c for c in named if set(c.split("_")) & MODEL_ROLE_WORDS)
    assert not offenders, "model-role columns in the published schema: %s" % offenders


# ------------------------------------------------------------- the vocabularies
def test_every_flag_on_every_row_is_in_the_published_flag_vocabulary(shipped, rules):
    vocabulary = set(rules["flags"])
    assert vocabulary == set(FLAG_VOCABULARY), (
        "the release's flags and the reader's FLAG_VOCABULARY disagree: %s"
        % sorted(vocabulary ^ set(FLAG_VOCABULARY)))
    seen = Counter()
    for name in MEASUREMENT_FILES:
        for row in shipped[name][1]:
            for flag in (row.get("flags") or "").split(";"):
                if flag.strip():
                    seen[flag.strip()] += 1
    assert seen, "not one flag was read out of the release; the parser has gone blind"
    outside = sorted(set(seen) - vocabulary)
    assert not outside, "flags outside the published vocabulary: %s" % outside


def test_every_method_value_is_in_the_published_method_vocabulary(shipped, rules):
    vocabulary = set(rules["method"])
    seen = Counter(row.get("method", "") for name in MEASUREMENT_FILES + (SOURCES,)
                   for row in shipped[name][1])
    assert seen, "no method values read"
    blank = seen.pop("", 0)
    assert not blank, "%d published rows carry no method value" % blank
    outside = sorted(set(seen) - vocabulary)
    assert not outside, "method values outside the published vocabulary: %s" % outside


def test_every_source_carries_exactly_one_source_type_word(shipped, rules):
    """One word per source, out of the six the release publishes."""
    vocabulary = set(rules["source_type"])
    assert len(vocabulary) == 6, sorted(vocabulary)
    _header, rows = shipped[SOURCES]
    seen = Counter((r.get("source_type") or "").strip() for r in rows)
    assert not seen.pop("", 0), "sources with an empty source_type"
    outside = sorted(set(seen) - vocabulary)
    assert not outside, "source_type values outside the published vocabulary: %s" % outside


def test_a_doi_is_a_bare_doi_and_every_source_is_cited(shipped):
    """The release carries no network test -- these tests must run in a clone with no
    internet -- so what is checked is the SHAPE of the locator: a DOI cell is the bare
    `10.<registrant>/<suffix>`, never a web address, and every source has a reference."""
    _header, rows = shipped[SOURCES]
    pattern = re.compile(r"^10\.\d{4,9}/\S+$")
    malformed = [(r["source_id"], r["doi"]) for r in rows
                 if (r.get("doi") or "").strip() and not pattern.match(r["doi"])]
    assert not malformed, "doi cells that are not bare DOIs: %s" % malformed[:5]
    uncited = [r["source_id"] for r in rows if not (r.get("reference") or "").strip()]
    assert not uncited, "sources with no reference: %s" % uncited[:5]
    assert len({r["source_id"] for r in rows}) == len(rows), "a source_id repeats"


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
    for name in ALL_FILES:
        header, rows = shipped[name]
        for row in rows:
            for column in header:
                if (row.get(column) or "").strip() in forbidden:
                    hits.append((name, column, row.get(column)))
    assert not hits, "%d sentinel or placeholder cells: %s" % (len(hits), hits[:5])


def test_every_number_lies_inside_the_band_the_release_publishes_for_it(shipped, rules):
    """The bands are plausibility, not precision: wide enough that no published row sits
    near an edge, narrow enough that a unit slip lands outside. A red here is a value to
    investigate against the printed page, never a band to widen."""
    bands = {key.split(" ", 1)[1]: (float(v[0]), float(v[1]))
             for key, v in rules.items() if key.startswith("range ") and len(v) == 2}
    assert len(bands) >= 6, sorted(bands)
    checked, offenders = 0, []
    for name in MEASUREMENT_FILES:
        header, rows = shipped[name]
        for column, (low, high) in sorted(bands.items()):
            if column not in header:
                continue
            for row in rows:
                cell = (row.get(column) or "").strip()
                if not cell:
                    continue
                value = _number(cell)
                if value is None:
                    offenders.append((name, row["point_id"], column, cell, "not a number"))
                    continue
                checked += 1
                if not (low <= value <= high):
                    offenders.append((name, row["point_id"], column, cell,
                                      "outside %g..%g" % (low, high)))
    assert checked >= PUBLISHED_ROW_FLOOR, (
        "only %d numbers were checked against a band; the columns have been renamed and "
        "this test is looking at nothing" % checked)
    assert not offenders, "%d values outside their band: %s" % (len(offenders),
                                                                offenders[:5])


# ------------------------------------------------------------------- the ions
def test_the_ion_columns_ship_whole_or_blank_and_balance_charge(shipped, rules, dictionary):
    """Three rules in one: a measurement file carries each of the six ion columns or the
    dictionary declares it dropped as always zero; a row fills all of its file's ion
    columns or none; and a filled row balances charge inside the published tolerance,
    a dropped column counting as zero. The tolerance is read from the release, and is a
    ceiling."""
    ions = rules["ion_columns"]
    assert len(ions) == 6, ions
    assert set(ions) == set(ION_CHARGE_NUMBER), (
        "the release's ion columns and the reader's charge table disagree: %s"
        % sorted(set(ions) ^ set(ION_CHARGE_NUMBER)))
    tolerance = float(rules["ion_charge_balance_tolerance"][0])
    assert tolerance > 0
    partial, unbalanced, filled, undeclared = [], [], 0, []
    for name in MEASUREMENT_FILES:
        header, rows = shipped[name]
        dropped = set()
        for table, _column, meaning in dictionary:
            if table == _stem(name):
                for listed in DROPPED_ZERO.findall(meaning):
                    dropped |= {c.strip() for c in listed.split(",") if c.strip()}
        present = [c for c in ions if c in header]
        undeclared += [(name, c) for c in ions if c not in header and c not in dropped]
        for row in rows:
            cells = [(row.get(c) or "").strip() for c in present]
            given = [c for c in cells if c]
            if not given:
                continue
            if len(given) != len(present):
                partial.append((name, row["point_id"]))
                continue
            filled += 1
            values = [_number(c) for c in cells]
            if any(v is None for v in values):
                unbalanced.append((name, row["point_id"], "non-numeric ion cell"))
                continue
            residual = sum(v * ION_CHARGE_NUMBER[c] for c, v in zip(present, values))
            if abs(residual) > tolerance:
                unbalanced.append((name, row["point_id"], residual))
    assert not undeclared, ("ion columns missing from a file without the dictionary "
                            "declaring them dropped as always zero: %s" % undeclared)
    assert filled >= PUBLISHED_ROW_FLOOR, (
        "only %d rows carry a filled ion composition; the columns have been renamed and "
        "the charge balance is being checked on nothing" % filled)
    assert not partial, "%d rows carry some but not all ion columns: %s" % (len(partial),
                                                                            partial[:5])
    assert not unbalanced, ("%d filled rows miss charge balance by more than %g: %s"
                            % (len(unbalanced), tolerance, unbalanced[:5]))
    # A pure-water row never carries a non-zero ion.
    salty_water = [(name, row["point_id"]) for name in MEASUREMENT_FILES
                   for row in shipped[name][1] if row.get("salt") == PURE_WATER
                   and any(_number(row.get(c)) for c in ions if (row.get(c) or "").strip())]
    assert not salty_water, salty_water[:5]


# -------------------------------------------------------------- the detail files
def test_one_printed_values_row_per_published_row_and_one_published_row_per_printed_row(
        shipped):
    """The release's traceability promise: every published row has its value, unit and
    page as printed in detail/printed_values.csv, and that file names no row this release
    does not publish."""
    _header, printed = shipped[PRINTED_VALUES]
    assert printed, "detail/printed_values.csv is empty"
    published = Counter()
    for name in MEASUREMENT_FILES:
        published.update(r["point_id"] for r in shipped[name][1])
    twice = sorted(k for k, n in published.items() if n > 1)
    assert not twice, "point_ids published twice: %s" % twice[:5]
    listed = Counter(r["point_id"] for r in printed)
    repeated = sorted(k for k, n in listed.items() if n > 1)
    assert not repeated, "printed_values names %d point_ids twice: %s" % (len(repeated),
                                                                          repeated[:5])
    assert set(listed) == set(published), sorted(set(listed) ^ set(published))[:10]


def test_the_published_and_left_out_rows_account_for_every_audited_row(shipped, rules):
    """detail/excluded_sources.csv counts the audited rows this release does NOT publish,
    by source and reason. Published plus left out must be the audited total the release
    states -- a number that comes from the compilation's own records, not from adding
    these files together."""
    _header, excluded = shipped[EXCLUDED_SOURCES]
    assert excluded, "detail/excluded_sources.csv is empty"
    reasonless = [r for r in excluded if not (r.get("reason") or "").strip()]
    assert not reasonless, "%d excluded-source rows carry no reason" % len(reasonless)
    left_out = sum(int(r["rows_left_out"]) for r in excluded)
    published = sum(len(shipped[name][1]) for name in MEASUREMENT_FILES)
    stated_published = int(rules["published_rows"][0])
    stated_screened = int(rules["screened_rows"][0])
    audited = int(rules["audited_rows"][0])
    assert published == stated_published, (
        "the CSVs hold %d rows, the release states %d" % (published, stated_published))
    assert left_out == stated_screened, (
        "the excluded sources leave out %d rows, the release states %d"
        % (left_out, stated_screened))
    assert published + left_out == audited, (
        "%d published + %d left out = %d, but the release states %d audited rows"
        % (published, left_out, published + left_out, audited))


def test_every_replicate_flag_sits_on_both_rows_of_an_identical_pair(shipped, rules):
    """`replicate` means the paper prints this measurement more than once and BOTH rows
    are kept.  So the flag is never true of a row on its own: a flagged row must have at
    least one other row identical to it -- the same in every published column but
    `point_id` (the flag included), and the same value, unit and page as printed.  Drop
    the flag from one member of a pair and this goes red, which is what makes it a check.

    Deliberately ONE-DIRECTIONAL: two rows of one paper can print the same digits without
    being the same measurement, so "every identical pair is flagged" is not asserted.
    """
    assert "replicate" in set(rules["flags"]), rules["flags"]
    printed_header, printed_rows = shipped[PRINTED_VALUES]
    printed = {r["point_id"]: tuple(r[c] for c in printed_header if c != "point_id")
               for r in printed_rows}
    lonely, flagged = [], 0
    for name in MEASUREMENT_FILES:
        header, rows = shipped[name]
        key_columns = [c for c in header if c != "point_id"]
        grouped = defaultdict(list)
        for row in rows:
            key = tuple(row.get(c) or "" for c in key_columns) + printed[row["point_id"]]
            grouped[key].append(row)
        for members in grouped.values():
            if not any("replicate" in (m.get("flags") or "") for m in members):
                continue
            flagged += len(members)
            if len(members) < 2:
                lonely.append((name, members[0]["point_id"]))
    assert flagged, ("no row in this release carries the `replicate` flag, so this test "
                     "checked nothing; the flag was in the vocabulary when it was written")
    assert not lonely, ("%d rows are flagged `replicate` and have no identical twin: %s"
                        % (len(lonely), lonely[:5]))
