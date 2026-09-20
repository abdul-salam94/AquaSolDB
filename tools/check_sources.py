#!/usr/bin/env python
"""Every source in csv/sources.csv resolves, or is a blank this release already had.

Three things a reader can check without leaving this repository:

  * the citation string is a citation, not an empty cell or a leftover marker;
  * a DOI, where one is given, is shaped like a DOI;
  * the number of sources with no DOI at all does not exceed 111, the number this
    release was packaged with. That ceiling is written here by the packaging script from
    the table beside it; it may fall between releases and must never be raised by hand.

Some older papers -- 19th-century volumes, Soviet-era reports, university theses -- have
no DOI to give, which is why the ceiling is a number and not zero. The project repository
records the reason for each one on the tracker row the citation comes from.
"""
import csv
import os
import re
import sys

csv.field_size_limit(10 ** 7)
HERE = os.path.dirname(os.path.abspath(__file__))
TABLE = os.path.join(os.path.dirname(HERE), "csv", "sources.csv")

BLANK_DOI_CEILING = 111
MIN_CITATION_CHARS = 12
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/\S+$")
PLACEHOLDER_PATTERNS = (r"\bTBD\b", r"\bTO-RESOLVE\b", r"\bTODO\b", r"\bXXX\b",
                        r"\bFIXME\b", r"\bplaceholder\b", r"\bcitation pending\b",
                        r"\?\?\?")


def main():
    with open(TABLE, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    problems = []
    blank = 0
    for r in rows:
        sid = r["source_id"]
        ref = (r.get("reference") or "").strip()
        doi = (r.get("doi") or "").strip()
        if len(ref) < MIN_CITATION_CHARS:
            problems.append("%s: citation is empty or too short to be one: %r"
                            % (sid, ref))
        for pat in PLACEHOLDER_PATTERNS:
            m = re.search(pat, ref, re.IGNORECASE)
            if m:
                problems.append("%s: citation carries the placeholder %r"
                                % (sid, m.group(0)))
                break
        if doi and not DOI_PATTERN.match(doi):
            problems.append("%s: %r is not a DOI" % (sid, doi))
        if not doi:
            blank += 1
    if not rows:
        problems.append("csv/sources.csv holds no rows -- the reader has gone blind")
    if blank > BLANK_DOI_CEILING:
        problems.append("%d sources ship a blank doi, ceiling %d -- fill the identifier, "
                        "never raise the ceiling" % (blank, BLANK_DOI_CEILING))
    for p in problems:
        print("SOURCE:", p)
    print("%d sources checked, %d with a blank doi (ceiling %d), %d problems"
          % (len(rows), blank, BLANK_DOI_CEILING, len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
