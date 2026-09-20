#!/usr/bin/env python
"""Recount the per-file rows each source contributes and compare with sources.csv.

Stand-alone on purpose: this runs inside the public repository, which holds the CSVs and
nothing else, so it depends on the standard library only. The same check runs inside the
project repository as `build_aquasoldb.py --check`, which additionally re-hashes the files
against the digests the build recorded.
"""
import csv
import os
import sys
from collections import Counter, defaultdict

csv.field_size_limit(10 ** 7)
HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(os.path.dirname(HERE), "csv")
FILES = [("solubility", "n_solubility"), ("watercontent", "n_watercontent"),
         ("liquidwatercontent", "n_liquidwatercontent"), ("mixtures", "n_mixtures"),
         ("phaseboundaries", "n_phaseboundaries")]


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    counts = defaultdict(Counter)
    for stem, col in FILES:
        for r in rows(os.path.join(CSV, stem + ".csv")):
            counts[r["source_id"]][col] += 1
    problems = []
    listed = set()
    for r in rows(os.path.join(CSV, "sources.csv")):
        sid = r["source_id"]
        listed.add(sid)
        for _stem, col in FILES:
            if int(r[col] or 0) != counts[sid][col]:
                problems.append("%s: %s says %s, the CSVs hold %d"
                                % (sid, col, r[col], counts[sid][col]))
    for sid in sorted(set(counts) - listed):
        problems.append("%s has rows and no entry in sources.csv" % sid)
    for p in problems:
        print("STALE:", p)
    print("%d sources checked, %d problems" % (len(listed), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
