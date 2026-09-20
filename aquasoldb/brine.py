# -*- coding: utf-8 -*-
"""Brine quantities computed from the six published ion molalities.

The ion rule the release states: the six cells `m_Na`, `m_Cl`, `m_K`, `m_Ca`, `m_Mg`,
`m_SO4` are filled together or blank together.  Blank means the composition of that
medium is not known to us in numbers -- the source prints none we can resolve, or the
medium carries an ion outside these six.  A blank is never a zero, and pure water carries
six zeros.

Every function here honours that rule literally: where the six are blank the result is
NaN, and no value is filled in, assumed, or taken from `salt_molality` instead.  A row
with SOME of the six filled would be a broken file, and is raised on rather than worked
around.
"""
import pandas as pd

#: The six published ion columns, in the order they appear in every measurement file.
ION_COLUMNS = ("m_Na", "m_Cl", "m_K", "m_Ca", "m_Mg", "m_SO4")

#: Formal charge of each ion, fully dissociated.
ION_CHARGE_NUMBER = {"m_Na": 1, "m_Cl": -1, "m_K": 1, "m_Ca": 2, "m_Mg": 2, "m_SO4": -2}


def _ions(df):
    """The six columns as floats, with the whole-or-blank rule enforced."""
    missing = [c for c in ION_COLUMNS if c not in df.columns]
    if missing:
        raise KeyError("this table has no ion columns %s; the six ion molalities ship in "
                       "every measurement file" % ", ".join(missing))
    ions = pd.DataFrame({c: pd.to_numeric(df[c], errors="coerce") for c in ION_COLUMNS},
                        index=df.index)
    filled = ions.notna().sum(axis=1)
    partial = filled[(filled > 0) & (filled < len(ION_COLUMNS))]
    if len(partial):
        raise ValueError(
            "%d row(s) carry some but not all six ion molalities, which the release's ion "
            "rule forbids (filled together or blank together). First: index %r. This file "
            "is not an AquaSolDB release as published."
            % (len(partial), partial.index[0]))
    return ions


def composition_known(df):
    """Boolean Series: is this row's medium composition known to us in numbers?

    True when all six ion molalities are present -- including the six zeros of pure
    water, whose composition IS known.  False when all six are blank.
    """
    return _ions(df).notna().all(axis=1)


def ion_strength(df):
    """Ionic strength in mol per kg of water: 0.5 * sum(m_i * z_i^2). NaN where blank."""
    ions = _ions(df)
    total = sum(ions[c] * (ION_CHARGE_NUMBER[c] ** 2) for c in ION_COLUMNS)
    return (0.5 * total).rename("ion_strength_mol_per_kgw")


def total_ions(df):
    """Sum of the six ion molalities, mol per kg of water. NaN where blank.

    This is the total of IONS, which on a fully dissociated single salt is about twice
    the salt molality; it is not `salt_molality` and does not replace it.
    """
    ions = _ions(df)
    return sum(ions[c] for c in ION_COLUMNS).rename("total_ions_mol_per_kgw")


def charge_residual(df):
    """(m_Na + m_K + 2 m_Ca + 2 m_Mg) - (m_Cl + 2 m_SO4), mol per kg of water.

    Zero to within the storage precision of the release (5e-6) on every row whose six
    cells are filled; NaN where they are blank.  A residual away from zero on a published
    row is a defect to report, not a number to use.
    """
    ions = _ions(df)
    residual = sum(ions[c] * ION_CHARGE_NUMBER[c] for c in ION_COLUMNS)
    return residual.rename("charge_residual_mol_per_kgw")
