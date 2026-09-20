# -*- coding: utf-8 -*-
"""Find the shipped CSVs and read them into pandas with the dictionary's own dtypes.

Nothing here decides what a column means.  `csv/column_dictionary.csv` ships beside the
data and gives every column a unit; this module turns that unit into a dtype, so a column
added or retyped in a later release is read correctly without an edit here, and a column
the dictionary does not know is an error rather than a guess.

    unit                       dtype
    ------------------------   -----------------------------------------
    K, MPa, mol/kg water,      float64  -- an empty cell is NaN
      mol/mol
    rows                       Int64    -- an empty cell is <NA>
    -                          string   -- an empty cell is "", never NaN

Text columns are read with the CSV's own emptiness and NOTHING else: `keep_default_na` is
off for them, so a printed `NA`, `None` or `nan` stays the four characters the page
printed.  `value_as_printed` in particular is deliberately not numeric -- it holds decimal
commas, printed uncertainties, and the two labels ILLEGIBLE and NOT PRINTED.
"""
import hashlib
import os

import pandas as pd

#: Every family (CSV) in the release, in the order the README lists them.
TABLE_NAMES = ("solubility", "watercontent", "liquidwatercontent", "mixtures",
               "phaseboundaries", "sources")
#: The five that hold measurements; `sources` is the table of papers.
MEASUREMENT_TABLES = TABLE_NAMES[:5]

#: Set this to the folder that holds `csv/` to read a copy anywhere on disk.
AQUASOLDB_ROOT_ENV = "AQUASOLDB_ROOT"

DICTIONARY = "column_dictionary"
CHECKSUM_MANIFEST = os.path.join("provenance", "CHECKSUMS.sha256")

# The dictionary's unit vocabulary, mapped to how the column is read.  A unit outside this
# table stops the read: a new physical unit in a later release is a decision for a package
# release (R-DB3-13), not something to fall back on `object` for.
_UNIT_DTYPE = {"K": "float64",
               "MPa": "float64",
               "mol/kg water": "float64",
               "mol/mol": "float64",
               "rows": "Int64",
               "-": "string"}


def _family_path(root, family):
    return os.path.join(root, "csv", family + ".csv")


def _holds_the_data(path):
    """True when `path` is a folder with a csv/ holding every family of the release."""
    return all(os.path.isfile(_family_path(path, f)) for f in TABLE_NAMES + (DICTIONARY,))


def release_folder(root=None):
    """Resolve where the CSVs are, in the order: argument, environment, beside the package.

    The last of those is how the public repository works: `aquasoldb/` sits next to
    `csv/`, so an unpacked clone needs no configuration at all.  Inside the project
    repository that folder does not exist, and the caller must say which packaged copy it
    means -- an error naming both routes, never a silent read of the wrong release.
    """
    if root is not None:
        root = os.path.abspath(os.fspath(root))
        if not _holds_the_data(root):
            raise FileNotFoundError(
                "%s does not hold an AquaSolDB release: expected csv/<family>.csv for "
                "each of %s" % (root, ", ".join(TABLE_NAMES)))
        return root

    env = os.environ.get(AQUASOLDB_ROOT_ENV)
    if env:
        env = os.path.abspath(os.path.expanduser(env))
        if not _holds_the_data(env):
            raise FileNotFoundError(
                "%s is set to %s, which does not hold an AquaSolDB release (no "
                "csv/<family>.csv there)" % (AQUASOLDB_ROOT_ENV, env))
        return env

    here = os.path.dirname(os.path.abspath(__file__))
    candidate = here
    while True:
        if _holds_the_data(candidate):
            return candidate
        parent = os.path.dirname(candidate)
        if parent == candidate:
            break
        candidate = parent
    raise FileNotFoundError(
        "no AquaSolDB csv/ folder found next to the package (searched upwards from %s). "
        "Pass load(..., root=<folder holding csv/>) or set the %s environment variable."
        % (here, AQUASOLDB_ROOT_ENV))


def dtypes_from_dictionary(root=None):
    """`{family: {column: dtype}}`, read from the shipped column dictionary."""
    root = release_folder(root)
    dictionary = pd.read_csv(_family_path(root, DICTIONARY), dtype="string",
                             keep_default_na=False)
    out = {f: {} for f in TABLE_NAMES}
    for _i, row in dictionary.iterrows():
        unit = (row["unit"] or "").strip()
        if unit not in _UNIT_DTYPE:
            raise ValueError(
                "column_dictionary.csv gives column %r the unit %r, which this reader "
                "does not know how to type; the package version must follow the schema "
                "(R-DB3-13)." % (row["column"], unit))
        for family in (row["applies_to"] or "").split(","):
            family = family.strip()
            if not family:
                continue
            if family not in out:
                raise ValueError(
                    "column_dictionary.csv sends column %r to the unknown family %r"
                    % (row["column"], family))
            out[family][row["column"]] = _UNIT_DTYPE[unit]
    return out


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


def open_table(family, root=None, verify=False):
    """Read one family into a DataFrame, typed from the shipped column dictionary.

    `family` is one of `TABLE_NAMES`.  `root` overrides where the release is read from
    (see `release_folder`).  `verify=True` first re-hashes that file against the digest
    `provenance/CHECKSUMS.sha256` records -- off by default because it re-reads the file,
    and worth turning on once after a download.
    """
    if family not in TABLE_NAMES:
        raise ValueError("unknown family %r; AquaSolDB ships %s"
                         % (family, ", ".join(TABLE_NAMES)))
    root = release_folder(root)
    if verify:
        verify_checksums(root=root, names=["csv/%s.csv" % family])
    return _read(_family_path(root, family), dtypes_from_dictionary(root)[family])


def verify_checksums(root=None, names=None):
    """Re-hash the shipped data files against `provenance/CHECKSUMS.sha256`.

    Returns the list of package-relative names verified.  Raises on the first mismatch,
    on a missing file, and on a name the manifest does not carry: a release whose bytes
    have moved is not a release, and nothing here repairs a manifest.
    """
    root = release_folder(root)
    manifest = os.path.join(root, CHECKSUM_MANIFEST)
    if not os.path.isfile(manifest):
        raise FileNotFoundError("no checksum manifest at %s" % manifest)
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
    """`{family: rows}` for every family, read from the files themselves."""
    root = release_folder(root)
    dtypes = dtypes_from_dictionary(root)
    return {f: len(_read(_family_path(root, f), dtypes[f])) for f in TABLE_NAMES}
