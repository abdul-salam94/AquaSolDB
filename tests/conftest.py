# -*- coding: utf-8 -*-
"""Shared fixtures: which release is under test, and its tables, read once.

Every test here runs against SHIPPED FILES -- the CSVs of a packaged release, found the
same way a downloader's code finds them (`AQUASOLDB_ROOT`, or the folder beside the
package).  Nothing is generated for the tests to read.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aquasoldb  # noqa: E402


@pytest.fixture(scope="session")
def root():
    return aquasoldb.release_folder()


@pytest.fixture(scope="session")
def tables(root):
    """`{family: DataFrame}` for all six tables, read once for the whole session."""
    return {family: aquasoldb.open_table(family, root=root)
            for family in aquasoldb.TABLE_NAMES}


@pytest.fixture(scope="session")
def measurements(tables):
    """`{family: DataFrame}` for the five measurement tables only."""
    return {f: tables[f] for f in aquasoldb.MEASUREMENT_TABLES}


@pytest.fixture(scope="session")
def solubility(tables):
    return tables["solubility"]
