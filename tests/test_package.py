# -*- coding: utf-8 -*-
"""The AquaSolDB reader, tested against the files a release actually ships.

Two rules shape these tests.  Row counts are read from the shipped `csv/sources.csv`
rather than typed here, so a release that grows stays green while a release whose sources
table has drifted from its CSVs goes red -- the failure that matters.  And nothing is
loosened to pass: a blank ion cell must stay blank through every derived quantity, and a
charge balance that misses is a red, not a tolerance to widen.
"""
import math
import os
import shutil
import sys

import pandas as pd
import pytest

import aquasoldb
from aquasoldb import brine, save, subset, tables as tables_module

# Two rows pinned by their permanent point_id (R-DB3-8: point_ids are permanent and are
# never renumbered).  Each is checked against arithmetic done by hand from the printed
# composition, so the test states an independent answer rather than restating the code.
NACL_ROW = "C2H6_bennaimyaacobi1974_c2c4_011"     # NaCl: m_Na = m_Cl = 1.021036
MIXED_ROW = "CH4_byrnestoessell1982_ch4_004"      # Cl 4, Ca 1, Mg 1 mol/kg water
BLANK_ROW = "C3H8_wenhung1970_c2c4_002"           # NH4Br: an ion outside the six

#: The charge-balance tolerance the release states (SCHEMA.md): the storage precision of
#: the record behind each row.  It is a ceiling, never to be raised to make a row pass.
CHARGE_BALANCE_TOL = 5e-6


def _row(df, point_id):
    hit = df[df["point_id"] == point_id]
    assert len(hit) == 1, (
        "%s is pinned by this test and the release holds %d row(s) with that point_id. "
        "point_ids are permanent; if this row was withdrawn, re-pin the test on a row "
        "with a comparable composition -- do not delete the check."
        % (point_id, len(hit)))
    return hit


# --------------------------------------------------------------- loading
def test_every_family_loads_and_its_row_count_matches_the_sources_table(tables):
    """The sources table's per-file counts are the release's own statement of its size."""
    sources = tables["sources"]
    assert len(sources) > 0
    for family in aquasoldb.MEASUREMENT_TABLES:
        declared = int(sources["n_%s" % family].fillna(0).sum())
        assert len(tables[family]) == declared, (
            "%s.csv holds %d rows; sources.csv declares %d"
            % (family, len(tables[family]), declared))


def test_every_source_in_the_table_is_named_by_at_least_one_row(tables, measurements):
    listed = set(tables["sources"]["source_id"])
    used = set()
    for df in measurements.values():
        used |= set(df["source_id"])
    assert used <= listed, sorted(used - listed)[:10]
    assert listed == used, ("sources with no published row: %s"
                            % sorted(listed - used)[:10])


def test_columns_are_typed_from_the_shipped_dictionary(root, tables):
    declared = tables_module.dtypes_from_dictionary(root)
    for family, df in tables.items():
        for column in df.columns:
            assert column in declared[family], (family, column)
            want = declared[family][column]
            got = str(df[column].dtype)
            assert got == want, "%s.%s is %s, the dictionary asks for %s" % (
                family, column, got, want)
    # The two types that carry the reading rules: state is numeric, the as-printed cell
    # is text (it holds decimal commas, printed uncertainties, ILLEGIBLE and NOT PRINTED).
    sol = tables["solubility"]
    assert sol["temperature_K"].dtype == "float64"
    assert str(sol["value_as_printed"].dtype) == "string"


def test_a_blank_number_is_nan_and_a_blank_text_cell_is_empty(solubility):
    assert solubility["pressure_MPa"].isna().any(), "no blank pressure anywhere to check"
    clean = solubility[solubility["flags"] == ""]
    assert len(clean) > 0
    assert not solubility["flags"].isna().any(), (
        "a blank flags cell must read as the empty string, not as missing")


def test_a_printed_na_like_word_is_not_read_as_missing(solubility):
    """`keep_default_na` is off for text: the page's words survive as words."""
    printed = solubility["value_as_printed"]
    assert not printed.isna().any(), "no as-printed cell may be NaN; blank reads as ''"
    assert (printed == "NOT PRINTED").any() or (printed == "ILLEGIBLE").any()


def test_open_table_refuses_a_family_the_release_does_not_ship(root):
    with pytest.raises(ValueError) as exc:
        aquasoldb.open_table("henry_constants", root=root)
    assert "henry_constants" in str(exc.value)


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
    assert len(verified) >= 7, verified
    assert "csv/solubility.csv" in verified

    copy = tmp_path / "release"
    shutil.copytree(root, copy)
    target = copy / "csv" / "liquidwatercontent.csv"
    text = target.read_text(encoding="utf-8")
    target.write_text(text + "\n", encoding="utf-8", newline="")
    with pytest.raises(ValueError) as exc:
        aquasoldb.verify_checksums(root=copy)
    assert "liquidwatercontent" in str(exc.value)
    with pytest.raises(ValueError):
        aquasoldb.open_table("liquidwatercontent", root=copy, verify=True)
    # ... and the check really is opt-in: the same edited file loads without it.
    assert len(aquasoldb.open_table("liquidwatercontent", root=copy)) > 0


# --------------------------------------------------------------- subset
def test_narrow_composes_gas_medium_and_the_two_windows(solubility):
    got = subset.narrow(solubility, gas="CO2", medium="brine",
                         T_K=(298.15, 373.15), P_MPa=(1.0, 20.0))
    assert len(got) > 0
    assert set(got["gas"]) == {"CO2"}
    assert set(got["salt"]) != {"none"} and "none" not in set(got["salt"])
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


def test_the_two_media_partition_every_row_whose_medium_was_recorded(solubility):
    water = subset.narrow(solubility, medium="water")
    brine_rows = subset.narrow(solubility, medium="brine")
    recorded = solubility[solubility["salt"].str.strip() != ""]
    assert len(water) + len(brine_rows) == len(recorded)
    assert set(water["salt"]) == {"none"}
    assert "none" not in set(brine_rows["salt"])
    assert (water[list(brine.ION_COLUMNS)] == 0.0).all().all(), (
        "a pure-water row carries six zeros, never six blanks")


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
    assert float(brine.charge_residual(row).iloc[0]) == pytest.approx(0.0,
                                                                                abs=1e-12)
    assert bool(brine.composition_known(row).iloc[0])
    assert float(row["salt_molality"].iloc[0]) == pytest.approx(m, abs=1e-9)


def test_derived_quantities_on_a_known_mixed_brine_row(solubility):
    """Cl 4, Ca 1, Mg 1 mol/kg water: I = 0.5*(4*1 + 1*4 + 1*4) = 6, total = 6."""
    row = _row(solubility, MIXED_ROW)
    assert [float(row[c].iloc[0]) for c in brine.ION_COLUMNS] == [0.0, 4.0, 0.0,
                                                                    1.0, 1.0, 0.0]
    assert float(brine.ion_strength(row).iloc[0]) == pytest.approx(6.0, abs=1e-12)
    assert float(brine.total_ions(row).iloc[0]) == pytest.approx(6.0, abs=1e-12)
    assert float(brine.charge_residual(row).iloc[0]) == pytest.approx(0.0,
                                                                                abs=1e-12)
    assert bool(brine.composition_known(row).iloc[0])


def test_a_blank_composition_propagates_to_nan_and_is_never_guessed(solubility):
    """The mixed brine whose ion is outside the six: blank in, NaN out, nothing filled."""
    row = _row(solubility, BLANK_ROW)
    assert row[list(brine.ION_COLUMNS)].isna().all().all()
    assert not bool(brine.composition_known(row).iloc[0])
    for quantity in (brine.ion_strength, brine.total_ions,
                     brine.charge_residual):
        assert math.isnan(float(quantity(row).iloc[0])), quantity.__name__
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


def test_charge_balance_holds_on_every_published_row(measurements):
    """The release states a 5e-6 ceiling; this is the check that keeps it true."""
    worst = 0.0
    for family, df in measurements.items():
        residual = brine.charge_residual(df).abs()
        known = brine.composition_known(df)
        assert residual[~known].isna().all(), family
        bad = df.loc[known & (residual > CHARGE_BALANCE_TOL), "point_id"]
        assert bad.empty, "%s: %d row(s) miss charge balance, first %s" % (
            family, len(bad), bad.iloc[0] if len(bad) else "")
        if known.any():
            worst = max(worst, float(residual[known].max()))
    assert worst <= CHARGE_BALANCE_TOL


def test_every_row_is_either_wholly_known_or_wholly_blank(measurements):
    """No published row carries a part composition; both kinds exist in the release.

    Per family the rule is only "never partial" -- `liquidwatercontent` is 18 rows and
    every one of them has a known composition, which is a fact about that file and not a
    thing to assert of each.
    """
    known = blank = 0
    for _family, df in measurements.items():
        got = brine.composition_known(df)            # raises on a partial row
        known += int(got.sum())
        blank += int((~got).sum())
    assert known > 0 and blank > 0, (known, blank)
    assert known + blank == sum(len(df) for df in measurements.values())


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
                           "the release is CSV only (R-DB3-9)")
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
    assert any(d.replace(" ", "").startswith("pandas>=2") for d in meta["dependencies"])
    assert len(meta["dependencies"]) == 1, meta["dependencies"]


def test_the_module_entry_point_prints_a_count_per_family(root, capsys):
    from aquasoldb.__main__ import print_counts
    assert print_counts([str(root)]) == 0
    printed = capsys.readouterr().out
    for family in aquasoldb.TABLE_NAMES:
        assert family in printed, printed
    assert aquasoldb.__version__ in printed
    assert print_counts([str(root), "extra"]) == 2
    assert sys.modules["aquasoldb"].__version__ == "1.1.0"
