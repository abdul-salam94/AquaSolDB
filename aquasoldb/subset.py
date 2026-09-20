# -*- coding: utf-8 -*-
"""One selection function over any AquaSolDB measurement table.

`narrow` refuses a value the column does not hold.  A misspelt gas, salt or flag is an
error naming what is there, never a silently empty result -- the failure mode that turns
into a wrong number in a paper.
"""
import pandas as pd

#: The five row-status flags the release publishes (README, "Flags").  `replicate` joined
#: the set at the final v1.0 build (PD-DB8-1, KI-143): it marks both rows of a measurement
#: the paper prints more than once, and a reader who wants one point per state excludes it
#: by hand rather than being handed our choice of which run to keep.
FLAG_VOCABULARY = ("from_compilation", "digitized_from_figure", "printed_defect",
                   "suspect_value", "replicate")
#: `medium=` takes one of these.  The dataset has exactly two kinds of medium.
MEDIA = ("water", "brine")
#: The `salt` value that means pure water; every other value is a dissolved-salt medium.
PURE_WATER = "none"


def _as_list(value):
    if value is None:
        return None
    if isinstance(value, str):
        return [value]
    return list(value)


def _require_column(df, column, what):
    if column not in df.columns:
        raise KeyError("this table has no %r column, so it cannot be filtered by %s; "
                       "columns: %s" % (column, what, ", ".join(map(str, df.columns))))


def _match(df, column, values, what):
    """Case-insensitive exact match, refusing a value the column does not hold."""
    _require_column(df, column, what)
    series = df[column].astype("string").fillna("")
    folded = series.str.casefold()
    present = {v.casefold(): v for v in series.unique().tolist()}
    keep = set()
    unknown = []
    for v in values:
        key = str(v).casefold()
        if key not in present:
            unknown.append(v)
        else:
            keep.add(key)
    if unknown:
        shown = sorted(present.values())
        if len(shown) > 12:
            shown = shown[:12] + ["... %d more" % (len(present) - 12)]
        raise ValueError("no row of this table has %s %s; the column holds: %s"
                         % (what, ", ".join(repr(u) for u in unknown), ", ".join(shown)))
    return folded.isin(keep)


def _window(df, column, bounds, what):
    """Inclusive (lo, hi); either end may be None for unbounded.

    A row whose value is blank is NOT in any window: an unprinted temperature is not
    known to lie in a range, and a range filter that kept it would be stating something
    the source never printed.
    """
    _require_column(df, column, what)
    try:
        lo, hi = bounds
    except (TypeError, ValueError):
        raise ValueError("%s takes a (low, high) pair, got %r" % (what, bounds)) from None
    if lo is not None and hi is not None and float(lo) > float(hi):
        raise ValueError("%s low %r is above high %r" % (what, lo, hi))
    values = pd.to_numeric(df[column], errors="coerce")
    mask = values.notna()
    if lo is not None:
        mask &= values >= float(lo)
    if hi is not None:
        mask &= values <= float(hi)
    return mask


def narrow(df, gas=None, medium=None, T_K=None, P_MPa=None, salt=None, source_id=None,
           flags_exclude=None):
    """Return the rows of `df` that match every argument given.

    gas           one gas label or a sequence of them, e.g. "H2" or ["CO2", "CH4"]
    medium        "water" (salt = none) or "brine" (any dissolved salt).  Rows whose
                  medium the source did not record are in neither.
    T_K, P_MPa    inclusive (low, high) pairs; either end may be None
    salt          one medium label or a sequence: none, NaCl, KCl, CaCl2, MgCl2,
                  seawater, mixed
    source_id     one source key or a sequence
    flags_exclude one flag word or a sequence; rows carrying any of them are dropped

    Arguments combine with AND.  The result is a copy, so the caller can add columns to
    it without touching the loaded table.
    """
    mask = pd.Series(True, index=df.index)

    if gas is not None:
        mask &= _match(df, "gas", _as_list(gas), "gas")
    if salt is not None:
        mask &= _match(df, "salt", _as_list(salt), "salt")
    if source_id is not None:
        mask &= _match(df, "source_id", _as_list(source_id), "source_id")

    if medium is not None:
        if medium not in MEDIA:
            raise ValueError("medium is one of %s, got %r" % (", ".join(MEDIA), medium))
        _require_column(df, "salt", "medium")
        labels = df["salt"].astype("string").fillna("")
        recorded = labels.str.strip() != ""
        is_water = labels.str.casefold() == PURE_WATER
        mask &= (recorded & is_water) if medium == "water" else (recorded & ~is_water)

    if T_K is not None:
        mask &= _window(df, "temperature_K", T_K, "T_K")
    if P_MPa is not None:
        mask &= _window(df, "pressure_MPa", P_MPa, "P_MPa")

    if flags_exclude is not None:
        wanted = _as_list(flags_exclude)
        unknown = [f for f in wanted if f not in FLAG_VOCABULARY]
        if unknown:
            raise ValueError("unknown flag(s) %s; AquaSolDB publishes %s"
                             % (", ".join(repr(u) for u in unknown),
                                ", ".join(FLAG_VOCABULARY)))
        _require_column(df, "flags", "flags_exclude")
        carried = df["flags"].astype("string").fillna("").map(
            lambda s: {f.strip() for f in s.split(";") if f.strip()})
        mask &= ~carried.map(lambda got: bool(got & set(wanted)))

    return df[mask].copy()
