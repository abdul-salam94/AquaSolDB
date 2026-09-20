#!/usr/bin/env python
"""One version string, in every place this repository states one.

Seven places, two numbers that differ on purpose: a Python distribution carries three
components (1.0.0), a dataset release carries two (1.0). They are tied -- the dataset
version is the first two components of the package version -- so a bump in one place and
not the others is caught here rather than reaching a reader.

    aquasoldb/__init__.py   __version__       the package version
    pyproject.toml          version =         the same
    python -m aquasoldb     first line        the same, as the installed code prints it
    aquasoldb/__init__.py   DATASET_VERSION   the dataset version
    CITATION.cff            version:          the same
    CHANGELOG.md            newest ## v...    the same, with a leading v
    .zenodo.json            "version"         the same

The last one is the metadata the archive reads when a release is published, so a drift
there is the one drift nobody can correct afterwards: the DOI is already minted.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def one(pattern, text, what, where):
    hits = re.findall(pattern, text, re.MULTILINE)
    if not hits:
        print("VERSION: no %s found in %s" % (what, where))
        sys.exit(1)
    return hits


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


def main():
    init = read("aquasoldb", "__init__.py")
    package = one(r'^__version__ = "([^"]+)"', init, "__version__", "__init__.py")[0]
    dataset = one(r'^DATASET_VERSION = "([^"]+)"', init, "DATASET_VERSION",
                  "__init__.py")[0]
    pyproject = one(r'^version = "([^"]+)"', read("pyproject.toml"), "version",
                    "pyproject.toml")[0]
    cff = sorted(set(one(r'^\s*version: "([^"]+)"', read("CITATION.cff"), "version:",
                         "CITATION.cff")))
    changelog = one(r"^## (v\S+)", read("CHANGELOG.md"), "section heading",
                    "CHANGELOG.md")[0]
    deposit = json.loads(read(".zenodo.json"))
    if "version" not in deposit:
        print("VERSION: .zenodo.json states no version")
        sys.exit(1)
    zenodo = deposit["version"]
    env = dict(os.environ)
    env.setdefault("AQUASOLDB_ROOT", ROOT)
    # -B and the environment variable together: importing the reader must not leave a
    # __pycache__ folder behind in a published tree the manifest does not name.
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([sys.executable, "-B", "-m", "aquasoldb"], cwd=ROOT, env=env,
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print("VERSION: `python -m aquasoldb` failed: %s" % proc.stderr[-500:])
        return 1
    cli = one(r"^aquasoldb (\S+) reading ", proc.stdout, "printed version",
              "the command line")[0]

    problems = []
    if pyproject != package:
        problems.append("pyproject.toml says %s, __init__.py says %s"
                        % (pyproject, package))
    if cli != package:
        problems.append("`python -m aquasoldb` prints %s, __init__.py says %s"
                        % (cli, package))
    if dataset != ".".join(package.split(".")[:2]):
        problems.append("DATASET_VERSION %s is not the first two components of the "
                        "package version %s" % (dataset, package))
    if cff != [dataset]:
        problems.append("CITATION.cff states %s, the dataset version is %s"
                        % (cff, dataset))
    if changelog != "v" + dataset:
        problems.append("the newest CHANGELOG section is %s, expected v%s"
                        % (changelog, dataset))
    if zenodo != dataset:
        problems.append(".zenodo.json states %s, the dataset version is %s"
                        % (zenodo, dataset))
    for p in problems:
        print("VERSION:", p)
    print("7 places checked (package %s, dataset %s), %d problems"
          % (package, dataset, len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
