# -*- coding: utf-8 -*-
"""Find the shipped CSVs and read them into pandas with the dictionary's own dtypes.

Nothing here decides what a column means.  `csv/column_dictionary.csv` ships beside the
data and gives every column of every file a unit (one row per file and column: `table`,
`column`, `unit`, `meaning`, `blank_means`); this module turns that unit into a dtype, so a
column added or retyped in a later release is read correctly without an edit here, and a
column the dictionary does not know is an error rather than a guess.

    unit                       dtype
    ------------------------   -----------------------------------------
    K, MPa, mol/kg water,      float64  -- an empty cell is NaN
      mol/mol
    rows                       Int64    -- an empty cell is <NA>
    -                          string   -- an empty cell is "", never NaN

Text columns are read with the CSV's own emptiness and NOTHING else: `keep_default_na` is
off for them, so a printed `NA`, `None` or `nan` stays the characters the page printed.
`value_as_printed` in `detail/printed_values.csv` in particular is deliberately not
numeric -- it holds decimal commas, printed uncertainties, and the labels ILLEGIBLE and
NOT PRINTED.

The release has two folders: `csv/` holds the five measurement files, the sources and the
column dictionary (`open_table`); `detail/` holds the printed values, the sources left out
and the id changes (`open_detail`).
"""
import hashlib
import os
import re

import pandas as pd

#: Every file under csv/ a reader opens with `open_table`, in the order the README lists
#: them.
TABLE_NAMES = ("solubility", "water_content", "mixtures", "phase_boundaries",
               "other_quantities", "sources")
#: The five that hold measurement rows; `sources` is the table of papers.
MEASUREMENT_TABLES = TABLE_NAMES[:5]
#: Every file under detail/, opened with `open_detail`.
DETAIL_NAMES = ("printed_values", "excluded_sources", "id_changes")

#: Set this to the folder that holds `csv/` and `detail/` to read a copy anywhere on disk.
AQUASOLDB_ROOT_ENV = "AQUASOLDB_ROOT"

DICTIONARY = "column_dictionary"
#: The digest lists a release may carry, the first one present is used: the data-file list
#: and the whole-release list.
CHECKSUM_MANIFESTS = (os.path.join("provenance", "CHECKSUMS.sha256"), "SHA256SUMS.txt")

# The dictionary's unit vocabulary, mapped to how the column is read.  A unit outside this
# table stops the read: a new physical unit in a later release is a decision for a package
# release, not something to fall back on `object` for.
_UNIT_DTYPE = {"K": "float64",
               "MPa": "float64",
               "mol/kg water": "float64",
               "mol/mol": "float64",
               "rows": "Int64",
               "-": "string"}
_DICTIONARY_COLUMNS = ("table", "column", "unit", "meaning", "blank_means")
# The sentence the dictionary writes into a file's rows when the file leaves out an ion
# column that was zero on every row with a known composition.
_DROPPED_ZERO = re.compile(r"Dropped as always zero: ([A-Za-z0-9_, ]+)\.")

# Keys `open_table` and `open_detail` set in `DataFrame.attrs`, so the helpers that take
# only a frame know which file and which release it came from.
ATTR_TABLE = "aquasoldb_table"
ATTR_ROOT = "aquasoldb_root"
ATTR_DROPPED_ZERO = "aquasoldb_dropped_as_zero"


def _relname(name):
    """`csv/<name>.csv` or `detail/<name>.csv`, as the checksum lists write it."""
    return "%s/%s.csv" % ("detail" if name in DETAIL_NAMES else "csv", name)


def _path(root, name):
    return os.path.join(root, *_relname(name).split("/"))


def _holds_the_data(path):
    """True when `path` is a folder with csv/ and detail/ holding every file of the release."""
    return all(os.path.isfile(_path(path, n))
               for n in TABLE_NAMES + (DICTIONARY,) + DETAIL_NAMES)


def _expected_files():
    return ", ".join(_relname(n) for n in TABLE_NAMES + (DICTIONARY,) + DETAIL_NAMES)


def _beside_the_package():
    """The first folder at or above the package that holds a release, or None."""
    candidate = os.path.dirname(os.path.abspath(__file__))
    while True:
        if _holds_the_data(candidate):
            return candidate
        parent = os.path.dirname(candidate)
        if parent == candidate:
            return None
        candidate = parent


def release_folder(root=None):
    """Resolve where the release is, in the order: argument, environment, beside the
    package, then a copy `download()` already saved in the cache.  No step goes online.

    The third of those is how the public repository works: `aquasoldb/` sits next to
    `csv/`, so an unpacked clone needs no configuration at all.  A folder named by the
    argument or the environment variable that is not a release is an error naming it,
    never a silent read of another copy.
    """
    if root is not None:
        root = os.path.abspath(os.fspath(root))
        if not _holds_the_data(root):
            raise FileNotFoundError(
                "%s does not hold an AquaSolDB release: expected %s"
                % (root, _expected_files()))
        return root

    env = os.environ.get(AQUASOLDB_ROOT_ENV)
    if env:
        env = os.path.abspath(os.path.expanduser(env))
        if not _holds_the_data(env):
            raise FileNotFoundError(
                "%s is set to %s, which does not hold an AquaSolDB release (expected %s)"
                % (AQUASOLDB_ROOT_ENV, env, _expected_files()))
        return env

    beside = _beside_the_package()
    if beside is not None:
        return beside

    from .remote import cached_release
    cached = cached_release()
    if cached is not None:
        return cached
    raise FileNotFoundError(
        "no AquaSolDB release found: none beside the package (searched upwards from %s) "
        "and none in the download cache. Pass root=<folder holding csv/ and detail/>, set "
        "the %s environment variable, or fetch a copy once with aquasoldb.download()."
        % (os.path.dirname(os.path.abspath(__file__)), AQUASOLDB_ROOT_ENV))


def _dictionary(root):
    dictionary = pd.read_csv(_path(root, DICTIONARY), dtype="string",
                             keep_default_na=False)
    if tuple(dictionary.columns) != _DICTIONARY_COLUMNS:
        raise ValueError(
            "column_dictionary.csv has the columns %s; this reader reads %s"
            % (", ".join(dictionary.columns), ", ".join(_DICTIONARY_COLUMNS)))
    return dictionary


def dtypes_from_dictionary(root=None):
    """`{file: {column: dtype}}` for every file of the release, read from the shipped
    column dictionary."""
    root = release_folder(root)
    known = TABLE_NAMES + (DICTIONARY,) + DETAIL_NAMES
    out = {n: {} for n in known}
    for _i, row in _dictionary(root).iterrows():
        table = (row["table"] or "").strip()
        unit = (row["unit"] or "").strip()
        if table not in out:
            raise ValueError("column_dictionary.csv describes column %r of the unknown file "
                             "%r" % (row["column"], table))
        if unit not in _UNIT_DTYPE:
            raise ValueError(
                "column_dictionary.csv gives column %r of %s the unit %r, which this reader "
                "does not know how to type; the package version must follow the release's "
                "schema." % (row["column"], table, unit))
        out[table][row["column"]] = _UNIT_DTYPE[unit]
    return out


def _dropped_as_zero(root, table):
    """The ion columns the dictionary says `table` left out as zero on every row with a
    known composition."""
    dropped = []
    rows = _dictionary(root)
    for meaning in rows.loc[rows["table"] == table, "meaning"]:
        for listed in _DROPPED_ZERO.findall(meaning or ""):
            dropped += [c.strip() for c in listed.split(",") if c.strip()]
    return tuple(dict.fromkeys(dropped))


def _read(path, dtypes):
    header = pd.read_csv(path, nrows=0).columns.tolist()
    unknown = [c for c in header if c not in dtypes]
    if unknown:
        raise ValueError(
            "%s carries columns the shipped column dictionary does not describe: %s"
            % (os.path.basename(path), ", ".join(unknown)))
    use = {c: dtypes[c] for c in header}
    # Emptiness, and only emptiness, is missing: `na_values` is set per column so that a
    # text cell reading "NA" or "None" survives as text, and a numeric cell that is blank
    # becomes NaN.
    na_values = {c: [""] for c, d in use.items() if d != "string"}
    return pd.read_csv(path, dtype=use, keep_default_na=False, na_values=na_values)


def _open(name, root, verify):
    root = release_folder(root)
    if verify:
        verify_checksums(root=root, names=[_relname(name)])
    df = _read(_path(root, name), dtypes_from_dictionary(root)[name])
    df.attrs[ATTR_TABLE] = name
    df.attrs[ATTR_ROOT] = root
    df.attrs[ATTR_DROPPED_ZERO] = _dropped_as_zero(root, name)
    return df


def open_table(name, root=None, verify=False):
    """Read one file of csv/ into a DataFrame, typed from the shipped column dictionary.

    `name` is one of `TABLE_NAMES`.  `root` overrides where the release is read from
    (see `release_folder`).  `verify=True` first re-hashes that file against the digest
    the release's checksum list records -- off by default because it re-reads the file,
    and worth turning on once after copying a release by hand.
    """
    if name not in TABLE_NAMES:
        raise ValueError("unknown table %r; csv/ holds %s%s"
                         % (name, ", ".join(TABLE_NAMES),
                            " (open %r with open_detail)" % name
                            if name in DETAIL_NAMES else ""))
    return _open(name, root, verify)


def open_detail(name):
    """Read one file of detail/ (`DETAIL_NAMES`) from the release `release_folder()` finds.

    printed_values    the value, unit and page as the source printed them, one row per
                      measurement row, joined on `point_id`
    excluded_sources  the sources whose rows are left out, with the count and the reason
    id_changes        every earlier id that no longer ships under the same id, and why
    """
    if name not in DETAIL_NAMES:
        raise ValueError("unknown detail file %r; detail/ holds %s%s"
                         % (name, ", ".join(DETAIL_NAMES),
                            " (open %r with open_table)" % name
                            if name in TABLE_NAMES else ""))
    return _open(name, None, False)


def with_citation(df):
    """A copy of `df` with the `reference` and `doi` of each row's source added, joined on
    `source_id` from csv/sources.csv of the release the frame was read from.

    Row order and index are kept.  A `source_id` the sources table does not list is an
    error naming it, never a row left without its citation.
    """
    if "source_id" not in df.columns:
        raise KeyError("this table has no 'source_id' column, so its rows cannot be joined "
                       "to their sources")
    clash = [c for c in ("reference", "doi") if c in df.columns]
    if clash:
        raise ValueError("this table already has %s; with_citation adds them from "
                         "csv/sources.csv" % ", ".join(clash))
    sources = open_table("sources", root=df.attrs.get(ATTR_ROOT))
    listed = set(sources["source_id"])
    unknown = sorted(set(df["source_id"]) - listed)
    if unknown:
        raise KeyError("source_id not in csv/sources.csv: %s" % ", ".join(unknown[:10]))
    out = df.join(sources.set_index("source_id")[["reference", "doi"]], on="source_id")
    out.attrs = dict(df.attrs)
    return out


def verify_checksums(root=None, names=None):
    """Re-hash the shipped files against the release's checksum list.

    The list is `provenance/CHECKSUMS.sha256`, or `SHA256SUMS.txt` where the release ships
    only that.  Returns the list of release-relative names verified.  Raises on the first
    mismatch, on a missing file, and on a name the list does not carry: a release whose
    bytes have moved is not a release, and nothing here repairs a checksum list.
    """
    root = release_folder(root)
    manifest = next((os.path.join(root, m) for m in CHECKSUM_MANIFESTS
                     if os.path.isfile(os.path.join(root, m))), None)
    if manifest is None:
        raise FileNotFoundError("no checksum list (%s) in %s"
                                % (" or ".join(CHECKSUM_MANIFESTS), root))
    pinned = {}
    with open(manifest, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            digest, name = line.split("  ", 1)
            pinned[name] = digest
    wanted = sorted(pinned) if names is None else list(names)
    missing = [n for n in wanted if n not in pinned]
    if missing:
        raise KeyError("%s names no digest for: %s" % (manifest, ", ".join(missing)))
    for name in wanted:
        path = os.path.join(root, *name.split("/"))
        if not os.path.isfile(path):
            raise FileNotFoundError("%s is named in %s and is not here" % (name, manifest))
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for block in iter(lambda: fh.read(1 << 20), b""):
                h.update(block)
        if h.hexdigest() != pinned[name]:
            raise ValueError(
                "%s does not match the digest the release recorded: expected %s, got %s. "
                "The file has been edited or the download is incomplete."
                % (name, pinned[name], h.hexdigest()))
    return wanted


def row_counts(root=None):
    """`{table: rows}` for every file of csv/ in `TABLE_NAMES`, read from the files."""
    root = release_folder(root)
    dtypes = dtypes_from_dictionary(root)
    return {n: len(_read(_path(root, n), dtypes[n])) for n in TABLE_NAMES}
