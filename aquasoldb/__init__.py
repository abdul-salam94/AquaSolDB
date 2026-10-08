# -*- coding: utf-8 -*-
"""AquaSolDB -- read the published CSVs into pandas, narrow them, derive brine quantities.

AquaSolDB is a compilation of published measurements of how much gas dissolves in water
and in brine, read from the printed pages of the papers that reported them.  This package
is the reference reader for the files that ship with the dataset: it does not contain,
compute or correct a single measured value, and it never invents one.  Every number it
returns is the number in the CSV, with the exceptions that say so in their names --
`ion_strength`, `total_ions` and `charge_residual`, arithmetic on the published ion
molalities, and `to_mole_fraction`, the stored molality written as a mole fraction.

    >>> from aquasoldb import open_table, narrow, ion_strength, to_mole_fraction
    >>> df = open_table("solubility")
    >>> hot = narrow(df, gas="H2", medium="brine", status="measured", T_K=(298.0, 373.0))
    >>> hot["I"] = ion_strength(hot)
    >>> hot["x"] = to_mole_fraction(hot, include_salt=True)

The blank rule runs through everything here: an empty ion cell means the composition is
not known to us in numbers, so it becomes NaN and propagates to NaN.  A blank is never
read as a zero and is never guessed at; the only zeros read in are those of pure water
and the ion columns the column dictionary declares dropped as always zero.

The data are found locally (see `release_folder`); `download()` fetches a release from
its archive once, on request, into a cache on disk.

Data licence CC BY 4.0 (`LICENSE`); this code MIT (`LICENSE-CODE`).  Cite the paper that
printed a value for the value itself -- `source_id` names it on every row, and
`with_citation` adds its reference and DOI.
"""
from .tables import (AQUASOLDB_ROOT_ENV, DETAIL_NAMES, MEASUREMENT_TABLES, TABLE_NAMES,
                     dtypes_from_dictionary, open_detail, open_table, release_folder,
                     row_counts, verify_checksums, with_citation)
from .subset import FLAG_VOCABULARY, MEDIA, NOT_STATED, narrow
from .brine import (ION_CHARGE_NUMBER, ION_COLUMNS, WATER_MOL_PER_KG, charge_residual,
                    composition_known, ion_strength, to_mole_fraction, total_ions)
from .remote import AQUASOLDB_CACHE_ENV, CONCEPT_DOI, download
from .save import save_csv, save_parquet

__version__ = "2.0.0"
#: The dataset release this reader is the reference reader for.
DATASET_VERSION = "2.0"

__all__ = [
    "__version__", "DATASET_VERSION", "CONCEPT_DOI",
    "AQUASOLDB_ROOT_ENV", "AQUASOLDB_CACHE_ENV", "TABLE_NAMES", "MEASUREMENT_TABLES",
    "DETAIL_NAMES", "release_folder", "download", "dtypes_from_dictionary", "open_table",
    "open_detail", "with_citation", "row_counts", "verify_checksums",
    "FLAG_VOCABULARY", "MEDIA", "NOT_STATED", "narrow",
    "ION_COLUMNS", "ION_CHARGE_NUMBER", "WATER_MOL_PER_KG", "charge_residual",
    "composition_known", "ion_strength", "total_ions", "to_mole_fraction",
    "save_csv", "save_parquet",
]
