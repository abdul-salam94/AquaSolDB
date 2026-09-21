# -*- coding: utf-8 -*-
"""AquaSolDB -- read the published CSVs into pandas, narrow them, derive brine quantities.

AquaSolDB is a compilation of published measurements of how much gas dissolves in water
and in brine, read from the printed pages of the papers that reported them.  This package
is the reference reader for the files that ship with the dataset: it does not contain,
compute or correct a single measured value, and it never invents one.  Every number it
returns is the number in the CSV, with three exceptions that say so in their names --
`ion_strength`, `total_ions` and `charge_residual` in `brine`, which are arithmetic on the
six published ion molalities.

    >>> from aquasoldb import open_table, narrow, ion_strength
    >>> df = open_table("solubility")
    >>> hot = narrow(df, gas="H2", medium="brine", T_K=(298.0, 373.0))
    >>> hot["I"] = ion_strength(hot)

The blank rule runs through everything here: an empty ion cell means the composition is
not known to us in numbers, so it becomes NaN and propagates to NaN.  A blank is never
read as a zero and is never guessed at.

Data licence CC BY 4.0 (`LICENSE`); this code MIT (`LICENSE-CODE`).  Cite the paper that
printed a value for the value itself -- `source_id` names it on every row.
"""
from .tables import (AQUASOLDB_ROOT_ENV, MEASUREMENT_TABLES, TABLE_NAMES,
                     dtypes_from_dictionary, open_table, release_folder, row_counts,
                     verify_checksums)
from .subset import FLAG_VOCABULARY, MEDIA, narrow
from .brine import (ION_CHARGE_NUMBER, ION_COLUMNS, charge_residual, composition_known,
                    ion_strength, total_ions)
from .save import save_csv, save_parquet

__version__ = "1.1.0"
#: The dataset release this reader is the reference reader for.
DATASET_VERSION = "1.1"

__all__ = [
    "__version__", "DATASET_VERSION",
    "AQUASOLDB_ROOT_ENV", "TABLE_NAMES", "MEASUREMENT_TABLES", "release_folder",
    "dtypes_from_dictionary", "open_table", "row_counts", "verify_checksums",
    "FLAG_VOCABULARY", "MEDIA", "narrow",
    "ION_COLUMNS", "ION_CHARGE_NUMBER", "charge_residual", "composition_known",
    "ion_strength", "total_ions",
    "save_csv", "save_parquet",
]
