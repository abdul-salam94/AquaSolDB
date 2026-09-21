# AquaSolDB v1.0

Published experimental measurements of how much gas dissolves in water and in
brine, read from the printed pages of the papers that reported them and put into
one set of tables with one set of units. 22,872 measurement rows from
496 sources. **Status: v1.0, released 2026-09-21** -- archived on Zenodo:
version DOI 10.5281/zenodo.22870467, concept DOI 10.5281/zenodo.22870466.

## How to cite

Cite this dataset for the compilation, and **cite the paper that printed a value
for the value itself**. Every row names its source in `source_id`, and
`csv/sources.csv` gives that source's full reference and, where one exists, its
DOI. `CITATION.cff` carries the same instruction in machine-readable form.

> Abd, A. (2026). AquaSolDB v1.0 [Data set]. Zenodo. https://doi.org/10.5281/zenodo.22870467

There are two addresses and they say different things. The version DOI above
names exactly v1.0 and nothing else, so it is the one to cite for a number you
took from these files: it can never resolve to a different set of rows. The
concept DOI https://doi.org/10.5281/zenodo.22870466 always resolves to the
newest version, so it is the one to cite for the database as a whole. The files
and the release notes are in the GitHub repository
https://github.com/abdul-salam94/AquaSolDB.

## What is in it, and what is not

Nine gases -- CO2, CH4, H2, N2, H2S, ethane, propane, n-butane and i-butane --
plus a few audited rows of other gases, labelled as such. Two kinds of medium:
pure water and brine, where brine means **dissolved salts only**. Six kinds of
measurement: gas dissolved in water, gas dissolved in brine, gas-mixture
solubility, water content of a gas or vapour phase, water content of a
hydrocarbon-rich liquid phase, and phase-boundary points.

Measurements in anything else are out of scope and are in none of these files:
acids, bases, organic co-solvents such as methanol and the glycols, surfactants,
colloids, heavy water, exotic media such as uranyl sulfate. Nor are quantities
that are not an absolute measurement of dissolved gas -- solution enthalpies,
Henry-law constants, partial molal volumes, salting-out constants. Scope is
decided by the **medium the source names**, never by a reported concentration,
so an empty concentration cell must never be read as "pure water".

Whether a measurement was used by, held out of, or rejected from any model fit
is **not** recorded here: that is a property of the fit, and no column of this
database encodes it.

Values were read from rendered images of the printed pages, and the reading is
checked by sampling rather than row by row: the most recent audit re-read 60
published rows against their pages and found 56 as printed, 1 that disagreed
with the page, 1 page the rendered corpus does not hold, and 2 rows digitized
from a figure, which have no printed digit to check. Rows flagged
`digitized_from_figure` are outside that check by construction.

## The files

| file | rows | what it holds |
|---|---|---|
| `csv/solubility.csv` | 18,200 | gas dissolved in water or brine |
| `csv/watercontent.csv` | 2,013 | water in the gas or vapour phase |
| `csv/liquidwatercontent.csv` | 18 | water in a hydrocarbon-rich liquid phase |
| `csv/mixtures.csv` | 1,661 | solubility from a gas mixture |
| `csv/phaseboundaries.csv` | 980 | hydrate, dew, bubble and three-phase points |
| `csv/sources.csv` | 496 | one row per source: full reference, year, DOI, row counts |
| `csv/column_dictionary.csv` | - | every column: unit, meaning, blank rule, how it was arrived at |
| `provenance/row_crosswalk.csv` | 22,872 | one row per published row, naming the internal record behind it |
| `provenance/screened_rows.csv` | 1,827 | every audited row NOT published, with the reason |
| `CONTRIBUTING.md` | - | how to report a wrong value, and how to contribute rows |

`SCHEMA.md` says the same as the column dictionary in document form, generated
from it. `provenance/CHECKSUMS.sha256` holds a digest for each data file and
`SHA256SUMS.txt` one for every file here. A measurement appears in exactly one
file; mixed-gas measurements are always in `csv/mixtures.csv`.

## The columns

Every measurement file starts with the same columns, so one reader works on all
five. `point_id` is a permanent row identifier; `gas`, `temperature_K` and
`pressure_MPa` are the state, with `pressure_basis` saying what the pressure was
measured against; `salt`, `salt_molality` and `salt_composition` describe the
medium; `m_Na`, `m_Cl`, `m_K`, `m_Ca`, `m_Mg` and `m_SO4` give that medium's
composition as per-ion molalities in mol per kg of water; `source_id`,
`reference` and `method` say where the number came from and how it was measured;
`flags` carries row-level warnings. After those come the measured quantity in
normalized units and the same quantity `value_as_printed` with its
`unit_as_printed`, exactly as the page gave it. **The ion rule:** the six ion
cells are filled together or blank together, never in part. Blank means the
composition is not known to us in numbers -- the source prints none we can
resolve, or the medium contains an ion outside these six, such as a carbonate or
a bicarbonate, and half a composition would state a brine that does not balance.
A blank is never a zero; pure water carries six zeros. Where the six are filled
they balance charge, m_Na + m_K + 2*m_Ca + 2*m_Mg equal to m_Cl + 2*m_SO4 within
5e-6 mol per kg. 17,961 published rows carry the six numbers and
4,911 carry six blanks.

## Flags

`flags` is empty on a clean row and otherwise holds one or more of five words,
separated by semicolons. `from_compilation` means the row reaches us through a
compilation, a data series or a secondary transcription rather than the primary
experimental paper. `digitized_from_figure` means the number was read off a
published figure, so there is no printed digit behind it. `printed_defect`
means the printed source itself carries a defect at this row -- a typo, a
mislabelled heading, an illegible cell, an impossible unit. `suspect_value`
means the value is physically or statistically implausible as printed.
`replicate` means the paper prints this measurement more than once -- an old
titration or volumetric sheet that tabulates each run instead of a mean, where two
runs round to the same digits -- and both rows are kept, so a reader who wants one
point per state can average or drop by hand rather than being handed our choice.
Flagged rows are published, never silently dropped: the flag is there so you can
decide.

## Methods

`method` says how the measurement was made, read from the source itself and
recorded per source rather than per row, so where a paper prints several tables
measured different ways the column gives the dominant one. Ten classes, each
defined in `SCHEMA.md`; `unstated` means the paper was read and does not say. In
this release, by rows:

analytical sampling 8,960, manometric volumetric 3,312, chromatography 1,831,
synthetic visual 2,328, electrochemical 409, gravimetric 1,271, pressure
decrease mass balance 32, calculated compilation 1,121, other 1,514, unstated
1,850.

## Known limitations

- **Some brine rows carry no ion composition.** 2,142 published rows
  labelled `mixed` have six blank ion cells, usually because the medium contains
  an ion outside the six, which the rule refuses to fill in part. A smaller
  group carries a printed zero that is a placeholder, not a measured zero (a
  "composition not separately reported" cell); those are blank too, rather than
  asserting a composition nobody printed.
- **Some rows reach us through a transcription, not the original page.** They
  carry `from_compilation`, and the source row names the compilation or series.
- **`salt_molality` is empty on some mixed brines.** It comes from the six ion
  molalities and is empty where those are blank. It is never the sum of two
  recorded salt slots, which double-counted on some sources.
- **`page_ref` is not published.** An internal audit found the page pointer
  wrong on about one row in eight, so it is held back until that pass is done.

## Licence

CC BY 4.0. The full legal code is in `LICENSE`, with a note on what the licence
covers: the compilation, not the measurements, which belong to the authors who
published them and must be cited.

## Versions

Semantic versions: 1.x for corrections and additions that do not change what the
database covers, 2.0 when the scope grows. `point_id`s are permanent; new rows
append. Each release gets its own DOI, and all of them sit under one concept DOI
that always resolves to the newest -- **cite the version DOI**, so that a number
computed from this database can be traced to the exact release it came from.
`CHANGELOG.md` has one section per release.

## Where to get it

- Repository (the files and the release notes):
  https://github.com/abdul-salam94/AquaSolDB
- Zenodo record (the archived copy of exactly these files, under the version
  DOI 10.5281/zenodo.22870467): https://zenodo.org/records/22870467
- Concept DOI, which always resolves to the newest version:
  https://doi.org/10.5281/zenodo.22870466

**Python package.** The repository ships a small reader, `aquasoldb`: it loads
these files into pandas with the units and blank rules above, narrows by gas,
medium, temperature and pressure, and derives ion strength, total ions and the
charge residual from the six ion columns, leaving a blank composition blank.
It needs pandas and nothing else, and it is installed from the repository:
`pip install .` in a clone, or `pip install git+https://github.com/abdul-salam94/AquaSolDB`.

```python
from aquasoldb import open_table, narrow
df = open_table("solubility")
hot = narrow(df, gas="H2", medium="brine", T_K=(298.15, 423.15))
```

`aquasoldb/README.md` is its ten-line manual. The data stays CC BY 4.0; the
reader's own code is MIT.
