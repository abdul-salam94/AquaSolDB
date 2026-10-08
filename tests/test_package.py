# -*- coding: utf-8 -*-
"""The AquaSolDB reader, tested against the files a release actually ships.

Two rules shape these tests.  Row counts are read from the shipped `SCHEMA.md` rather
than typed here, so a release that grows stays green while a release whose schema has
drifted from its CSVs goes red -- the failure that matters.  And nothing is loosened to
pass: a blank ion cell must stay blank through every derived quantity, and a charge
balance that misses is a red, not a tolerance to widen.

The download tests never go online: they serve a fake archive record, built in a
temporary folder from the release under test, through the one function the package uses
to fetch a URL.
"""
import hashlib
import io
import json
import math
import os
import re
import shutil
import sys
import zipfile

import pandas as pd
import pytest

import aquasoldb
from aquasoldb import brine, remote, save, subset, tables as tables_module

# Rows pinned by their permanent point_id (point_ids are permanent and are never
# renumbered).  Each is checked against arithmetic done by hand from the printed
# composition, so the test states an independent answer rather than restating the code.
NACL_ROW = "C2H6_bennaimyaacobi1974_c2c4_011"     # NaCl: m_Na = m_Cl = 1.021036
MIXED_ROW = "CH4_byrnestoessell1982_ch4_004"      # Cl 4, Ca 1, Mg 1 mol/kg water
BLANK_ROW = "C3H8_wenhung1970_c2c4_002"           # NH4Br: an ion outside the six

#: The charge-balance tolerance the release states (SCHEMA.md): the storage precision of
#: the record behind each row.  It is a ceiling, never to be raised to make a row pass.
CHARGE_BALANCE_TOL = 5e-6

# The mole-fraction examples worked by hand for the release's web viewer, with the
# viewer's own tolerances: the same rows must give the same numbers here.
#   pure water: m = 0.418856, x = 0.418856 / (0.418856 + 55.508373) = 0.0074893036, and
#               with the salt counted the same (no ions);
#   NaCl 2 mol/kg: m = 0.849, x = 0.849 / 56.357373 = 0.015064577; ions 2 + 2 = 4, so with
#               the salt x = 0.849 / 60.357373 = 0.014066218; I = 2, charge balance 0.
VIEWER_PURE_WATER = ("CO2_liu2011_co2_009", 0.0074893036, 1e-10)
VIEWER_NACL = ("CO2_wang2019_co2_269", 0.015064577, 0.014066218, 1e-9)
N_W = 1000.0 / 18.0153

SCHEMA_COUNT = re.compile(r"^## `(csv|detail)/([a-z_]+)\.csv`\s+\((\d+) rows\)$", re.MULTILINE)


def _row(df, point_id):
    hit = df[df["point_id"] == point_id]
    assert len(hit) == 1, (
        "%s is pinned by this test and the release holds %d row(s) with that point_id. "
        "point_ids are permanent; if this row was withdrawn, re-pin the test on a row "
        "with a comparable composition -- do not delete the check."
        % (point_id, len(hit)))
    return hit


# --------------------------------------------------------------- loading
def test_every_table_loads_and_its_row_count_matches_the_schema(root, tables, details):
    """SCHEMA.md states every file's row count; the files must hold exactly that."""
    with open(os.path.join(root, "SCHEMA.md"), encoding="utf-8") as fh:
        stated = {name: int(n) for _folder, name, n in SCHEMA_COUNT.findall(fh.read())}
    loaded = dict(tables, **details)
    for name, df in loaded.items():
        assert name in stated, "SCHEMA.md states no row count for %s" % name
        assert len(df) == stated[name], "%s holds %d rows; SCHEMA.md states %d" % (
            name, len(df), stated[name])
    assert set(aquasoldb.TABLE_NAMES) <= set(stated)


def test_every_source_in_the_table_is_named_by_at_least_one_row(tables, measurements):
    listed = set(tables["sources"]["source_id"])
    used = set()
    for df in measurements.values():
        used |= set(df["source_id"])
    assert used <= listed, sorted(used - listed)[:10]
    assert listed == used, ("sources with no published row: %s"
                            % sorted(listed - used)[:10])


def test_columns_are_typed_from_the_shipped_dictionary(root, tables, details):
    declared = tables_module.dtypes_from_dictionary(root)
    for name, df in dict(tables, **details).items():
        assert list(df.columns) == list(declared[name]), name
        for column in df.columns:
            want = declared[name][column]
            got = str(df[column].dtype)
            assert got == want, "%s.%s is %s, the dictionary asks for %s" % (
                name, column, got, want)
    # The two types that carry the reading rules: state is numeric, the as-printed cell
    # is text (it holds decimal commas, printed uncertainties, ILLEGIBLE and NOT PRINTED).
    assert tables["solubility"]["temperature_K"].dtype == "float64"
    assert str(details["printed_values"]["value_as_printed"].dtype) == "string"


def test_a_blank_number_is_nan_and_a_blank_text_cell_is_empty(solubility):
    assert solubility["pressure_MPa"].isna().any(), "no blank pressure anywhere to check"
    clean = solubility[solubility["flags"] == ""]
    assert len(clean) > 0
    assert not solubility["flags"].isna().any(), (
        "a blank flags cell must read as the empty string, not as missing")


def test_a_printed_na_like_word_is_not_read_as_missing(details):
    """`keep_default_na` is off for text: the page's words survive as words."""
    printed = details["printed_values"]["value_as_printed"]
    assert not printed.isna().any(), "no as-printed cell may be NaN; blank reads as ''"
    assert printed.str.startswith("NOT PRINTED").any()
    assert printed.str.startswith("ILLEGIBLE").any()


def test_open_table_and_open_detail_refuse_a_file_the_release_does_not_ship(root):
    with pytest.raises(ValueError) as exc:
        aquasoldb.open_table("henry_constants", root=root)
    assert "henry_constants" in str(exc.value)
    with pytest.raises(ValueError) as exc:
        aquasoldb.open_table("printed_values", root=root)
    assert "open_detail" in str(exc.value)
    with pytest.raises(ValueError) as exc:
        aquasoldb.open_detail("solubility")
    assert "open_table" in str(exc.value)


def test_release_folder_refuses_a_folder_that_is_not_a_release(tmp_path):
    with pytest.raises(FileNotFoundError):
        aquasoldb.release_folder(tmp_path)


def test_the_root_environment_variable_is_honoured(root, monkeypatch, tmp_path):
    monkeypatch.setenv(tables_module.AQUASOLDB_ROOT_ENV, str(root))
    assert aquasoldb.release_folder() == os.path.abspath(str(root))
    monkeypatch.setenv(tables_module.AQUASOLDB_ROOT_ENV, str(tmp_path))
    with pytest.raises(FileNotFoundError):
        aquasoldb.release_folder()


# --------------------------------------------------------------- checksums
def test_the_checksum_check_passes_on_the_shipped_files_and_catches_an_edited_byte(
        root, tmp_path):
    verified = aquasoldb.verify_checksums(root=root)
    assert "csv/solubility.csv" in verified
    assert "detail/printed_values.csv" in verified

    copy = tmp_path / "release"
    shutil.copytree(root, copy, ignore=shutil.ignore_patterns("__pycache__", ".git"))
    target = copy / "csv" / "water_content.csv"
    text = target.read_text(encoding="utf-8")
    target.write_text(text + "\n", encoding="utf-8", newline="")
    with pytest.raises(ValueError) as exc:
        aquasoldb.verify_checksums(root=copy)
    assert "water_content" in str(exc.value)
    with pytest.raises(ValueError):
        aquasoldb.open_table("water_content", root=copy, verify=True)
    # ... and the check really is opt-in: the same edited file loads without it.
    assert len(aquasoldb.open_table("water_content", root=copy)) > 0


# --------------------------------------------------------------- download
def _fake_archive(root, as_zip, corrupt=None):
    """A fake archive record of the release under test, served from memory.

    as_zip=True deposits one zip with a top folder (as an archive made from a repository
    release is); False deposits each file on its own.  `corrupt` names a file whose
    listed hash is wrong.  Returns (fake _get, the URLs it was asked for)."""
    files = {}
    for dirpath, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
        for n in names:
            path = os.path.join(dirpath, n)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            with open(path, "rb") as fh:
                files[rel] = fh.read()
    if as_zip:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for rel, data in files.items():
                zf.writestr("someone-AquaSolDB-0123abc/" + rel, data)
        files = {"AquaSolDB-v%s.zip" % aquasoldb.DATASET_VERSION: buffer.getvalue()}
    served, entries = {}, []
    for n, (key, data) in enumerate(sorted(files.items())):
        url = "https://archive.invalid/files/%d" % n
        served[url] = data
        digest = hashlib.md5(data).hexdigest()
        if key == corrupt:
            digest = hashlib.md5(data + b"x").hexdigest()
        entries.append({"key": key, "checksum": "md5:" + digest, "links": {"self": url}})
    versions = {"hits": {"hits": [
        {"id": 2, "metadata": {"version": "1.2"}, "files": []},
        {"id": 3, "metadata": {"version": aquasoldb.DATASET_VERSION}, "files": entries}]}}
    listing = "%s/records/%s/versions?size=200" % (
        remote.ZENODO_API, aquasoldb.CONCEPT_DOI.rsplit(".", 1)[1])
    served[listing] = json.dumps(versions).encode("utf-8")
    asked = []

    def fake_get(url):
        asked.append(url)
        if url not in served:
            raise AssertionError("the package asked for an unexpected URL: %s" % url)
        return served[url]
    return fake_get, asked


@pytest.mark.parametrize("as_zip", [True, False], ids=["zip", "files"])
def test_download_fetches_the_record_checks_every_hash_and_caches_it(
        root, tmp_path, monkeypatch, as_zip):
    fake_get, asked = _fake_archive(root, as_zip)
    monkeypatch.setattr(remote, "_get", fake_get)
    cache = tmp_path / "cache"
    got = aquasoldb.download(cache=cache)
    assert got == os.path.join(str(cache), aquasoldb.DATASET_VERSION)
    assert asked[0].endswith("/records/%s/versions?size=200"
                             % aquasoldb.CONCEPT_DOI.rsplit(".", 1)[1]), asked[0]
    assert aquasoldb.verify_checksums(root=got)
    for name in aquasoldb.TABLE_NAMES:
        a = aquasoldb.open_table(name, root=got)
        b = aquasoldb.open_table(name, root=root)
        pd.testing.assert_frame_equal(a, b)
    # Nothing but the release is left in the cache.
    assert sorted(os.listdir(cache)) == [aquasoldb.DATASET_VERSION]


def test_download_refuses_a_file_whose_hash_does_not_match_the_record(
        root, tmp_path, monkeypatch):
    for as_zip, corrupt in ((True, "AquaSolDB-v%s.zip" % aquasoldb.DATASET_VERSION),
                            (False, "csv/solubility.csv")):
        fake_get, _asked = _fake_archive(root, as_zip, corrupt=corrupt)
        monkeypatch.setattr(remote, "_get", fake_get)
        cache = tmp_path / ("cache_zip" if as_zip else "cache_files")
        with pytest.raises(ValueError) as exc:
            aquasoldb.download(cache=cache)
        assert corrupt in str(exc.value) and "hash" in str(exc.value)
        assert os.listdir(cache) == [], os.listdir(cache)
    with pytest.raises(LookupError):
        aquasoldb.download(version="9.9", cache=tmp_path / "cache_none")


def test_download_uses_the_cache_without_going_online_and_release_folder_finds_it(
        root, tmp_path, monkeypatch):
    fake_get, _asked = _fake_archive(root, True)
    monkeypatch.setattr(remote, "_get", fake_get)
    cache = tmp_path / "cache"
    got = aquasoldb.download(cache=cache)

    def offline(url):
        raise AssertionError("went online for %s with a release in the cache" % url)
    monkeypatch.setattr(remote, "_get", offline)
    assert aquasoldb.download(cache=cache) == got
    # release_folder: argument, environment, beside the package, then the cache.
    monkeypatch.delenv(tables_module.AQUASOLDB_ROOT_ENV, raising=False)
    monkeypatch.setattr(tables_module, "_beside_the_package", lambda: None)
    monkeypatch.setenv(remote.AQUASOLDB_CACHE_ENV, str(cache))
    assert aquasoldb.release_folder() == got
    monkeypatch.setenv(remote.AQUASOLDB_CACHE_ENV, str(tmp_path / "empty"))
    with pytest.raises(FileNotFoundError) as exc:
        aquasoldb.release_folder()
    assert "download()" in str(exc.value)


# --------------------------------------------------------------- subset
def test_narrow_composes_gas_medium_and_the_two_windows(solubility):
    got = subset.narrow(solubility, gas="CO2", medium="brine",
                        T_K=(298.15, 373.15), P_MPa=(1.0, 20.0))
    assert len(got) > 0
    assert set(got["gas"]) == {"CO2"}
    assert "none" not in set(got["salt"])
    assert got["temperature_K"].min() >= 298.15
    assert got["temperature_K"].max() <= 373.15
    assert got["pressure_MPa"].between(1.0, 20.0).all()
    assert len(got) < len(solubility)


def test_a_range_never_keeps_a_row_whose_value_is_blank(solubility):
    blank_p = solubility[solubility["pressure_MPa"].isna()]
    assert len(blank_p) > 0, "no blank pressure to check against"
    wide = subset.narrow(solubility, P_MPa=(None, None))
    assert set(wide["point_id"]).isdisjoint(set(blank_p["point_id"]))
    assert len(wide) == int(solubility["pressure_MPa"].notna().sum())


def test_the_two_media_partition_every_row_whose_medium_was_recorded(measurements):
    for name, df in measurements.items():
        water = subset.narrow(df, medium="water")
        brine_rows = subset.narrow(df, medium="brine")
        recorded = df[~df["salt"].isin(["", aquasoldb.NOT_STATED])]
        assert len(water) + len(brine_rows) == len(recorded), name
        assert set(water["salt"]) == {"none"}, name
        assert not set(brine_rows["salt"]) & {"none", aquasoldb.NOT_STATED}, name
    sol_water = subset.narrow(measurements["solubility"], medium="water")
    assert (sol_water[list(brine.ION_COLUMNS)] == 0.0).all().all(), (
        "a pure-water solubility row carries six zeros, never six blanks")


def test_not_stated_is_neither_water_nor_brine_and_can_be_selected(tables):
    df = tables["water_content"]
    not_stated = df[df["salt"] == aquasoldb.NOT_STATED]
    assert len(not_stated) > 0, "no not_stated row to check against"
    ids = set(not_stated["point_id"])
    for medium in subset.MEDIA:
        assert ids.isdisjoint(subset.narrow(df, medium=medium)["point_id"]), medium
    picked = subset.narrow(df, salt="not_stated")
    assert set(picked["point_id"]) == ids
    assert not (df["salt"] == "").any(), "a blank salt cell; the release writes not_stated"


def test_narrow_by_status_and_phase(tables):
    sol = tables["solubility"]
    for status in sol["status"].unique():
        got = subset.narrow(sol, status=status)
        assert set(got["status"]) == {status}
        assert len(got) == int((sol["status"] == status).sum())
    both = subset.narrow(sol, status=["measured", "calculated"])
    assert len(both) == int(sol["status"].isin(["measured", "calculated"]).sum())
    oq = tables["other_quantities"]
    assert (oq["status"] == "no_value").any()
    assert set(subset.narrow(oq, status="no_value")["status"]) == {"no_value"}
    wc = tables["water_content"]
    assert wc["phase"].nunique() >= 2
    for phase in wc["phase"].unique():
        got = subset.narrow(wc, phase=phase)
        assert set(got["phase"]) == {phase}
        assert len(got) == int((wc["phase"] == phase).sum())
    assert len(subset.narrow(wc, phase=list(wc["phase"].unique()))) == len(wc)
    with pytest.raises(ValueError) as exc:
        subset.narrow(sol, status="measrued")
    assert "measrued" in str(exc.value)
    with pytest.raises(ValueError):
        subset.narrow(wc, phase="liquid")
    with pytest.raises(KeyError):
        subset.narrow(sol, phase="vapour")          # solubility has no phase column


def test_narrow_refuses_a_value_the_column_does_not_hold(solubility):
    with pytest.raises(ValueError) as exc:
        subset.narrow(solubility, gas="Ne")
    assert "Ne" in str(exc.value)
    with pytest.raises(ValueError):
        subset.narrow(solubility, salt="NaCI")          # capital i, not l
    with pytest.raises(ValueError):
        subset.narrow(solubility, source_id="no_such_source_1999_ch4")
    with pytest.raises(ValueError):
        subset.narrow(solubility, medium="seawater")     # a salt, not a medium
    with pytest.raises(ValueError):
        subset.narrow(solubility, T_K=(400.0, 300.0))


def test_flags_exclude_drops_exactly_the_flagged_rows(solubility):
    carried = solubility["flags"].str.contains("digitized_from_figure")
    assert carried.any(), "no digitized rows to exclude"
    got = subset.narrow(solubility, flags_exclude="digitized_from_figure")
    assert len(got) == int((~carried).sum())
    assert not got["flags"].str.contains("digitized_from_figure").any()
    both = subset.narrow(solubility, flags_exclude=list(subset.FLAG_VOCABULARY))
    assert set(both["flags"]) == {""}
    with pytest.raises(ValueError) as exc:
        subset.narrow(solubility, flags_exclude="fit_holdout")
    assert "fit_holdout" in str(exc.value)


def test_narrow_says_so_when_a_table_has_no_such_column(tables):
    with pytest.raises(KeyError):
        subset.narrow(tables["sources"], gas="CO2")


# --------------------------------------------------------------- brine
def test_derived_quantities_on_a_known_nacl_row(solubility):
    row = _row(solubility, NACL_ROW)
    m = float(row["m_Na"].iloc[0])
    assert m == pytest.approx(1.021036, abs=1e-9)
    assert float(row["m_Cl"].iloc[0]) == pytest.approx(m, abs=1e-12)
    # A 1:1 salt: I equals the salt molality, the ion total is twice it, balance is zero.
    assert float(brine.ion_strength(row).iloc[0]) == pytest.approx(m, abs=1e-12)
    assert float(brine.total_ions(row).iloc[0]) == pytest.approx(2 * m, 1e-12)
    assert float(brine.charge_residual(row).iloc[0]) == pytest.approx(0.0, abs=1e-12)
    assert bool(brine.composition_known(row).iloc[0])
    assert float(row["salt_molality"].iloc[0]) == pytest.approx(m, abs=1e-9)


def test_derived_quantities_on_a_known_mixed_brine_row(solubility):
    """Cl 4, Ca 1, Mg 1 mol/kg water: I = 0.5*(4*1 + 1*4 + 1*4) = 6, total = 6."""
    row = _row(solubility, MIXED_ROW)
    assert [float(row[c].iloc[0]) for c in brine.ION_COLUMNS] == [0.0, 4.0, 0.0,
                                                                   1.0, 1.0, 0.0]
    assert float(brine.ion_strength(row).iloc[0]) == pytest.approx(6.0, abs=1e-12)
    assert float(brine.total_ions(row).iloc[0]) == pytest.approx(6.0, abs=1e-12)
    assert float(brine.charge_residual(row).iloc[0]) == pytest.approx(0.0, abs=1e-12)
    assert bool(brine.composition_known(row).iloc[0])


def test_a_blank_composition_propagates_to_nan_and_is_never_guessed(solubility):
    """The mixed brine whose ion is outside the six: blank in, NaN out, nothing filled."""
    row = _row(solubility, BLANK_ROW)
    assert row[list(brine.ION_COLUMNS)].isna().all().all()
    assert not bool(brine.composition_known(row).iloc[0])
    for quantity in (brine.ion_strength, brine.total_ions, brine.charge_residual):
        assert math.isnan(float(quantity(row).iloc[0])), quantity.__name__
    assert math.isnan(float(brine.to_mole_fraction(row, include_salt=True).iloc[0]))
    # The row's salt_molality is printed and present: a known total must NOT be taken as
    # a composition, which is exactly the substitution the ion rule forbids.
    assert not pd.isna(row["salt_molality"].iloc[0])


def test_the_whole_or_blank_ion_rule_is_enforced_and_not_worked_around(solubility):
    """Fault injection: three of six filled is a broken file, and must raise."""
    broken = _row(solubility, MIXED_ROW).copy()
    broken.loc[broken.index[0], "m_Cl"] = float("nan")
    with pytest.raises(ValueError) as exc:
        brine.ion_strength(broken)
    assert "ion rule" in str(exc.value)
    with pytest.raises(ValueError):
        brine.composition_known(broken)


def test_a_column_dropped_as_always_zero_reads_as_zero_and_no_other(root, tables):
    """A file leaves out an ion column only where the dictionary declares it dropped as
    always zero; that column reads as zero, and only that one."""
    mix = tables["mixtures"]
    dropped = mix.attrs[tables_module.ATTR_DROPPED_ZERO]
    assert dropped and not set(dropped) & set(mix.columns), dropped
    filled = mix[mix[[c for c in brine.ION_COLUMNS if c in mix.columns]].notna().all(axis=1)]
    assert len(filled) > 0
    ions = brine._ions(filled)
    assert (ions[list(dropped)] == 0.0).all().all()
    expected = sum(filled[c] * brine.ION_CHARGE_NUMBER[c] ** 2
                   for c in brine.ION_COLUMNS if c in mix.columns) * 0.5
    assert (brine.ion_strength(filled) - expected).abs().max() == 0.0
    # The same frame without the dictionary's word is an error, not a zero.
    bare = filled.copy()
    bare.attrs = {}
    with pytest.raises(KeyError) as exc:
        brine.total_ions(bare)
    assert dropped[0] in str(exc.value)
    # A column the dictionary does NOT declare dropped is an error even with the word.
    sol = tables["solubility"]
    assert sol.attrs[tables_module.ATTR_DROPPED_ZERO] == ()
    with pytest.raises(KeyError) as exc:
        brine.ion_strength(sol.drop(columns=["m_K"]))
    assert "m_K" in str(exc.value)


def test_a_file_without_ion_columns_knows_pure_water_only(tables):
    """water_content carries no ion column (all six dropped as always zero): a pure-water
    row is zero ions, every other row's composition is blank."""
    wc = tables["water_content"]
    assert not set(brine.ION_COLUMNS) & set(wc.columns)
    known = brine.composition_known(wc)
    pure = wc["salt"] == "none"
    assert pure.any() and (~pure).any()
    assert (known == pure).all()
    assert (brine.total_ions(wc)[pure] == 0.0).all()
    assert brine.total_ions(wc)[~pure].isna().all()


def test_charge_balance_holds_on_every_published_row(measurements):
    """The release states a 5e-6 ceiling; this is the check that keeps it true."""
    worst = 0.0
    for name, df in measurements.items():
        residual = brine.charge_residual(df).abs()
        known = brine.composition_known(df)
        assert residual[~known].isna().all(), name
        bad = df.loc[known & (residual > CHARGE_BALANCE_TOL), "point_id"]
        assert bad.empty, "%s: %d row(s) miss charge balance, first %s" % (
            name, len(bad), bad.iloc[0] if len(bad) else "")
        if known.any():
            worst = max(worst, float(residual[known].max()))
    assert worst <= CHARGE_BALANCE_TOL


def test_every_row_is_either_wholly_known_or_wholly_blank(measurements):
    """No published row carries a part composition; both kinds exist in the release.
    Known: the file's ion cells filled, or pure water."""
    known = blank = 0
    for name, df in measurements.items():
        got = brine.composition_known(df)            # raises on a partial row
        present = [c for c in brine.ION_COLUMNS if c in df.columns]
        filled = df[present].notna().all(axis=1) if present else False
        assert (got == (filled | (df["salt"] == "none"))).all(), name
        known += int(got.sum())
        blank += int((~got).sum())
    assert known > 0 and blank > 0, (known, blank)
    assert known + blank == sum(len(df) for df in measurements.values())


# --------------------------------------------------------------- mole fraction
def test_to_mole_fraction_is_m_over_m_plus_the_water(tables):
    for name in ("solubility", "mixtures"):
        df = tables[name]
        m = df["solubility_mol_per_kgw"]
        x = brine.to_mole_fraction(df)
        assert (x - m / (m + N_W)).abs().max() == 0.0, name
        assert x.isna().sum() == m.isna().sum()
        assert ((x >= 0) & (x < 1)).all(), name
    with pytest.raises(KeyError):
        brine.to_mole_fraction(tables["water_content"])
    assert brine.WATER_MOL_PER_KG == pytest.approx(55.508373, abs=5e-7)


def test_to_mole_fraction_with_the_salt_counted(tables):
    sol = tables["solubility"]
    pid, x_pure, tol = VIEWER_PURE_WATER
    row = _row(sol, pid)
    assert float(brine.to_mole_fraction(row).iloc[0]) == pytest.approx(x_pure, abs=tol)
    assert float(brine.to_mole_fraction(row, include_salt=True).iloc[0]) == \
        float(brine.to_mole_fraction(row).iloc[0])
    pid, x_free, x_salt, tol = VIEWER_NACL
    row = _row(sol, pid)
    assert float(brine.to_mole_fraction(row).iloc[0]) == pytest.approx(x_free, abs=tol)
    assert float(brine.to_mole_fraction(row, include_salt=True).iloc[0]) == \
        pytest.approx(x_salt, abs=tol)
    assert float(brine.ion_strength(row).iloc[0]) == 2.0
    assert float(brine.total_ions(row).iloc[0]) == 4.0
    assert float(brine.charge_residual(row).iloc[0]) == 0.0
    for name in ("solubility", "mixtures"):
        df = tables[name]
        m = df["solubility_mol_per_kgw"]
        s = brine.total_ions(df)
        x = brine.to_mole_fraction(df, include_salt=True)
        assert (x - m / (m + N_W + s)).abs().max() == 0.0, name
        assert x[~brine.composition_known(df)].isna().all(), name
        pure = df["salt"] == "none"
        same = brine.to_mole_fraction(df)[pure]
        assert (x[pure] - same).abs().max() == 0.0, name
        salty = brine.composition_known(df) & (s > 0) & m.notna() & (m > 0)
        assert salty.any() and (x[salty] < brine.to_mole_fraction(df)[salty]).all(), name


# --------------------------------------------------------------- citation and detail
def test_with_citation_adds_the_reference_and_doi_of_each_row(tables):
    sol = subset.narrow(tables["solubility"], gas="H2")
    got = aquasoldb.with_citation(sol)
    assert list(got.columns) == list(sol.columns) + ["reference", "doi"]
    assert got.index.equals(sol.index)
    assert got["point_id"].tolist() == sol["point_id"].tolist()
    sources = tables["sources"].set_index("source_id")
    assert got["reference"].tolist() == sources.loc[sol["source_id"], "reference"].tolist()
    assert got["doi"].tolist() == sources.loc[sol["source_id"], "doi"].tolist()
    assert (got["reference"].str.strip() != "").all()
    broken = sol.head(2).copy()
    broken.loc[broken.index[0], "source_id"] = "no_such_source_1999_h2"
    with pytest.raises(KeyError) as exc:
        aquasoldb.with_citation(broken)
    assert "no_such_source_1999_h2" in str(exc.value)
    with pytest.raises(ValueError):
        aquasoldb.with_citation(tables["sources"])


def test_open_detail_printed_values_has_one_row_per_measurement_row(measurements, details):
    printed = details["printed_values"]
    ids = []
    for df in measurements.values():
        ids += df["point_id"].tolist()
    assert len(ids) == len(set(ids)), "a point_id repeats across the measurement files"
    assert printed["point_id"].is_unique
    assert set(printed["point_id"]) == set(ids)
    joined = measurements["solubility"].merge(printed, on="point_id", how="left",
                                              validate="one_to_one")
    assert len(joined) == len(measurements["solubility"])
    assert str(details["excluded_sources"]["rows_left_out"].dtype) == "Int64"
    assert (details["excluded_sources"]["rows_left_out"] > 0).all()
    changes = details["id_changes"]
    assert changes["old_point_id"].is_unique
    assert set(changes["old_point_id"]).isdisjoint(ids), (
        "an id listed as changed still ships under that id")
    renamed = changes[changes["new_point_id"] != ""]
    assert set(renamed["new_point_id"]) <= set(ids)


# --------------------------------------------------------------- save
def test_save_csv_round_trips_a_selection(solubility, tmp_path):
    got = subset.narrow(solubility, gas="H2", medium="brine")
    assert len(got) > 0
    out = tmp_path / "h2_brine.csv"
    assert save.save_csv(got, out) == out
    assert b"\r\n" not in out.read_bytes(), "the release writes LF, not CRLF"
    back = pd.read_csv(out)
    assert len(back) == len(got)
    assert list(back.columns) == list(got.columns)
    assert back["temperature_K"].tolist() == got["temperature_K"].tolist()


@pytest.mark.skipif(save.parquet_available(),
                    reason="pyarrow IS installed, so the missing-dependency path "
                           "cannot be exercised here")
def test_save_parquet_names_the_missing_dependency(solubility, tmp_path):
    with pytest.raises(ImportError) as exc:
        save.save_parquet(solubility.head(5), tmp_path / "x.parquet")
    assert save.PARQUET_DEPENDENCY in str(exc.value)


@pytest.mark.skipif(not save.parquet_available(),
                    reason="parquet is optional and pyarrow is not installed; "
                           "the release is CSV only")
def test_save_parquet_round_trips_a_selection(solubility, tmp_path):
    got = subset.narrow(solubility, gas="H2", medium="brine")
    out = tmp_path / "h2_brine.parquet"
    assert save.save_parquet(got, out) == out
    back = pd.read_parquet(out)
    assert len(back) == len(got)
    assert list(back.columns) == list(got.columns)


# --------------------------------------------------------------- packaging
def test_the_declared_version_is_the_one_pyproject_ships():
    import tomllib
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(here, "pyproject.toml"), "rb") as fh:
        meta = tomllib.load(fh)["project"]
    assert meta["name"] == "aquasoldb"
    assert meta["version"] == aquasoldb.__version__
    assert aquasoldb.DATASET_VERSION == ".".join(aquasoldb.__version__.split(".")[:2])
    assert any(d.replace(" ", "").startswith("pandas>=2") for d in meta["dependencies"])
    assert len(meta["dependencies"]) == 1, meta["dependencies"]


def test_the_module_entry_point_prints_a_count_per_table(root, capsys):
    from aquasoldb.__main__ import print_counts
    assert print_counts([str(root)]) == 0
    printed = capsys.readouterr().out
    for name in aquasoldb.TABLE_NAMES:
        assert re.search(r"^\s+%s\s+\d+ rows$" % name, printed, re.MULTILINE), printed
    assert printed.startswith("aquasoldb %s reading " % aquasoldb.__version__)
    assert print_counts([str(root), "extra"]) == 2
    assert sys.modules["aquasoldb"].__version__ == "2.0.0"
