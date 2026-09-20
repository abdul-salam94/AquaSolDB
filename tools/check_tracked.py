#!/usr/bin/env python
"""Every file in this repository is named in SHA256SUMS.txt, and nothing else is.

Both directions, because they are different failures:

  * a file on disk with no manifest entry is a file nobody checksummed -- it could have
    been added by hand after the release was built, and `sha256sum -c` would not notice;
  * a manifest entry with no file is a file that was deleted after the build, which makes
    the published tree a different thing from the one the DOI describes.

Reported separately for csv/ and provenance/, which are the data, and for the rest of the
repository.  Standard library only: this runs in the public repository, which holds the
files and nothing else.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MANIFEST = "SHA256SUMS.txt"
DATA_DIRS = ("csv", "provenance")
# Not part of the published tree: version-control internals and Python bytecode, neither
# of which a release ships.  The manifest never names them, so the walk must not either.
SKIP_DIRS = (".git", "__pycache__", ".pytest_cache")
SKIP_SUFFIXES = (".pyc",)


def manifest_entries():
    path = os.path.join(ROOT, MANIFEST)
    if not os.path.isfile(path):
        print("MISSING: %s -- the release has no manifest" % MANIFEST)
        sys.exit(1)
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            digest, rel = line.split("  ", 1)
            out[rel] = digest
    return out


def on_disk():
    found = []
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for n in sorted(names):
            rel = os.path.relpath(os.path.join(base, n), ROOT).replace("\\", "/")
            if rel == MANIFEST or rel.endswith(SKIP_SUFFIXES):
                continue
            found.append(rel)
    return sorted(found)


def main():
    entries = manifest_entries()
    # Everything, the workflow included: the manifest covers the whole tree, so the two
    # sides must match exactly rather than by an exception list.
    disk = on_disk()
    problems = []
    for rel in disk:
        if rel not in entries:
            problems.append("on disk, absent from %s: %s" % (MANIFEST, rel))
    for rel in sorted(entries):
        if not os.path.isfile(os.path.join(ROOT, rel)):
            problems.append("named in %s, not on disk: %s" % (MANIFEST, rel))
    data_files = [rel for rel in disk
                  if rel.split("/")[0] in DATA_DIRS]
    if not data_files:
        problems.append("no files found under %s -- the walk has gone blind"
                        % "/, ".join(DATA_DIRS))
    for p in problems:
        print("UNTRACKED:", p)
    print("%d files on disk, %d manifest entries, %d of them data files, %d problems"
          % (len(disk), len(entries), len(data_files), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
