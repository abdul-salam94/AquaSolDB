# -*- coding: utf-8 -*-
"""Brine quantities computed from the published ion molalities, and the gas mole fraction.

The ion rule the release states: a row's ion columns (`m_Na`, `m_Cl`, `m_K`, `m_Ca`,
`m_Mg`, `m_SO4`, as many of them as the file carries) are filled together or blank
together.  Blank means the composition of that medium is not known to us in numbers --
the source prints none we can resolve, or the medium carries an ion outside these six.  A
blank is never a zero.

A file carries only the ion columns that are non-zero somewhere in it.  The column
dictionary names the ones it left out ("Dropped as always zero: ..."), and only those
read as zero; a missing ion column the dictionary does not name is an error, never a
zero.  Where a row's ion columns are blank, or a file carries none, the composition is
known only for pure water (salt = none), whose ions are all zero; every other such row
gives NaN.  No value is filled in, assumed, or taken from `salt_molality` instead.  A row
with SOME of its file's ion columns filled is a broken file, and is raised on rather than
worked around.
"""
import pandas as pd

from .subset import PURE_WATER
from .tables import ATTR_DROPPED_ZERO, ATTR_TABLE

#: The six ion columns, in the order the files carry them.
ION_COLUMNS = ("m_Na", "m_Cl", "m_K", "m_Ca", "m_Mg", "m_SO4")

#: Formal charge of each ion, fully dissociated.
ION_CHARGE_NUMBER = {"m_Na": 1, "m_Cl": -1, "m_K": 1, "m_Ca": 2, "m_Mg": 2, "m_SO4": -2}

#: Moles of water in one kilogram of water, 1000 / 18.0153 -- the constant the database
#: itself uses for every mole-fraction conversion it makes.
WATER_MOL_PER_KG = 1000.0 / 18.0153

#: The molality column `to_mole_fraction` converts.
SOLUBILITY_COLUMN = "solubility_mol_per_kgw"


def _ions(df):
    """The six columns as floats, NaN on a row whose composition is not known."""
    present = [c for c in ION_COLUMNS if c in df.columns]
    absent = [c for c in ION_COLUMNS if c not in df.columns]
    dropped = set(df.attrs.get(ATTR_DROPPED_ZERO, ()))
    undeclared = [c for c in absent if c not in dropped]
    if undeclared:
        raise KeyError(
            "this table has no ion column %s, and the column dictionary does not declare it "
            "dropped as always zero for %s, so it cannot be read as zero. Open the file with "
            "open_table, which records the declared columns, or keep every ion column the "
            "file ships." % (", ".join(undeclared),
                             df.attrs.get(ATTR_TABLE, "this table")))
    ions = pd.DataFrame({c: pd.to_numeric(df[c], errors="coerce") for c in present},
                        index=df.index, columns=present, dtype="float64")
    filled = ions.notna().sum(axis=1)
    partial = filled[(filled > 0) & (filled < len(present))]
    if len(partial):
        raise ValueError(
            "%d row(s) carry some but not all of this file's ion molalities, which the "
            "release's ion rule forbids (filled together or blank together). First: index "
            "%r. This file is not an AquaSolDB release as published."
            % (len(partial), partial.index[0]))
    known = filled == len(present) if present else pd.Series(False, index=df.index)
    if "salt" in df.columns:
        pure = df["salt"].astype("string").fillna("").str.strip() == PURE_WATER
        blank_pure = pure & (filled == 0)
    else:
        blank_pure = pd.Series(False, index=df.index)
    out = pd.DataFrame(index=df.index)
    for c in ION_COLUMNS:
        values = ions[c] if c in present else pd.Series(0.0, index=df.index)
        values = values.where(known, float("nan"))
        out[c] = values.mask(blank_pure, 0.0)
    return out


def composition_known(df):
    """Boolean Series: is this row's medium composition known to us in numbers?

    True when the row's ion columns are filled -- including the zeros of pure water, whose
    composition IS known -- and on a pure-water row (salt = none) whatever its ion cells.
    False where the composition is blank.
    """
    return _ions(df).notna().all(axis=1)


def ion_strength(df):
    """Ionic strength in mol per kg of water: 0.5 * sum(m_i * z_i^2). NaN where blank."""
    ions = _ions(df)
    total = sum(ions[c] * (ION_CHARGE_NUMBER[c] ** 2) for c in ION_COLUMNS)
    return (0.5 * total).rename("ion_strength_mol_per_kgw")


def total_ions(df):
    """Sum of the ion molalities, mol per kg of water. NaN where blank.

    This is the total of IONS, which on a fully dissociated single salt is about twice
    the salt molality; it is not `salt_molality` and does not replace it.
    """
    ions = _ions(df)
    return sum(ions[c] for c in ION_COLUMNS).rename("total_ions_mol_per_kgw")


def charge_residual(df):
    """(m_Na + m_K + 2 m_Ca + 2 m_Mg) - (m_Cl + 2 m_SO4), mol per kg of water.

    Zero to within the storage precision of the release (5e-6) on every row whose
    composition is known; NaN where it is blank.  A residual away from zero on a published
    row is a defect to report, not a number to use.
    """
    ions = _ions(df)
    residual = sum(ions[c] * ION_CHARGE_NUMBER[c] for c in ION_COLUMNS)
    return residual.rename("charge_residual_mol_per_kgw")


def to_mole_fraction(df, include_salt=False):
    """The dissolved gas as a mole fraction, from `solubility_mol_per_kgw` (m).

    include_salt=False   x = m / (m + N_W), counting only the gas and the water
                         (N_W = 1000 / 18.0153 mol of water per kg)
    include_salt=True    x = m / (m + N_W + S), S = the sum of the ion molalities
                         (`total_ions`), so every dissolved ion counts as a particle; NaN
                         where the composition is blank, and S = 0 for pure water

    A blank m gives NaN.  The stored molality is not changed.
    """
    if SOLUBILITY_COLUMN not in df.columns:
        raise KeyError("this table has no %r column; to_mole_fraction converts the "
                       "dissolved-gas molality of solubility and mixtures rows"
                       % SOLUBILITY_COLUMN)
    m = pd.to_numeric(df[SOLUBILITY_COLUMN], errors="coerce").astype("float64")
    if include_salt:
        x = m / (m + WATER_MOL_PER_KG + total_ions(df))
        return x.rename("gas_mole_fraction_with_salt")
    return (m / (m + WATER_MOL_PER_KG)).rename("gas_mole_fraction_salt_free")
