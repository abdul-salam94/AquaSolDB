# -*- coding: utf-8 -*-
"""Shared fixtures: which release is under test, and its tables, read once.

Every test here runs against SHIPPED FILES -- the CSVs of a packaged release, found the
same way a downloader's code finds them (`AQUASOLDB_ROOT`, or the folder beside the
package).  Point `AQUASOLDB_ROOT` at any release folder to test that one.  Nothing is
generated for the tests to read, except the small fakes a test builds for itself in a
temporary folder (named where they are made).
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
    """`{name: DataFrame}` for the six tables of csv/, read once for the whole session."""
    return {name: aquasoldb.open_table(name, root=root) for name in aquasoldb.TABLE_NAMES}


@pytest.fixture(scope="session")
def details(root):
    """`{name: DataFrame}` for the three files of detail/, read once for the session."""
    old = os.environ.get(aquasoldb.AQUASOLDB_ROOT_ENV)
    os.environ[aquasoldb.AQUASOLDB_ROOT_ENV] = root
    try:
        return {name: aquasoldb.open_detail(name) for name in aquasoldb.DETAIL_NAMES}
    finally:
        if old is None:
            del os.environ[aquasoldb.AQUASOLDB_ROOT_ENV]
        else:
            os.environ[aquasoldb.AQUASOLDB_ROOT_ENV] = old


@pytest.fixture(scope="session")
def measurements(tables):
    """`{name: DataFrame}` for the five measurement tables only."""
    return {n: tables[n] for n in aquasoldb.MEASUREMENT_TABLES}


@pytest.fixture(scope="session")
def solubility(tables):
    return tables["solubility"]
