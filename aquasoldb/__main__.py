# -*- coding: utf-8 -*-
"""`python -m aquasoldb` -- say which release is being read and how many rows it holds.

    python -m aquasoldb [ROOT]

ROOT is the folder holding `csv/`; without it the reader falls back to the AQUASOLDB_ROOT
environment variable and then to the folder beside the package.
"""
import sys

from . import __version__
from .tables import TABLE_NAMES, release_folder, row_counts


def print_counts(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    if len(argv) > 1:
        print("usage: python -m aquasoldb [ROOT]", file=sys.stderr)
        return 2
    root = argv[0] if argv else None
    try:
        where = release_folder(root)
        counts = row_counts(where)
    except (FileNotFoundError, ValueError) as exc:
        print("aquasoldb: %s" % exc, file=sys.stderr)
        return 1
    print("aquasoldb %s reading %s" % (__version__, where))
    for family in TABLE_NAMES:
        print("  %-20s %8d rows" % (family, counts[family]))
    print("  %-20s %8d rows"
          % ("(measurements)", sum(counts[f] for f in TABLE_NAMES if f != "sources")))
    return 0


if __name__ == "__main__":
    sys.exit(print_counts())
