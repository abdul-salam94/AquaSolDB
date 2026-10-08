#!/usr/bin/env python
"""Recount the rows of every data file and compare with SCHEMA.md and csv/sources.csv.

Three things a reader can check without leaving this repository:

  * every CSV in csv/ and detail/ holds exactly the row count SCHEMA.md states for it,
    and SCHEMA.md states a count for every one of them;
  * every source that a measurement row names has an entry in csv/sources.csv;
  * every entry in csv/sources.csv is named by at least one measurement row.

Stand-alone on purpose: this runs inside the public repository, which holds the CSVs and
nothing else, so it depends on the standard library only.
"""
import csv
import os
import re
import sys

csv.field_size_limit(10 ** 7)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIRS = ("csv", "detail")
MEASUREMENT_FILES = ("solubility", "water_content", "mixtures", "phase_boundaries",
                     "other_quantities")
STATED = re.compile(r"^## `([a-z]+/[a-z_]+[.]csv)` +[(]([0-9]+) rows[)]$", re.MULTILINE)


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    with open(os.path.join(ROOT, "SCHEMA.md"), encoding="utf-8") as fh:
        stated = {rel: int(n) for rel, n in STATED.findall(fh.read())}
    problems = []
    on_disk = sorted("%s/%s" % (folder, n) for folder in DATA_DIRS
                     if os.path.isdir(os.path.join(ROOT, folder))
                     for n in os.listdir(os.path.join(ROOT, folder)) if n.endswith(".csv"))
    if not on_disk:
        problems.append("no CSV found under %s/ -- the check has gone blind"
                        % "/, ".join(DATA_DIRS))
    held = {}
    for rel in on_disk:
        held[rel] = rows(os.path.join(ROOT, *rel.split("/")))
        if rel not in stated:
            problems.append("%s: SCHEMA.md states no row count for it" % rel)
        elif len(held[rel]) != stated[rel]:
            problems.append("%s holds %d rows, SCHEMA.md states %d"
                            % (rel, len(held[rel]), stated[rel]))
    for rel in sorted(set(stated) - set(held)):
        problems.append("%s: SCHEMA.md states %d rows, the file is not here"
                        % (rel, stated[rel]))
    named = set()
    for stem in MEASUREMENT_FILES:
        rel = "csv/%s.csv" % stem
        if rel not in held:
            problems.append("%s: measurement file missing" % rel)
            continue
        named.update(r["source_id"] for r in held[rel])
    listed = set(r["source_id"] for r in held.get("csv/sources.csv", []))
    for sid in sorted(named - listed):
        problems.append("%s has rows and no entry in csv/sources.csv" % sid)
    for sid in sorted(listed - named):
        problems.append("%s is in csv/sources.csv and no measurement row names it" % sid)
    for p in problems:
        print("STALE:", p)
    print("%d data files and %d sources checked, %d problems"
          % (len(held), len(listed), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
